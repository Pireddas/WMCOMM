from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, Field

class ConnectionRequest(BaseModel):
    """Dados de entrada para a conexão"""
    host: str = Field(..., example="tn3270://127.0.0.1:3270")
    model: str = Field(default="3279-2-E", description="Modelo do terminal")

class ConnectionResponse(BaseModel):
    """Resposta padronizada"""
    status: str
    state_id: int
    state_name: str
    lock_status: int
    handle: Optional[int] = None # O ponteiro da sessão (h_session)
    url: str  # Retornamos a URL confirmada pelo motor