# app/domains/engine/schema/status_schema.py
from pydantic import BaseModel
from typing import Optional

class SessionStatus(BaseModel):
    ready: int
    cursor_addr: int
    connection_id: int
    connection_name: str
    is_connected: bool
    is_locked: bool
    current_screen: str  # Identificador amigável da tela atual
    active_url: Optional[str]

class StatusResponse(BaseModel):
    status: SessionStatus