# app\platform\observability\err_logger\error_assembler.py
 
from app.platform.observability.err_logger.error_catalog import ErrorAssembler
from app.application.config import settings
from app.application.errors.semantic_error import ApplicationError

class Error():
    def error(request_id: str, error_key: str):
        try:
            code, description, name = getattr(ErrorAssembler, f"{error_key}_{settings.LANGUAGE}")
        except:
            raise ApplicationError("ERR_UNKNOWN_ERROR_KEY") # Sem erro genérico. Testes automatizados devem capturar qualquer falha de semântica.
        
        return {
            "ID": request_id,
            "Error": description,
            "Status": code
        }, name