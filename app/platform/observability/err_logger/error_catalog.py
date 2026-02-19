class ErrorAssembler:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    ############### PORTUGUÊS - BR ###############
    INV_PARAMS_PTBR = (400, "Parametros invalidos ou ausentes.", "api-governance-error-inv-params")
    INV_TICKERS_PTBR = (400, "Um ou mais tickers sao invalidos.", "api-governance-error-inv-tickers")
    INV_SDATE_PTBR = (400, "Either start_date or period must be provided", "api-governance-error-inv-sdate")
    INV_TICKER_PTBR = (400, "Invalid ticker.", "api-governance-error-inv-ticker")
    GENERIC_ERR_400_PTBR = (400, "Erro generico: ", "api-governance-generic-error")

    AUS_API_KEY_PTBR = (401, "Acesso negado: X-API-KEY ausente.", "api-governance-aus-key")
    
    INV_API_KEY_PTBR = (403, "Acesso negado: Chave invalida ou revogada.", "api-governance-inv-key")

    GENERIC_ERR_404_PTBR = (404, "Erro generico: ", "api-governance-generic-error")
    INV_HIST_PRICE_PTBR = (404, "Historico de precos muito curto para analise.", "api-governance-error-inv-hist-price")
    INV_CLOSE_COLUMNS_PTBR = (404, "Erro ao processar colunas de fechamento.", "api-governance-error-inv-close-columns")
    INV_INSUF_DATA_PTBR = (404, "Dados insuficientes para o intervalo selecionado.", "api-governance-error-insuf-data")
    NO_DATA_PTBR = (404, "Nenhum dado encontrado para os parametros fornecidos.", "api-governance-error-no-data")
    NO_API_KEYS_PTBR = (404, "Nenhuma chave API encontrada para o proprietario fornecido.", "api-governance-error-no-api-keys")

    SERVICE_MANUT_PTBR = (503, "Servico temporariamente em manutencao.", "api-governance-error-serv-manut")
    GENERIC_ERR_500_PTBR = (503, "Erro na autenticacao: ", "api-governance-generic-error")
    GENERIC_ERR_503_PTBR = (503, "Erro generico: ", "api-governance-generic-error")
    SERVICE_UNAV_PTBR = (503, "Erro interno: Servico nao disponivel.", "api-governance-error-serv-unav")

    ERR_CREATING_API_KEY_PTBR = (500, "Erro ao criar chave API.", "api-governance-error-creating-api-key")
    ERR_UPDATING_API_KEY_PTBR = (500, "Erro ao atualizar o status da chave API.", "api-governance-error-updating-api-key")
    ERR_UNKNOWN_ERROR_KEY_PTBR = (500, "Chave de erro desconhecida.", "api-governance-error-unknown-error-key")

    ############### ENGLISH ###############
    INV_PARAMS_EN = (400, "Invalid or missing parameters.", "api-governance-error-inv-params")
    INV_TICKERS_EN = (400, "One or more tickers are invalid.", "api-governance-error-inv-tickers")
    INV_SDATE_EN = (400, "Either start_date or period must be provided.", "api-governance-error-inv-sdate")
    INV_TICKER_EN = (400, "Invalid ticker.", "api-governance-error-inv-ticker")
    GENERIC_ERR_400_EN = (400, "Generic error: ", "api-governance-generic-error")

    AUS_API_KEY_EN = (401, "Access denied: Missing X-API-KEY.", "api-governance-aus-key")
    
    INV_API_KEY_EN = (403, "Access denied: Invalid or revoked key.", "api-governance-inv-key")

    GENERIC_ERR_404_EN = (404, "Generic error: ", "api-governance-generic-error")
    INV_HIST_PRICE_EN = (404, "Price history too short for analysis.", "api-governance-error-inv-hist-price")
    INV_CLOSE_COLUMNS_EN = (404, "Error processing closing price columns.", "api-governance-error-inv-close-columns")
    INV_INSUF_DATA_EN = (404, "Insufficient data for the selected interval.", "api-governance-error-insuf-data")
    NO_DATA_EN = (404, "No data found for the provided parameters.", "api-governance-error-no-data")
    NO_API_KEYS_EN = (404, "No API key found for the given owner.", "api-governance-error-no-api-keys")

    SERVICE_MANUT_EN = (503, "Service temporarily under maintenance.", "api-governance-error-serv-manut")
    GENERIC_ERR_500_EN = (503, "Authentication error: ", "api-governance-generic-error")
    GENERIC_ERR_503_EN = (503, "Generic error: ", "api-governance-generic-error")
    SERVICE_UNAV_EN = (503, "Internal error: Service unavailable.", "api-governance-error-serv-unav")

    ERR_CREATING_API_KEY_EN = (500, "Error creating API key.", "api-governance-error-creating-api-key")
    ERR_UPDATING_API_KEY_EN = (500, "Error updating API key status.", "api-governance-error-updating-api-key")
    ERR_UNKNOWN_ERROR_KEY_EN = (500, "Unknown error key.", "api-governance-error-unknown-error-key")
    
    ############### ESPAÑOL ###############
    INV_PARAMS_ES = (400, "Parametros invalidos o faltantes.", "api-governance-error-inv-params")
    INV_TICKERS_ES = (400, "Uno o mas tickers son invalidos.", "api-governance-error-inv-tickers")
    INV_SDATE_ES = (400, "Se debe proporcionar start_date o period.", "api-governance-error-inv-sdate")
    INV_TICKER_ES = (400, "Ticker invalido.", "api-governance-error-inv-ticker")
    GENERIC_ERR_400_ES = (400, "Error generico: ", "api-governance-generic-error")

    AUS_API_KEY_ES = (401, "Acceso denegado: X-API-KEY ausente.", "api-governance-aus-key")
    
    INV_API_KEY_ES = (403, "Acceso denegado: Clave inválida o revocada.", "api-governance-inv-key")

    GENERIC_ERR_404_ES = (404, "Error generico: ", "api-governance-generic-error")
    INV_HIST_PRICE_ES = (404, "Historial de precios demasiado corto para el analisis.", "api-governance-error-inv-hist-price")
    INV_CLOSE_COLUMNS_ES = (404, "Error al procesar las columnas de cierre.", "api-governance-error-inv-close-columns")
    INV_INSUF_DATA_ES = (404, "Datos insuficientes para el intervalo seleccionado.", "api-governance-error-insuf-data")
    NO_DATA_ES = (404, "No se encontraron datos para los parametros proporcionados.", "api-governance-error-no-data")
    NO_API_KEYS_ES = (404, "No se encontro ninguna clave API para el propietario proporcionado.", "api-governance-error-no-api-keys")

    SERVICE_MANUT_ES = (503, "Servicio temporalmente en mantenimiento.", "api-governance-error-serv-manut")
    GENERIC_ERR_500_ES = (503, "Error de autenticación: ", "api-governance-generic-error")
    GENERIC_ERR_503_ES = (503, "Error genérico: ", "api-governance-generic-error")
    SERVICE_UNAV_ES = (503, "Error interno: Servicio no disponible.", "api-governance-error-serv-unav")

    ERR_CREATING_API_KEY_ES = (500, "Error al crear la clave API.", "api-governance-error-creating-api-key")
    ERR_UPDATING_API_KEY_ES = (500, "Error al actualizar el estado de la clave API.", "api-governance-error-updating-api-key")
    ERR_UNKNOWN_ERROR_KEY_ES = (500, "Clave de error desconocida.", "api-governance-error-unknown-error-key")