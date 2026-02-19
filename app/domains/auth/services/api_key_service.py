# app/domains/auth/services/api_key_service.py

import secrets
import hashlib
from app.infrastructure.auth.auth_repository import Repository

class BasicKeyService:

    def __init__(self):
        pass

    def create_key(self, owner: str) -> dict:

        raw_key = f"vibe_{secrets.token_hex(16)}"
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

        Repository(owner, key_hash).create()

        return {
            "nome": owner,
            "api_key": raw_key,
        }

    def list_key(self, owner: str):
        return Repository(owner).list()

    def deactivate_key(self, key_id: int):
        Repository().deactivate(key_id)

        return f"Chave {key_id} desativada"

    def activate_key(self, key_id: int):
        Repository().activate(key_id)

        return f"Chave {key_id} ativada"
