from pydantic import BaseModel
from typing import List

class LogoffResponse(BaseModel):
    status: str
    steps: List[str]