from fastapi import HTTPException
from app.infrastructure.lib3270.terminal_driver import TerminalDriver
from app.domains.engine.schema.connection_schema import ConnectionRequest, ConnectionResponse

class ConnectionService:
    def __init__(self, driver: TerminalDriver):
        self.driver = driver

    async def connect(self, data: ConnectionRequest) -> ConnectionResponse:
        try:
            # Limpa espaços em branco da URL que podem travar a DLL
            host = data.host.strip()
            self.driver.set_url(host)
            self.driver.reconnect()
            
            # Garante que a DLL processe o início do socket
            self.driver.main_iterate(0)

            # Espera o estado 5 (CONNECTED) por 10 segundos
            self.driver.wait_for_cstate(5, 10) 
            
            # Sincronização final
            self.driver.wait_for_ready(5)
            
            state = self.driver.get_connection_state()
            
            return ConnectionResponse(
                status="Conectado" if state["id"] >= 5 else "Falha na conexão",
                state_id=state["id"],
                state_name=state["name"],
                lock_status=self.driver.get_lock_status(),
                handle=str(self.driver.handle),
                url=self.driver.get_active_url()
            )
        except Exception as e:
            # Aqui você pode capturar se o erro foi ENOTCONN (Sem conexão)
            raise HTTPException(status_code=500, detail=f"Erro na conexão Mainframe: {str(e)}")