# app\domains\engine\route\screen_update_route.py

from fastapi import APIRouter, Depends
from app.infrastructure.lib3270.terminal_driver import TerminalDriver
from app.domains.engine.service.screen_service import ScreenService
from app.domains.engine.schema.screen_update_schema import ScreenResponse
router = APIRouter()

def get_screen_service():
    return ScreenService(TerminalDriver())

@router.post("/screen-update", response_model=ScreenResponse)
async def screen_view(service: ScreenService = Depends(get_screen_service)):
    """
    Renderiza a tela atual do mainframe com destaque em campos editáveis.
    """
    return await service.get_rendered_screen()