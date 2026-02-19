# app\main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.application.config import settings
from app.application.bootstrap import init_api_key_db
from app.platform.observability.logging_middleware import PerformanceLoggingMiddleware
from app.platform.observability.auth_middleware import SQLiteAuthMiddleware
from app.application.middlewares.request_id import RequestIDMiddleware

from app.infrastructure.lib3270.lib3270 import h_session, lib
from app.domains.engine.route.connect_route import router as connect_router
from app.domains.engine.route.logon_route import router as logon_router
from app.domains.engine.route.logoff_route import router as logoff_router
from app.domains.engine.route.disconnect_route import router as disconnect_router
from app.domains.engine.route.screen_update_route import router as screen_update
from app.domains.engine.route.status_route import router as status
from app.domains.engine.route.automation_route import router as automation_router
from app.domains.auth.route import api_key_route

from app.application.errors.semantic_error import ApplicationError
from app.application.errors.handlers import semantic_error_handler

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Início: O ambiente 3270 já está disponível via infra
    init_api_key_db()
    print("Engine iniciado. Sessão 3270 pronta.")
    yield
    # Fim: Desconexão limpa ao desligar o servidor
    if h_session and lib.lib3270_is_connected(h_session):
        print("Encerrando sessão 3270...")
        lib.lib3270_disconnect(h_session)
        lib.lib3270_main_iterate(h_session, 0)
    print("Sessão encerrada.")

app = FastAPI(
    dependencies=[Security(api_key_header)],
    lifespan=lifespan
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # em produção coloque o domínio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Middlewares
# -----------------------
app.add_middleware(PerformanceLoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SQLiteAuthMiddleware)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    dependencies=[Security(api_key_header)],
    lifespan=lifespan,
)


app.mount(
    "/terminal",
    StaticFiles(directory="app/platform/utils/terminal_test", html=True),
    name="terminal"
)

# -----------------------
# Error
# -----------------------
app.add_exception_handler(ApplicationError, semantic_error_handler)

# -----------------------
# Routers
# -----------------------
app.include_router(connect_router, prefix="/engine", tags=["Mainframe - Communication Engine"])
app.include_router(logon_router, prefix="/engine", tags=["Mainframe - Communication Engine"])
app.include_router(logoff_router, prefix="/engine", tags=["Mainframe - Communication Engine"])
app.include_router(disconnect_router, prefix="/engine", tags=["Mainframe - Communication Engine"])
app.include_router(status, prefix="/engine", tags=["Mainframe - Communication Engine"])
app.include_router(automation_router, prefix="/engine", tags=["Mainframe - Communication Engine"])
app.include_router(screen_update, prefix="/view", tags=["Screen View"])
app.include_router(api_key_route.router, prefix="/security", tags=["Security"])