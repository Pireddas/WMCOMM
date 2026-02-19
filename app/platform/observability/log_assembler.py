# app\platform\observability\err_logger\error_assembler.py
 
from app.platform.observability.log_metadata.metadata import LogAssembler
from app.platform.observability.logger import FastLog

class Log():
    def __init__(self, service_name: str, params=None, request_id: str = None):
        self.service_name = service_name
        self.params = params
        self.request_id = request_id

    def info(self):
        try:
            result = LogAssembler.info(self.service_name, self.request_id, self.params)
            FastLog.write_info(name="api-governance-info", message=result)
        except AttributeError:
            raise ValueError(f"Erro")
        
    def debug(self):
        try:
            result = LogAssembler.debug(self.service_name, self.request_id, self.params)
            FastLog.write_debug(name="api-governance-debug", message=result)
        except AttributeError:
            raise ValueError(f"Erro")
