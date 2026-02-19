# app/application/errors/handlers.py

from fastapi import Request
from fastapi.responses import JSONResponse
from app.application.errors.semantic_error import ApplicationError
from app.platform.observability.err_logger.error_assembler import Error
from app.platform.observability.logger import FastLog
 
async def semantic_error_handler(request: Request, exc: ApplicationError):
    msg, name = Error.error(
        request_id=getattr(request.state, "request_id", "unknown"),
        error_key=exc.code
    )

    FastLog.write_error(name=name, message=msg)

    return JSONResponse(
        status_code=msg["Status"],
        content={"detail": msg["Error"]},
    )
