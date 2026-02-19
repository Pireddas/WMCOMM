# app\domains\engine\schema\logon_schema.py

from pydantic import BaseModel, Field
from typing import Optional, Dict

class LogonData(BaseModel):
    user_id: str = Field(..., example="HERC01")
    password: str = Field(..., example="CUL8TR")

class LogonResponse(BaseModel):
    status: Optional[str] = None
    final_cursor: Optional[int] = None
    connection_state: Optional[int] = None
    error: Optional[str] = None
    screen: Optional[Dict[str, str]] = None