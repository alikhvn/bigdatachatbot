import asyncio
from aiogram import Bot, Dispatcher
from app.config.settings import BOT_TOKEN
from app.bot.handlers import router


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())