import sqlite3, os, psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.application.config import settings

def init_api_key_db():
    if not os.path.exists(settings.DB_DIR):
        os.makedirs(settings.DB_DIR)

    if settings.DB_TYPE == "sqlite":
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {settings.TBL_API_KEY} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_hash TEXT UNIQUE NOT NULL,
                owner TEXT NOT NULL,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        
    elif settings.DB_TYPE == "postgresql":
        # 1. Extrair informações da URL para conectar ao banco padrão 'postgres'
        # Isso permite criar o banco 'governance' programaticamente
        base_url = settings.POSTGRES_URL.rsplit('/', 1)[0]
        db_name = settings.POSTGRES_URL.rsplit('/', 1)[1]
        postgres_default_url = f"{base_url}/postgres"

        try:
            # Conexão inicial para garantir que o banco de dados existe
            conn_admin = psycopg2.connect(postgres_default_url, client_encoding='utf8')
            conn_admin.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor_admin = conn_admin.cursor()

            # Verifica se o banco alvo existe
            cursor_admin.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
            exists = cursor_admin.fetchone()

            if not exists:
                print(f"PostgreSQL: Banco '{db_name}' não encontrado. Criando...")
                cursor_admin.execute(f"CREATE DATABASE {db_name}")
            
            cursor_admin.close()
            conn_admin.close()

            # 2. Agora conecta no banco específico para criar a tabela
            conn = psycopg2.connect(settings.POSTGRES_URL, client_encoding='utf8')
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {settings.TBL_API_KEY} (
                    id SERIAL PRIMARY KEY,
                    key_hash TEXT UNIQUE NOT NULL,
                    owner TEXT NOT NULL,
                    active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print(f"PostgreSQL: Banco '{db_name}' e tabelas prontos!")

        except Exception as e:
            error_msg = str(e).encode('utf-8', errors='replace').decode('utf-8')
            print(f"Erro crítico no bootstrap do Postgres: {error_msg}")
            raise e