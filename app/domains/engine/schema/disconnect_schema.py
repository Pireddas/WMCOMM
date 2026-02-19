from pydantic import BaseModel

class DisconnectResponse(BaseModel):
    status: str
    message: str
    screen: str