# app\domains\engine\route\logon_route.py

from fastapi import APIRouter, Depends
from app.application.config import settings
from app.domains.engine.schema.logon_schema import LogonData, LogonResponse
from app.domains.engine.service.logon_service import LogonService
from app.infrastructure.lib3270.terminal_driver import TerminalDriver
from app.domains.engine.service.connection_service import ConnectionService
from app.domains.engine.schema.connection_schema import ConnectionRequest

router = APIRouter()

shared_driver = TerminalDriver()

def get_logon_service():
    """Injeta a dependência do Driver no Serviço."""
    return LogonService(shared_driver)

@router.post("/logon", response_model=LogonResponse)
async def logon(
    data: LogonData, 
    service: LogonService = Depends(get_logon_service)
):
    """
    Endpoint de logon orquestrado. 
    O 'service' aqui já vem instanciado com o TerminalDriver.
    """
    state=service.driver.get_connection_state()
    if state!=5:
        conn_service = ConnectionService(service.driver)
        conn_payload = ConnectionRequest(
            host=f"{settings.MF_HOST}:{settings.MF_PORT}", 
            model=settings.TN_MODEL
        )
        await conn_service.connect(conn_payload)

    return await service.execute_logon(data)