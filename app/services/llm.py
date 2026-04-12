import google.generativeai as genai
from app.config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(context: str, question: str):
    prompt = f"""
Отвечай только по контексту и используя HTML теги: <b>жирный</b>, <i>курсив</i>.
Если нет информации — скажи "Бұл сұрақ лекцияда қарастырылмаған".

КОНТЕКСТ:
{context}

ВОПРОС:
{question}
"""
    response = model.generate_content(prompt)
    return response.text