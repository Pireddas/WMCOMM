# app\platform\observability\logging_middleware.py

import time, logging, os
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.application.config import settings
from app.platform.observability.logger import FastLog

log_dir = os.path.dirname(settings.API_LOG)

if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)
 
logger = logging.getLogger("api-governance")
logger.setLevel(logging.INFO)

if not logger.handlers:
    log_path = os.path.join(
        settings.API_LOG_DIR,
        settings.API_LOG_INFO
    )
    file_handler = logging.FileHandler(log_path)
    file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

class PerformanceLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        request_id = request.state.request_id
       
        response = await call_next(request)
        
        process_time = time.time() - start_time
        user_identity = getattr(request.state, "user", "anonymous")

        logged_params = getattr(request.state, "payload", dict(request.query_params))
        
        log_message = (
            f"ID: {request_id} | "
            f"User: {user_identity} | "
            f"Method: {request.method} | "
            f"Path: {request.url.path} | "
            f"Params: {logged_params} | "
            f"Time: {process_time:.4f}s | "
            f"Status: {response.status_code}"
        )
        
        FastLog.write_info(name="api-governance-middleware-info", message=log_message)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        
        return response
