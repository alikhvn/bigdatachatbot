import asyncio
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

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    loader = await message.answer(
        "⏳ Іздеп жатырмын..."
    )

    question = message.text

    texts, sources = await asyncio.to_thread(search, question)
    context = "\n\n".join(texts)

    answer, tokens = await asyncio.to_thread(ask_gemini, context, question)

    unique_sources = list(set(sources))
    sources_text = "\n".join([f"📄 {s}" for s in unique_sources])

    final_answer = (
        f"{answer}\n\n"
        f"📚 <b>Дереккөз:</b>\n{sources_text}\n\n"
        f"🤖 <i>Токенов использовано: {tokens}</i>"
    )

    await loader.edit_text(final_answer, parse_mode="HTML")