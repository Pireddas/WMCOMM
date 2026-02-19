from app.infrastructure.lib3270.terminal_driver import TerminalDriver
from app.domains.engine.schema.logoff_schema import LogoffResponse

class LogoffService:
    def __init__(self, driver: TerminalDriver):
        # Agora o service RECEBE o terminal, ele não importa mais do arquivo lib3270
        self.driver = driver

    async def execute_logoff(self) -> LogoffResponse:
        # 1. SAIR DO ISPF (PF3 ou PF4 conforme sua regra)
        if self.driver.wait_for_ready(10) != 0:
            self.driver.keyboard_reset()
            self.driver.main_iterate(0) # Flush rápido

        self.driver.main_iterate(1)
        self.driver.wait_for_ready(10)
        tela = self.driver.get_screen_lines()
        for sc in tela:
            if "LOGON ===>" in sc.upper():
                final_state = self.driver.get_connection_state()
                
                return LogoffResponse(
                    status="Logoff efetuado com sucesso",
                    connection_state=final_state["id"],
                    steps=["PF3 enviado", "Comando LOGOFF injetado", "Enter processado"]
                )
        
        self.driver.send_pfkey(3)
        
        # 2. Aguarda o prompt READY do TSO
        self.driver.main_iterate(1)
        self.driver.wait_for_ready(10)
        
        # 3. TERCEIRO PASSO: "LOGOFF" definitivo
        # Usamos o método do driver que já encapsula a lógica técnica
        tela = self.driver.get_screen_lines()
        ln = " " * 80
        for i, scc in enumerate(tela):
            if ln in scc.upper():
                self.driver.set_string(((int(i))*80), "LOGOFF")
                self.driver.wait_for_ready(10)
                self.driver.send_enter()
                self.driver.main_iterate(1)
                self.driver.wait_for_ready(10)
                break

        
        # Captura o estado final para o log
        final_state = self.driver.get_connection_state()
        
        return LogoffResponse(
            status="Logoff efetuado com sucesso",
            connection_state=final_state["id"],
            steps=["PF3 enviado", "Comando LOGOFF injetado", "Enter processado"]
        )