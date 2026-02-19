import ctypes, os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

# --- SETUP DLL ---
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

# --- INSTÂNCIA GLOBAL ---
# Criamos a sessão uma única vez no início do módulo
h_session = lib.lib3270_session_new(b"3279-2-E")

# --- LIFESPAN ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando API e preparando ambiente 3270...")
    yield
    print("Encerrando: Desconectando sessão 3270...")
    if h_session and lib.lib3270_is_connected(h_session):
        lib.lib3270_disconnect(h_session)
        lib.lib3270_main_iterate(h_session, 0)
    print("Sessão encerrada limpamente.")

app = FastAPI(lifespan=lifespan)

# --- MODELS ---
class LogonData(BaseModel):
    user_id: str
    password: str

class CommandData(BaseModel):
    command: str # Str ou PFKEY|Num da PF
    address: int = None  # Se for None, ele usa a posição atual do cursor

class InputData(BaseModel):
    field_id: str  # Ex: "CP1"
    value: str     # Ex: "1"

# --- ROTAS ---
@app.post("/connect")
async def connect():
    # Define a URL e tenta reconectar
    lib.lib3270_set_url(h_session, b"tn3270://127.0.0.1:3270")
    lib.lib3270_reconnect(h_session, 0)
    
    # 1. Espera nativa pelo estado de conectado (6 = CONNECTED_3270) por até 5 seg
    lib.lib3270_wait_for_cstate(h_session, 6, 5)
    
    # 2. Se o teclado estiver bloqueado (comum em reloads), limpa o erro
    if lib.lib3270_get_lock_status(h_session) != 0:
        lib.lib3270_kybdreset(h_session)
        lib.lib3270_enter(h_session) # Força o host a redesenhar a tela
    
    # 3. Espera o terminal ficar pronto para receber dados
    lib.lib3270_wait_for_ready(h_session, 5)
    
    c_state = lib.lib3270_get_connection_state(h_session)
    state_name = lib.lib3270_connection_state_get_name(c_state).decode('utf-8')
    
    return {
        "status": "Conectado" if c_state >= 6 else "Em progresso",
        "state_id": c_state,
        "state_name": state_name,
        "lock_status": lib.lib3270_get_lock_status(h_session),
        "handle": h_session
    }

@app.get("/status")
async def status():
    lib.lib3270_main_iterate(h_session, 0)
    
    # Estados numéricos e nomes
    cstate_id = lib.lib3270_get_connection_state(h_session)
    cstate_name = lib.lib3270_connection_state_get_name(cstate_id).decode('utf-8')
    
    # Informações de Host e Modelo
    current_url = lib.lib3270_get_url(h_session)
    host_type_name = lib.lib3270_get_host_type_name(h_session)
    model_name = lib.lib3270_get_model_name(h_session)
    
    return {
        "is_connected": cstate_id >= 5,
        "connection": {
            "url": current_url.decode('utf-8') if current_url else "Nenhum",
            "state": cstate_name,
            "server_type_name": host_type_name.decode('utf-8') if host_type_name else "Desconhecido",
            "terminal_model": model_name.decode('utf-8') if model_name else "Desconhecido"
        },
        "session_id": h_session
    }

@app.get("/map")
async def get_map():
    lib.lib3270_main_iterate(h_session, 1) 
    for _ in range(3):
        lib.lib3270_main_iterate(h_session, 0)
       
    tamanho = 1920
    chars = (ctypes.c_ubyte * tamanho)()
    attrs = (ctypes.c_ushort * tamanho)()
    lib.lib3270_get_contents(h_session, 0, tamanho - 1, chars, attrs)
    
    fields = {}
    current_field = None
    field_count = 0

    mapa_visual=""
    for addr in range(tamanho):
            real_attr = lib.lib3270_get_field_attribute(h_session, addr)
            mapa_visual = f"{mapa_visual}, {str(real_attr)}"

            is_editable = (real_attr in [192, 200])
            if is_editable:
                if current_field is None:
                    start_= addr + 2
                    field_count += 1
                    current_field = {
                        "start": addr + 2,
                        "row_start": (addr // 80) + 1,
                        "col_start": (addr % 80) + 2,
                        "attr_type": real_attr
                    }
            else:
                if current_field is not None:
                    end_addr = addr - 1
                    current_field.update({
                        "end": end_addr + 1,
                        "row_end": (end_addr // 80) + 1,
                        "col_end": (end_addr % 80) + 1,
                        "length": (addr - 1) - (start_) + 2
                    })
                    fields[f"CP{field_count}"] = current_field
                    current_field = None

    # print(real_attr) # <=== Identificar campos no terminal quando necessário (192, 200 ...)

    # Caso o campo termine exatamente no último byte da tela (1919)
    if current_field is not None:
        end_addr = 1919
        current_field.update({
            "end": end_addr,
            "row_end": 24, "col_end": 80,
            "length": end_addr - current_field["start"] + 1
        })
        fields[f"CP{field_count}"] = current_field

    # Formatação da tela para visualização
    screen_rows = ["".join([chr(b) if 32 <= b <= 126 else " " for b in chars[i:i+80]]) for i in range(0, 1920, 80)]

    return {
        "state": lib.lib3270_get_connection_state(h_session),
        "fields": fields,
        "screen": screen_rows
    }

@app.post("/logon/step1")
async def logon_step1(data: LogonData):
    # 1. Primeira tentativa de esperar o terminal
    rc = lib.lib3270_wait_for_ready(h_session, 5)
    
    if rc != 0:
        print("Terminal travado ou sem campos. Iniciando sequência de destravamento...")
        
        # Sequência 'Power Flush': Reset -> Erase (Clear) -> Main Iterate
        lib.lib3270_kybdreset(h_session)
        lib.lib3270_erase(h_session)
        lib.lib3270_main_iterate(h_session, 1)
        
        # Dá um Enter para pedir a tela de novo
        lib.lib3270_enter(h_session)
        lib.lib3270_main_iterate(h_session, 1)

        # Agora checamos se o campo apareceu
        if lib.lib3270_wait_for_ready(h_session, 5) != 0:
            return {"error": "Terminal continua sem campos após Erase/Enter", "cursor": lib.lib3270_get_cursor_address(h_session)}

    # Se chegou aqui, temos um cursor e um campo
    addr_user = lib.lib3270_get_cursor_address(h_session)
    
    # Se o endereço for 0 ou 1, ainda estamos sem campo real
    if addr_user < 80: 
        print("Atenção: Cursor em posição suspeita, PF5 para forçar campos")
        lib.lib3270_pfkey(h_session, 4)
        lib.lib3270_main_iterate(h_session, 1)
        addr_user = lib.lib3270_get_cursor_address(h_session)
        lib.lib3270_enter(h_session)
        lib.lib3270_main_iterate(h_session, 1)

    mapa_atual = await get_map() 
    tela = mapa_atual["screen"]
    for sc in tela:
        if "LOGON" in sc.upper():
            # Injeta os dados
            lib.lib3270_set_string_at_address(h_session, addr_user, data.user_id.encode('ascii'))
            lib.lib3270_enter(h_session)

            # 3. Aguarda a tela de senha aparecer
            # Se o wait_for_ready falhar, F5
            if lib.lib3270_wait_for_ready(h_session, 5) != 0:
                print("Timeout detectado. Tentando destravar com F5...")
                lib.lib3270_pfkey(h_session, 4)
                lib.lib3270_main_iterate(h_session, 1)
                
                # Tenta o ready de novo
                lib.lib3270_enter(h_session)
                lib.lib3270_main_iterate(h_session, 1)
                lib.lib3270_pfkey(h_session, 4)
                lib.lib3270_main_iterate(h_session, 1)
                lib.lib3270_enter(h_session)
                if lib.lib3270_wait_for_ready(h_session, 3) != 0:
                    return {"error": "Mesmo com F5 o terminal não respondeu"}
                
            mapa_atual = await get_map() 
            tela = mapa_atual["screen"]
            for sc in tela:
                if "ENTER CURRENT PASSWORD" in sc.upper():
                    # 4. Injeta a senha e dá o ENTER final
                    addr_pass = lib.lib3270_get_cursor_address(h_session)
                    lib.lib3270_set_string_at_address(h_session, addr_pass, data.password.encode('ascii'))
                    lib.lib3270_enter(h_session)

                    # 5. Sincronismo final para garantir que o "/map" pegue a tela de "LOGGED ON"
                    lib.lib3270_wait_for_ready(h_session, 5)
                    lib.lib3270_main_iterate(h_session, 1)

                    # 5. Loop para "Limpar" as telas de boas-vindas (os ***)
                    for _ in range(3):
                        lib.lib3270_wait_for_ready(h_session, 2)

                        tamanho = 1920
                        chars = (ctypes.c_ubyte * tamanho)()
                        attrs = (ctypes.c_ushort * tamanho)()

                        lib.lib3270_get_contents(h_session, 0, tamanho - 1, chars, attrs)
                        screen_text = "".join([chr(b) for b in chars])

                        if "***" in screen_text:
                            lib.lib3270_enter(h_session)
                        else:
                            break

                    # Sincronismo final
                    lib.lib3270_wait_for_ready(h_session, 3)

                    return {
                        "status": "Logon processado",
                        "final_cursor": lib.lib3270_get_cursor_address(h_session),
                        "connection_state": lib.lib3270_get_connection_state(h_session)
                    }
    mapa_atual = await get_map() 
    tela = mapa_atual["screen"]
    linhas_validas = [sc for sc in tela if sc.strip()]

    response = {
        "error": "Tela para logon não identificada."
    }

    if linhas_validas:
        response["screen"] = {
            f"line{i+1}": linha
            for i, linha in enumerate(linhas_validas)
        }

    return response

@app.post("/command")
async def send_command(data: CommandData):
    # 1. VERIFICAÇÃO DE PRONTIDÃO
    if lib.lib3270_get_lock_status(h_session) != 0:
        lib.lib3270_kybdreset(h_session)
        lib.lib3270_main_iterate(h_session, 1)

    # 2. ESPERA O BUFFER SINCRONIZAR - Esperamos até 3 segundos para o terminal aceitar entrada
    lib.lib3270_wait_for_ready(h_session, 3)

    # 3. DEFINE O ENDEREÇO DE ESCRITA
    pos_addr = int(data.address) - 1
    target_addr = pos_addr if data.address is not 0 else lib.lib3270_get_cursor_address(h_session)

    # 4. ENVIA O TEXTO - Convertemos para ASCII.
    if "PFKEY|" in data.command.upper():
        lib.lib3270_pfkey(h_session, int(data.command[6:]))
    else:
        lib.lib3270_set_string_at_address(h_session, target_addr, data.command.upper().encode('ascii'))
    
    # 5. PRESSIONA ENTER - O comando só é processado pelo Host após o sinal de AID (Enter)
    lib.lib3270_enter(h_session)
    lib.lib3270_main_iterate(h_session, 1)

    # 6. SINCRONISMO PÓS-COMANDO - Mainframe processa e devolve a nova tela
    lib.lib3270_wait_for_ready(h_session, 5)
    lib.lib3270_main_iterate(h_session, 1)

    return {
        "status": "Comando enviado",
        "comando": data.command.upper(),
        "posicao_usada": target_addr,
        "novo_cursor": lib.lib3270_get_cursor_address(h_session),
        "lock_status": lib.lib3270_get_lock_status(h_session)
    }

@app.post("/input")
async def set_field_value(data: InputData):
    # 1. Obter o mapa atual (você pode extrair a lógica do get_map para uma função interna)
    mapa_atual = await get_map() 
    fields = mapa_atual["fields"]
    
    if data.field_id not in fields:
        return {"error": f"Campo {data.field_id} não encontrado na tela atual"}
    
    # 2. Pegar metadados do campo
    target_addr = fields[data.field_id]["start"]
    max_len = fields[data.field_id]["length"]
    
    # 3. Tratar a string (Padding)
    # .ljust(max_len) preenche com espaços à direita até atingir o tamanho exato
    val_raw = data.value.upper()
    if len(val_raw) > max_len:
        # Opcional: truncar se o usuário mandar algo maior que o campo
        val_raw = val_raw[:max_len]
    
    padded_value = val_raw.ljust(max_len)
    
    # 4. Enviar para o terminal
    lib.lib3270_set_string_at_address(
        h_session, 
        target_addr, 
        padded_value.encode('ascii')
    )
    
    # 5. Executar
    lib.lib3270_enter(h_session)
    lib.lib3270_wait_for_ready(h_session, 5)
    
    return {
        "status": "Sucesso",
        "campo": data.field_id,
        "valor_enviado": f"'{padded_value}'",
        "tamanho_campo": max_len
    }

@app.post("/logoff")
async def logoff():
    # 1. SAIR DO ISPF (O F4 que você mencionou ou F3 repetido)
    # No menu principal do ISPF, o F4 costuma ser o atalho de saída/cancel
    lib.lib3270_pfkey(h_session, 4)
    lib.lib3270_wait_for_ready(h_session, 5)
    
    # 2. SEGUNDO PASSO: "END" + ENTER
    # Se o F4 te deixou em uma tela de confirmação, o "END" garante a saída
    addr = lib.lib3270_get_cursor_address(h_session)
    lib.lib3270_set_string_at_address(h_session, addr, b"END")
    lib.lib3270_enter(h_session)
    
    # Aguarda o prompt READY do TSO aparecer
    lib.lib3270_wait_for_ready(h_session, 3)
    
    # 3. TERCEIRO PASSO: "LOGOFF" + ENTER
    # Agora sim, o comando definitivo para o TSO liberar o seu terminal
    addr_ready = lib.lib3270_get_cursor_address(h_session)
    lib.lib3270_set_string_at_address(h_session, addr_ready, b"LOGOFF")
    lib.lib3270_enter(h_session)
    
    # 4. SINCRONISMO FINAL
    # Esperamos o host processar o logoff antes de realmente fechar o socket
    lib.lib3270_wait_for_cstate(h_session, 5, 2) 
    
    # Agora sim, desconexão física
    #lib.lib3270_disconnect(h_session)
    
    return {
        "status": "Logoff efetuado com sucesso",
        "steps": ["F4 (PFK4) enviado", "END enviado", "LOGOFF enviado"]
    }

@app.post("/disconnect")
async def logoff():
    # 1. Garantir que o teclado não está travado
    lib.lib3270_wait_for_ready(h_session, 2)
    
    # 2. Sair do ISPF (Envia 'X' na linha de comando e ENTER)
    # A linha de comando do ISPF geralmente está no endereço 80 + 9 = 89
    # Mas para ser seguro, usamos o cursor atual se ele estiver no local certo
    lib.lib3270_set_string_at_address(h_session, 89, b"X")
    lib.lib3270_enter(h_session)
    
    # Espera a tela de "READY" do TSO aparecer
    lib.lib3270_wait_for_ready(h_session, 3)
    
    # 3. Envia o comando LOGOFF para o TSO
    # No prompt READY, o cursor costuma estar no início da linha
    addr = lib.lib3270_get_cursor_address(h_session)
    lib.lib3270_set_string_at_address(h_session, addr, b"LOGOFF")
    lib.lib3270_enter(h_session)
    
    # 4. Aguarda o Host encerrar a sessão TSO e voltar para a tela de abertura
    lib.lib3270_wait_for_cstate(h_session, 5, 3) # Espera voltar para LINE_MODE ou similar
    
    # 5. Desconexão Física da DLL
    lib.lib3270_disconnect(h_session)
    
    return {
        "status": "Logoff finalizado",
        "message": "Sessão encerrada no TSO e conexão finalizada."
    }