# app\domains\engine\route\disconnect_route.py

from fastapi import APIRouter, Depends
from app.domains.engine.schema.disconnect_schema import DisconnectResponse
from app.domains.engine.service.disconnect_service import DisconnectService
from app.infrastructure.lib3270.terminal_driver import TerminalDriver

router = APIRouter()
# Função auxiliar para injetar o serviço
def get_disconnection_service():
    driver = TerminalDriver()
    return DisconnectService(driver)

@router.post("/disconnect", response_model=DisconnectResponse)
async def disconnect(
    service: DisconnectService = Depends(get_disconnection_service)
):
    # O service já é uma instância criada pelo Depends
    return await service.disconnect()