from pydantic import BaseModel, Field
from typing import List, Optional

class ScreenSucess(BaseModel):
    """Define uma área da tela e o texto esperado nela"""
    text: Optional[str] = None
    pos_start: int
    pos_end: int

class ScreenError(BaseModel):
    """Define uma área da tela e o texto esperado nela"""
    pos_start: int
    pos_end: int

class FieldInput(BaseModel):
    """Define um valor a ser inserido em uma posição específica"""
    value: str
    pos_start: int
    pos_end: int

class AutomationSlice(BaseModel):
    """A estrutura completa da 'Fatia' de automação"""
    command: str = Field(..., description="Comando para o mainframe (ex: 3.4)")
    pos_start: int
    pos_end: int
    # Validação de contexto (Onde estou?)
    confirmation: ScreenSucess
    
    # Validação de resultado (O que aconteceu?)
    msg_success: ScreenSucess
    msg_error: ScreenError
    
    # Dados para preenchimento
    fields: List[FieldInput]

class DataSlice(BaseModel):
    """A estrutura completa da 'Fatia' de automação"""
    command: str