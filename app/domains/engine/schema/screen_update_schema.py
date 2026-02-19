from pydantic import BaseModel, Field

class ScreenResponse(BaseModel):
    screen: str