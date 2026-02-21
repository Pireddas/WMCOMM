from fastapi import HTTPException
import asyncio
from app.domains.engine.schema.disconnect_schema import DisconnectResponse
from app.infrastructure.lib3270.terminal_driver import TerminalDriver
from app.application.config import settings
 
def _get_disconnect_screen():
    """Gera a arte ASCII de encerramento."""
    PROJECT_NAME = settings.PROJECT_NAME
    VERSION = settings.VERSION
    
    lines = [
        "<pre>",
        "================================================================================",
        f"                  {PROJECT_NAME} - v{VERSION}                 ",
        "--------------------------------------------------------------------------------",
        "                                                                                ",
        "                         SESSION TERMINATED SUCCESSFULLY                        ",
        "                                                                                ",
        f"           Thank you for using the <u>{PROJECT_NAME}</u>         ",
        "                                                                                ",
        "                           Press Connect to continue...                         ",
        "                                                                                ",
        "    ........................................................................    ",
        "    .+...................................................................+..    ",
        "    ...............    .....    ...    .....    ...        ................    ",
        "    ..............  MM   .   MM  .  WW   .   WW  .  <b>CCCCCCC</b>  ...............    ",
        "    ..............  MMM  .  MMM  .  WW       WW  .  <b>CC   CC</b>  ...............    ",
        "    ..............  MMMM   MMMM  .  WW  WWW  WW  .  <b>CC</b>      ................    ",
        "    ..............  MM MM MM MM  .  WW WW WW WW  .  <b>CC</b>     .................    ",
        "    ..............  MM  MMM  MM  .  WWWW   WWWW  .  <b>CC</b>      ................    ",
        "    ..............  MM   .   MM  .  WWW  .  WWW  .  <b>CC   CC</b>  ...............    ",
        "    ..............  MM  ...  MM  .  WW  ...  WW  .  <b>CCCCCCC</b>  ...............    ",
        "    ................................                             ...........    ",
        "    .+.............................  <span style='color: #ffc400;'>Mainframe Web Communication</span>  ........+.    ",
        "    ........................................................................    ",
        "                                                                                ",
        "                                                                                ",
        "================================================================================",
        "                                                                 Ralf Piredda   ",
        "</pre>"
    ]
    
    while len(lines) < 24:
        lines.append("")
    return "\n".join(lines)

_disconnect_lock = asyncio.Lock()

class DisconnectService:
    def __init__(self, driver: TerminalDriver):
        self.driver = driver

    async def disconnect(self) -> DisconnectResponse:
        async with _disconnect_lock:
            # 1. Checagem de Sanidade: Já estou desconectado?
            state = self.driver.get_connection_state()
            state_id = state["id"] if isinstance(state, dict) else state
            if state_id < 5:
                return DisconnectResponse(
                    status="Logoff finalizado",
                    message="Sessão encerrada no TSO e conexão finalizada.",
                    screen=_get_disconnect_screen()
                )
            if self.driver.wait_for_ready(10) != 0:
                self.driver.keyboard_reset()
                self.driver.main_iterate(0) # Flush rápido

            self.driver.main_iterate(1)
            self.driver.wait_for_ready(10)
            tela = self.driver.get_screen_lines()
            for sc in tela:
                if "LOGON ===>" in sc.upper():
                    self.driver.disconnect()
                    return DisconnectResponse(
                        status="Logoff finalizado",
                        message="Sessão encerrada no TSO e conexão finalizada.",
                        screen=_get_disconnect_screen()
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

                
                # Encerra o socket na DLL (Importante para liberar licença no Host)
            self.driver.disconnect()
            
            return DisconnectResponse(
                status="Logoff finalizado",
                message="Sessão encerrada no TSO e conexão finalizada.",
                screen=_get_disconnect_screen()
            )