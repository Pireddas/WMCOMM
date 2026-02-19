from app.infrastructure.lib3270.terminal_driver import TerminalDriver
from app.domains.engine.schema.screen_update_schema import ScreenResponse

class ScreenService:
    def __init__(self, driver: TerminalDriver):
        self.driver = driver

    async def get_rendered_screen(self) -> ScreenResponse:
        # Usa o método protegido que já criamos no Driver
        tela = self.driver.get_screen_lines()
        str_html = ""
        
        for row_index, sc in enumerate(tela):
            sc_ = ""
            is_in_highlight_zone = False
            
            for col_index, char in enumerate(sc):
                addr = row_index * 80 + col_index
                # Pede o atributo ao driver
                real_attr = self.driver.get_field_attribute(addr)
                
                # Verifica se o campo é editável (Atributos 192/200)
                #is_editable = (real_attr in [192, 200])
                prev_attr = self.driver.get_field_attribute(addr - 1)

                is_editable = (
                    real_attr in [192, 200] and
                    prev_attr in [192, 200]
                )

                if is_editable:
                    if not is_in_highlight_zone:
                        sc_ += f"<span style='color: #ffffff;'>{char.replace(" ", ".")}"
                        is_in_highlight_zone = True
                    else:
                        sc_ += char.replace(" ", ".")
                else:
                    if is_in_highlight_zone:
                        sc_ += f"</span>{char}"
                        is_in_highlight_zone = False
                    else:
                        sc_ += char
            
            if is_in_highlight_zone:
                sc_ += "</span>"
            str_html += f"<pre>{sc_}</pre>"

        # Lógica do Cursor usando o Driver
        cursor_addr = self.driver.get_cursor_address()
        lin = (cursor_addr // 80) + 1
        pos = cursor_addr + 1
        col = pos - ((lin - 1) * 80)

        # Rodapé de Coordenadas
        espacamento = "<pre> </pre><pre>  [.] UNPROTECTED FIELDS                                           "
        if lin > 0:
            str_html += f"{espacamento}{lin:02d}/{col:02d} [P.{pos:04d}]</pre>"

        return ScreenResponse(screen=str_html)