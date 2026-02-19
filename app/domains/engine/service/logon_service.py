from app.infrastructure.lib3270.terminal_driver import TerminalDriver
from app.domains.engine.schema.logon_schema import LogonData, LogonResponse
from app.domains.engine.service.connection_service import ConnectionService

class LogonService:
    def __init__(self, driver: TerminalDriver):
        self.driver = driver

    async def execute_logon(self, data: LogonData) -> LogonResponse:
        # 1. Sincronismo Inicial (Usando o que aprendemos no wait_for_ready.c)
        # Se retornar EPERM (1), resetamos o teclado imediatamente

        if self.driver.wait_for_ready(10) != 0:
            self.driver.keyboard_reset()
            self.driver.main_iterate(0) # Flush rápido
            self.driver.send_enter() 
        
        # Aguarda o Mainframe processar o Enter inicial
        self.driver.wait_for_ready(10)
        
        # 2. Localização Dinâmica do Cursor
        tela = self.driver.get_screen_lines()
        lgn = False

        for sc in tela:
            if "LOGON" in sc.upper():
                lgn = True
                # Pega o endereço no exato momento da escrita
                addr_user = self.driver.get_cursor_address()
                self.driver.set_string(addr_user, data.user_id)
                self.driver.send_enter()
                
                # 3. Espera a tela de senha (com tratamento de erro de operador)
                if self.driver.wait_for_ready(10) != 0:
                    # Se travou, tenta forçar a saída (PF4 costuma ser cancel/refresh no BB)
                    self.driver.keyboard_reset()
                    self.driver.send_pfkey(4)
                    self.driver.wait_for_ready(5)
                
                # 4. Busca o campo de senha
                self.driver.main_iterate(1) # Garante que o buffer leu a tela de senha
                tela_senha = self.driver.get_screen_lines()
                
                for sc_pass in tela_senha:
                    if "ENTER CURRENT PASSWORD" in sc_pass.upper():
                        # Sincronismo total antes da senha (dado sensível)
                        addr_pass = self.driver.get_cursor_address()
                        self.driver.set_string(addr_pass, data.password)
                        self.driver.send_enter()
                        break

                # 5. Limpeza de Banners (Otimizada)
                # Em Mainframes, banners podem ser muitos. 
                # O wait_for_ready(10) aqui é o que garante que o '***' apareça.
                for _ in range(5): # Aumentei para 5, banners de aviso de feriado/segurança são longos
                    self.driver.wait_for_ready(5)
                    if "***" in self.driver.get_screen_text():
                        self.driver.send_enter()
                    else:
                        break
                
                # Sincronia Final antes de devolver a resposta
                self.driver.wait_for_ready(10)
                raw_state = self.driver.get_connection_state()
                
                return LogonResponse(
                    status="Logon processado",
                    final_cursor=self.driver.get_cursor_address(),
                    connection_state=raw_state["id"] if isinstance(raw_state, dict) else raw_state
                )

        if not lgn:
            return LogonResponse(error="Tela para logon não identificada.")
        
        linhas_validas = [l.strip() for l in tela if l.strip()]
        screen_dict = {f"line{i+1}": linha for i, linha in enumerate(linhas_validas)}
        return LogonResponse(error="Erro no processo de logon.", screen=screen_dict)