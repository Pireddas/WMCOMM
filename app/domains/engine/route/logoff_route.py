# app\domains\engine\route\logoff_route.py

from fastapi import APIRouter, Depends
from app.domains.engine.schema.logoff_schema import LogoffResponse
from app.domains.engine.service.logoff_service import LogoffService
from app.infrastructure.lib3270.terminal_driver import TerminalDriver

router = APIRouter()

def get_logoff_service():
    """
    Função de dependência que instancia o Driver e o Service.
    Isso garante que o Service tenha acesso à sessão do terminal.
    """
    driver = TerminalDriver()
    return LogoffService(driver)

@router.post("/logoff", response_model=LogoffResponse)
async def logoff(service: LogoffService = Depends(get_logoff_service)):
    """
    Endpoint que agora recebe o service instanciado via Depends.
    """
    return await service.execute_logoff()