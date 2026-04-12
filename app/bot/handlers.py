from aiogram import Router, types
from aiogram.filters import CommandStart

from app.services.rag import get_context
from app.services.llm import ask_gemini
from app.db.loader import search

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("👋 Cәлем! Мен BigData экожүйелері сабағы бойынша AI көмекшімін. Сұрақтарға лекциялардың негізінде жауап беремін! Қандай сұрағыңыз бар?")


@router.message()
async def handle(message: types.Message):

    question = message.text

    # 1. поиск
    texts, sources = search(question)

    context = "\n\n".join(texts)

    # 2. ответ от Gemini
    answer = ask_gemini(context, question)

    # 3. добавляем источники вручную
    unique_sources = list(set(sources))

    sources_text = "\n".join([f"📄 {s}" for s in unique_sources])

    final_answer = f"{answer}\n\n📚 Дереккөз:\n{sources_text}"

    await message.answer(final_answer, parse_mode="HTML")