import psycopg2
from psycopg2.extras import RealDictCursor
from app.application.config import settings
from app.application.errors.semantic_error import ApplicationError

class PostgresApiKeyRepository:
    def _get_connection(self):
        # Em produção, você usaria um Pool de conexões, 
        # mas para seguir seu padrão atual:
        return psycopg2.connect(settings.POSTGRES_URL)

    def create(self, owner: str, key_hash: str):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"INSERT INTO {settings.TBL_API_KEY} (key_hash, owner) VALUES (%s, %s)",
                        (key_hash, owner),
                    )
                conn.commit()
        except Exception:
            raise ApplicationError("ERR_CREATING_API_KEY")

    def list_by_owner(self, owner: str):
        try:
            with self._get_connection() as conn:
                # RealDictCursor faz o resultado virar um dicionário similar ao sqlite3.Row
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        f"SELECT id, owner, active, created_at FROM {settings.TBL_API_KEY} WHERE owner = %s",
                        (owner,),
                    )
                    rows = cur.fetchall()
            
            if not rows:
                raise ApplicationError("NO_API_KEYS")
            
            return [
                {
                    "id": r["id"],
                    "owner": r["owner"],
                    "status": "Ativa" if r["active"] else "Inativa",
                    "create": r["created_at"].isoformat() if hasattr(r["created_at"], 'isoformat') else str(r["created_at"]),
                }
                for r in rows
            ]
        except ApplicationError:
            raise
        except Exception:
            raise ApplicationError("ERR_FETCHING_API_KEYS")

    def set_active(self, key_id: int, active: bool) -> bool:
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"UPDATE {settings.TBL_API_KEY} SET active = %s WHERE id = %s",
                        (active, key_id),
                    )
                    count = cur.rowcount
                conn.commit()
                return count > 0
        except Exception:
            raise ApplicationError("ERR_UPDATING_API_KEY")