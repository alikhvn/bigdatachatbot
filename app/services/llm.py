from google.genai import Client
from app.config.settings import GEMINI_API_KEY

client = Client(api_key=GEMINI_API_KEY)


def ask_gemini(context: str, question: str):
    prompt = f"""
Отвечай только по контексту и используя HTML теги: <b>жирный</b>, <i>курсив</i>.
Если нет информации — скажи "Бұл сұрақ лекцияда қарастырылмаған".

КОНТЕКСТ:
{context}

ВОПРОС:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # Получаем количество токенов из метаданных
    tokens = response.usage_metadata.total_token_count if response.usage_metadata else 0

    return response.text, tokens