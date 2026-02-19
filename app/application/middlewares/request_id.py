# app\application\middlewares\request_id.py

import time
import hashlib
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        raw_id = f"{start_time}-{request.client.host}-{request.url.path}"
        request_hash = hashlib.md5(raw_id.encode()).hexdigest()[:32]

        request.state.request_id = request_hash

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_hash
        return response
