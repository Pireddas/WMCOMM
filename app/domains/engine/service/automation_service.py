# app/domains/engine/service/automation_service.py
from app.infrastructure.lib3270.terminal_driver import TerminalDriver
from app.domains.engine.schema.automation import AutomationSlice

class AutomationService:
    def __init__(self, driver: TerminalDriver):
        self.driver = driver

    async def execute_slice(self, data: AutomationSlice):
        # 1. Captura a tela atual para validação
        screen_text = self.driver.get_screen_text()

        # 2. Confirmação (Estou na tela certa para começar?)
        conf = data.confirmation
        current_title = screen_text[conf.pos_start-1:conf.pos_end+1].strip()

        if conf.text.upper().strip() not in current_title.upper().strip():
            return {"status": "error", "message": f"Tela inválida. Esperado: {conf.text}, Obtido: {current_title}"}

        # 3. Preenchimento de campos (Se existirem)
        if data.fields:
            for field in data.fields:
                erase=" " * int((field.pos_end - field.pos_start)+2)
                self.driver.set_string(field.pos_start-1, erase)
                self.driver.wait_for_ready(5)
                self.driver.set_string(field.pos_start-1, field.value)

        # frame atual
        self.driver.wait_for_ready(5)
        new_screen = self.driver.get_screen_text()
        err = data.msg_error
        f_err = new_screen[err.pos_start-1:err.pos_end+1]

        # 4. Envio do Comando
        if data.command:
            # Se for um comando de texto, digitamos. Se for tecla (PF1, ENTER), usamos a função específica.
            if data.command.upper() == "ENTER":
                self.driver.send_enter()
            elif data.command.upper().startswith("PF"):
                key_num = int(data.command.upper().replace("PF", ""))
                self.driver.send_pfkey(key_num)
            else:
                erase=" " * int((data.pos_end - data.pos_start)+2)
                self.driver.set_string(data.pos_start-1, erase)
                self.driver.wait_for_ready(5)
                self.driver.set_string(data.pos_start-1, data.command) # Seta na posição atual do cursor
                self.driver.send_enter()
                self.driver.main_iterate(1)

        # 5. Sincronização (Espera o Mainframe processar)
        self.driver.wait_for_ready(10)
        self.driver.main_iterate(1)
        # 6. Validação de Saída (Sucesso ou Erro?)
        new_screen = self.driver.get_screen_text()
        

        # Check de Erro prioritário
        err = data.msg_error
        conf = data.confirmation
        current_title = new_screen[conf.pos_start-1:conf.pos_end+1].strip()

        if (new_screen[err.pos_start-1:err.pos_end+1] != f_err) and (conf.text == current_title):
            return {"status": "mainframe_error", "message": new_screen[err.pos_start-1:err.pos_end+1].strip()}



        # Check de Sucesso
        succ = data.msg_success
        if succ.text.upper() in new_screen[succ.pos_start-1:succ.pos_end+1].upper():
            return {"status": "success", "message": "Fatia executada com sucesso."}

        return {"status": "unknown", "message": "Comando enviado, mas a tela resultante é inesperada."}