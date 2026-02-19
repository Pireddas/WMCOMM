# app\infrastructure\lib3270\terminal_driver.py

import ctypes
from app.infrastructure.lib3270.lib3270 import lib, h_session

class TerminalDriver:
    def __init__(self):
        self.lib = lib
        self.handle = h_session

    # --- Navegação e Teclado ---
    def wait_for_ready(self, timeout: int = 5):
        return self.lib.lib3270_wait_for_ready(self.handle, timeout)

    def keyboard_reset(self):
        self.lib.lib3270_kybdreset(self.handle)

    def erase_screen(self):
        self.lib.lib3270_erase(self.handle)

    def main_iterate(self, wait: int = 1):
        self.lib.lib3270_main_iterate(self.handle, wait)

    def send_enter(self):
        self.lib.lib3270_enter(self.handle)

    def send_pfkey(self, key: int):
        self.lib.lib3270_pfkey(self.handle, key)

    # --- Dados e Cursor ---
    def get_cursor_address(self) -> int:
        return self.lib.lib3270_get_cursor_address(self.handle)

    def set_string(self, address: int = 0, text: str = None):
        if isinstance(text, str):
            text = text.encode('ascii')
        self.lib.lib3270_set_string_at_address(self.handle, address, text)

    def set_string_(self, text: str = None):
        if isinstance(text, str):
            text = text.encode('ascii')
        return self.lib.lib3270_set_string(self.handle, text)

    def get_connection_state(self) -> int:
        return self.lib.lib3270_get_connection_state(self.handle)

    # --- Leitura de Tela (Protegida) ---
    def get_screen_text(self) -> str:
        tamanho = 1920
        chars = (ctypes.c_ubyte * tamanho)()
        attrs = (ctypes.c_ushort * tamanho)()
        self.lib.lib3270_get_contents(self.handle, 0, tamanho - 1, chars, attrs)
        
        # Converte substituindo nulos por espaços para evitar quebra de string
        return "".join([chr(b) if b != 0 else " " for b in chars])

    def is_field_protected(self, address: int) -> bool: 
        """Verifica se o campo onde você vai escrever é protegido (evita erro de teclado)."""
        attr = self.lib.lib3270_get_field_attribute(self.handle, address)
        # Na 3270, o bit 0x20 indica campo protegido
        return bool(attr & 0x20)

    def get_screen_lines(self):
        text = self.get_screen_text()
        return [text[i:i+80] for i in range(0, 1920, 80)]

    def set_url(self, url: str):
        self.lib.lib3270_set_url(self.handle, url.encode('utf-8'))

    def reconnect(self):
        self.lib.lib3270_reconnect(self.handle, 0)

    def wait_for_cstate(self, state: int, timeout: int):
        return self.lib.lib3270_wait_for_cstate(self.handle, state, timeout)

    def is_locked(self) -> bool:
        return self.lib.lib3270_get_lock_status(self.handle) != 0

    def reset_keyboard(self):
        self.lib.lib3270_kybdreset(self.handle)

    def send_enter(self):
        self.lib.lib3270_enter(self.handle)

    def get_connection_state(self):
        c_state = self.lib.lib3270_get_connection_state(self.handle)
        name = self.lib.lib3270_connection_state_get_name(c_state).decode('utf-8')
        return {"id": c_state, "name": name}

    def get_active_url(self) -> str:
        url_ptr = self.lib.lib3270_get_url(self.handle)
        if url_ptr is None:
            return "" # Retorna string vazia se for None
        
        # Se o retorno for bytes, decodifica. Se já for string (ctypes as_parameter), retorna.
        try:
            return url_ptr.decode('utf-8')
        except (AttributeError, UnicodeDecodeError):
            return str(url_ptr)
    
    def get_lock_status(self):
        return self.lib.lib3270_get_lock_status(self.handle)
    
    def disconnect(self):
        """Corta o vínculo com o host imediatamente."""
        self.lib.lib3270_disconnect(self.handle)

    def get_field_attribute(self, address: int) -> int:
        """Retorna o atributo do campo em um endereço específico."""
        return self.lib.lib3270_get_field_attribute(self.handle, address)
       
    # No terminal_driver.py
    def send_erase_eof(self):
        """Apaga o conteúdo do campo do cursor até o final."""
        try:
            # Tenta a função direta da DLL
            return self.lib.lib3270_erase_eof(self.handle)
        except AttributeError:
            # Se não existir, podemos tentar enviar o comando de tecla (Key 0x19)
            # Ou simplesmente pular este passo se a DLL for muito antiga
            print("Aviso: lib3270_erase_eof não encontrada na DLL.")
            return -1
        
    def get_oia_status(self) -> str:
            """Retorna a string de status da OIA (ex: 'X SYSTEM', 'READY', 'X CLOCK')."""
            try:
                return self.lib.lib3270_get_oia_status_message(self.handle).decode('utf-8')
            except:
                return "UNKNOWN"