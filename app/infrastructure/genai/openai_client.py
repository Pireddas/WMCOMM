# app\infrastructure\genai\openai_client.py

from openai import OpenAI
from app.application.config import settings
from app.application.errors.semantic_error import ApplicationError

def get_openai_client():
    api_key=settings.OPENAI_API_KEY
    if not api_key:
        raise ApplicationError("NO_API_KEYS") 
    
    return OpenAI(api_key=api_key)
