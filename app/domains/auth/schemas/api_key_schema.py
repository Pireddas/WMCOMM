# app\domains\auth\schemas\api_key_schema.py

from pydantic import BaseModel, Field

# --- INPUT SCHEMA ---
class BasicKeyRequest(BaseModel):
    execution_id: str = Field(..., json_schema_extra={"example": "45e1c8ca-0cbb-4345-a197-38c34f15e2b3"})
    user: str = Field(..., json_schema_extra={"example": "Test User"}, description="Nome do Proprietário (Owner)")

# --- OUTPUT SCHEMA ---
class BasicKeyResponse(BaseModel):
    request_id: str = Field(..., description="Hash único da requisição para auditoria")
    nome: str = Field(..., description="Dono da Chave de Acesso")
    api_key: str = Field(..., description="Chave de acesso à API")

class ListKeyItem(BaseModel):
    id: int
    owner: str
    status: str
    create: str

class ListKeyResponse(BaseModel):
    request_id: str
    result: list[ListKeyItem]


class DeactKeyRequest(BaseModel):
    execution_id: str = Field(..., json_schema_extra={"example": "45e1c8ca-0cbb-4345-a197-38c34f15e2b3"}, description="Gerado pelo processo de requisição")
    ID: int = Field(..., json_schema_extra={"example": "1"}, description="ID da chave")

class DeactKeyResponse(BaseModel):
    request_id: str
    result: str

