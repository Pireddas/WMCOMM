# app\application\guards\service_guard.py

from fastapi import HTTPException, Request
from app.application.config import settings
from app.platform.observability.err_logger.error_assembler import Error
from app.platform.observability.logger import FastLog
 
def service_guard(service_name: str):
    async def _guard(request: Request):
        if not settings.is_service_enabled(service_name):
            msg, name = Error.error(
                request_id=request.state.request_id,
                error_key="SERVICE_MANUT"
            )
            FastLog.write_error(name=name, message=msg)
            raise HTTPException(
                status_code=msg["Status"],
                detail=msg["Error"],
            )
    return _guard