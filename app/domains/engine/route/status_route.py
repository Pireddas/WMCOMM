# app/domains/engine/route/status_route.py
from fastapi import APIRouter
from app.domains.engine.schema.status_schema import StatusResponse
from app.domains.engine.service.status_service import StatusService
from app.infrastructure.lib3270.terminal_driver import TerminalDriver

router = APIRouter()
_driver = TerminalDriver()

# Mude para .post se o seu frontend estiver enviando POST
@router.post("/session-status", response_model=StatusResponse)
async def get_status():
    service = StatusService(_driver)
    return await service.get_detailed_status()