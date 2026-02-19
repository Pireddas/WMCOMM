# app/domains/engine/service/status_service.py
from app.infrastructure.lib3270.terminal_driver import TerminalDriver
from app.domains.engine.schema.status_schema import StatusResponse, SessionStatus

class StatusService:
    def __init__(self, driver: TerminalDriver):
        self.driver = driver

    async def get_detailed_status(self) -> StatusResponse:
        # 1. Coleta dados brutos do Driver
        c_state = self.driver.get_connection_state()
        ready = self.driver.wait_for_ready(0) # 0 para não bloquear a API
        lock_status = self.driver.get_lock_status()
        addr = self.driver.get_cursor_address()
        
        # 2. Lógica de Identificação de Tela (Observabilidade)
        # Lemos as linhas para saber onde o robô está "pisando"
        screen_lines = self.driver.get_screen_lines()
        screen_text = "".join(screen_lines).upper()
        
        current_screen = "UNKNOWN"
        if "LOGON ===>" in screen_text:
            current_screen = "MAIN_LOGON_SCREEN"
        elif "OPTION ===>" in screen_text and "ISPF" in screen_text:
            current_screen = "ISPF_PRIMARY_MENU"
        elif "READY" in screen_text and any("LOGOFF" in line for line in screen_lines):
            current_screen = "TSO_PROMPT"
        elif "ENTER USERID" in screen_text:
            current_screen = "TSO_USERID_INPUT"

        # 3. Construção da Resposta
        return StatusResponse(
            status=SessionStatus(
                ready=ready,
                cursor_addr=addr,
                connection_id=c_state["id"],
                connection_name=c_state["name"],
                is_connected=c_state["id"] >= 5, # 5 = LIB3270_CONNECTED_INITIAL
                is_locked=lock_status != 0,
                current_screen=current_screen,
                active_url=self.driver.get_active_url()
            )
        )