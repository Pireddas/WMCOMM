import uvicorn
import sys
import os
from app.application.config import settings
# Adiciona a raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Importante: O formato "app.main:app" diz: 
    # "procure o arquivo main.py dentro da pasta app e pegue a instância 'app'"
    uvicorn.run("app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)

