# app\infrastructure\genai\gpt_gateway.py

from app.infrastructure.genai.openai_client import get_openai_client
from app.application.config import settings


class GPTGateway:

    def __init__(self):
        self.client = get_openai_client()
        self.model = settings.MODEL_NAME

    def execute_prompt(self, system_prompt: str, user_input: str):
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ]
        )

        return response.output_text
