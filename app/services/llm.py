from openai import OpenAI
from app.config import settings

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def generate(self, prompt):
        if not self.client:
            return "LLM API key is not configured. Add OPENAI_API_KEY to generate the final answer."
        response = self.client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.1,
            messages=[
                {"role": "system", "content": "Answer only from supplied context."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
