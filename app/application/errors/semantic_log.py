# app\application\errors\semantic_error.py

class ApplicationLog(Exception):
    def __init__(self, code: str, context: dict | None = None):
        self.code = code
        self.context = context or {}
        super().__init__(code)
