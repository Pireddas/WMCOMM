# app\infrastructure\lib3270\lib3270.py

import ctypes
import os

# --- SETUP DLL (Singleton ou Global para a Infra) ---
DLL_PATH = r"D:\msys64\mingw64\bin\lib3270.dll"
os.add_dll_directory(os.path.dirname(DLL_PATH))
lib = ctypes.windll.LoadLibrary(DLL_PATH)

# --- CONFIGURAÇÃO DE TIPOS (ESSENCIAL PARA 64-BIT) ---

lib.lib3270_get_field_attribute.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.lib3270_get_field_attribute.restype = ctypes.c_int

# Sessão e Conexão
lib.lib3270_session_new.argtypes = [ctypes.c_char_p]
lib.lib3270_session_new.restype = ctypes.c_void_p
lib.lib3270_set_url.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.lib3270_reconnect.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.lib3270_disconnect.argtypes = [ctypes.c_void_p]
lib.lib3270_is_connected.argtypes = [ctypes.c_void_p]
lib.lib3270_is_connected.restype = ctypes.c_bool

# Estados e Nomes
lib.lib3270_get_connection_state.argtypes = [ctypes.c_void_p]
lib.lib3270_get_connection_state.restype = ctypes.c_int
lib.lib3270_connection_state_get_name.argtypes = [ctypes.c_int]
lib.lib3270_connection_state_get_name.restype = ctypes.c_char_p
lib.lib3270_get_lock_status.argtypes = [ctypes.c_void_p]
lib.lib3270_get_lock_status.restype = ctypes.c_int
lib.lib3270_get_url.argtypes = [ctypes.c_void_p]
lib.lib3270_get_url.restype = ctypes.c_char_p

# Retorna a URL atual (Ex: tn3270://127.0.0.1:3270)
lib.lib3270_get_url.argtypes = [ctypes.c_void_p]
lib.lib3270_get_url.restype = ctypes.c_char_p

# Retorna o nome do modelo do terminal (Ex: "3279-2-E")
lib.lib3270_get_model_name.argtypes = [ctypes.c_void_p]
lib.lib3270_get_model_name.restype = ctypes.c_char_p

# Retorna o tipo de host configurado
lib.lib3270_get_host_type_name.argtypes = [ctypes.c_void_p]
lib.lib3270_get_host_type_name.restype = ctypes.c_char_p

# Interação e Teclado
lib.lib3270_main_iterate.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.lib3270_kybdreset.argtypes = [ctypes.c_void_p]
lib.lib3270_enter.argtypes = [ctypes.c_void_p]
lib.lib3270_set_string_at_address.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]
# No seu arquivo de mapeamento da DLL (app/infrastructure/lib3270/lib3270.py)
lib.lib3270_set_string.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.lib3270_set_string.restype = ctypes.c_int

lib.lib3270_get_cursor_address.argtypes = [ctypes.c_void_p]
lib.lib3270_get_cursor_address.restype = ctypes.c_int

# AS MARAVILHOSAS (Funções de Espera Nativa)
lib.lib3270_wait_for_ready.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.lib3270_wait_for_ready.restype = ctypes.c_int
lib.lib3270_wait_for_cstate.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
lib.lib3270_wait_for_cstate.restype = ctypes.c_int
lib.lib3270_wait_for_keyboard_unlock.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.lib3270_wait_for_keyboard_unlock.restype = ctypes.c_int

# lib3270_pfkey(H3270 *h, int key_number)
lib.lib3270_pfkey.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.lib3270_pfkey.restype = ctypes.c_int


# lib3270_erase(H3270 *h) - Equivale à tecla CLEAR do terminal
lib.lib3270_erase.argtypes = [ctypes.c_void_p]
lib.lib3270_erase.restype = ctypes.c_int


# Conteúdo da Tela
lib.lib3270_get_contents.argtypes = [
    ctypes.c_void_p, ctypes.c_int, ctypes.c_int, 
    ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ushort)
]

# Instância da sessão para o ciclo de vida da infra
h_session = lib.lib3270_session_new(b"3279-2-E")