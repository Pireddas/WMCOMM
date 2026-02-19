# app\infrastructure\auth\auth_repository.py 

from app.application.config import settings
from app.infrastructure.auth.sqlite_api_key_repository import SqliteApiKeyRepository
from app.infrastructure.auth.postgres_api_key_repository import PostgresApiKeyRepository

class Repository():
    def __init__(self, owner: str = "", key_hash: str = None):
        self.owner = owner
        self.key_hash = key_hash
        self.db_type = settings.DB_TYPE

    def create(self):
        try:
            if self.db_type == "sqlite":
                SqliteApiKeyRepository().create(self.owner, self.key_hash)
            elif self.db_type == "postgresql":
                PostgresApiKeyRepository().create(self.owner, self.key_hash)
        except Exception as e:
            raise e

    def list(self):
        if self.db_type == "sqlite":
            return SqliteApiKeyRepository().list_by_owner(self.owner)
        elif self.db_type == "postgresql":
            return PostgresApiKeyRepository().list_by_owner(self.owner)


    def activate(self, key_id: int):
        if self.db_type == "sqlite":
            return SqliteApiKeyRepository().set_active(key_id, True)
        elif self.db_type == "postgresql":
            return PostgresApiKeyRepository().set_active(key_id, True)

    def deactivate(self, key_id: int):
        if self.db_type == "sqlite":
            return SqliteApiKeyRepository().set_active(key_id, False)
        elif self.db_type == "postgresql":
            return PostgresApiKeyRepository().set_active(key_id, False)