# app/domains/engine/route/automation_route.py
from fastapi import APIRouter, HTTPException
from app.domains.engine.schema.automation import AutomationSlice
from app.domains.engine.service.automation_service import AutomationService
from app.infrastructure.lib3270.terminal_driver import TerminalDriver

router = APIRouter()
_driver = TerminalDriver()

@router.post("/execute-slice")
async def receive_slice(slice_data: AutomationSlice):
    # Verificação de segurança da conexão
    if _driver.get_connection_state()["id"] < 5:
        raise HTTPException(status_code=400, detail="Terminal desconectado do Mainframe.")

    service = AutomationService(_driver)
    result = await service.execute_slice(slice_data)

    if result["status"] != "success":
        # Você pode optar por retornar 200 com o erro no corpo ou um erro HTTP
        raise HTTPException(status_code=422, detail=result)

    return result