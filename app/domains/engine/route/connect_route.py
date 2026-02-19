# app\domains\engine\route\connect_route.py

from fastapi import APIRouter, Depends
from app.domains.engine.schema.connection_schema import ConnectionRequest, ConnectionResponse
from app.domains.engine.service.connection_service import ConnectionService
from app.infrastructure.lib3270.terminal_driver import TerminalDriver

router = APIRouter()

# Instância única compartilhada por todas as rotas
_driver = TerminalDriver()

def get_connection_service():
    # Passamos sempre o MESMO driver para o serviço
    return ConnectionService(_driver)

@router.post("/connect", response_model=ConnectionResponse)
async def connect_mainframe(
    data: ConnectionRequest, 
    service: ConnectionService = Depends(get_connection_service)
):
    # Agora o service usará o driver que já tem a h_session correta
    return await service.connect(data)