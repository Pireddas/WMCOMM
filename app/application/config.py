# app/application/config.py

import os, json
from dotenv import load_dotenv
from typing import List

load_dotenv(override=False)

class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "Web Mainframe Communication (Engine)")
    VERSION = os.getenv("VERSION", "0.1.0")

    LANGUAGE = os.getenv("LANGUAGE", "EN")

    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT = int(os.getenv("APP_PORT", 8000))

    MF_HOST = os.getenv("MF_HOST", "tn3270://127.0.0.1")
    MF_PORT = int(os.getenv("MF_PORT", 3270))
    TN_MODEL = os.getenv("TN_MODEL", "3279-2-E")

    origins_raw = os.getenv("ALLOWED_ORIGINS", "*")
    if origins_raw == "*":
        ALLOWED_ORIGINS = ["*"]
    else:
        ALLOWED_ORIGINS = [o.strip() for o in origins_raw.split(",")]

    API_LOG_DIR = os.getenv(
            "API_LOG_DIR",
            "app/platform/observability/logs",
        )
    
    API_LOG_INFO = os.getenv("API_LOG_INFO", "api_access_info.log")
    API_LOG_DEBUG = os.getenv("API_LOG_DEBUG", "api_access_debug.log")
    API_LOG_WARNING = os.getenv("API_LOG_WARNING", "api_access_warning.log")
    API_LOG_ERROR = os.getenv("API_LOG_ERROR", "api_access_error.log")
    API_LOG_CRITICAL = os.getenv("API_LOG_CRITICAL", "api_access_critical.log")

    ASSET_CACHE_DIR = os.getenv("ASSET_CACHE_DIR", "app/infrastructure/cache")
    EXT_CACHE = os.getenv("EXT_CACHE", "parquet")
    COMPRESSION = os.getenv("COMPRESSION", "BROTLI")

    API_LOG = os.getenv(
        "API_LOG",
        "app/platform/observability/logs/api_access.log",
    )
    REL_LOG = os.getenv(
        "REL_LOG_API",
        "app/platform/observability/logs/performance_summary.json",
    )

    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    DB_DIR = os.getenv("DB_DIR", "app/infrastructure/db/sqlite")
    DB_PATH = os.getenv(
        "DB_PATH",
        f"{DB_DIR}/governance.db",
    )
    POSTGRES_URL = os.getenv("POSTGRES_URL")
    TBL_API_KEY = os.getenv("TBL_API_KEY", "api_keys_WMCOMM")
 
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    @staticmethod
    def _load_enabled_services() -> List[str]:
        raw = os.getenv("ENABLED_SERVICES")
        if not raw:
            return ["basic_metrics"]

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return [s.strip() for s in raw.split(",")]

    ENABLED_SERVICES: List[str] = _load_enabled_services()

    def is_service_enabled(self, service_name: str) -> bool:
        return service_name in self.ENABLED_SERVICES

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = "gpt-4.1-nano"

settings = Settings()
