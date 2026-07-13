import asyncio
import logging

from aiogram import Bot, Dispatcher

import database as db
from config import BOT_TOKEN
from handlers import router


async def main():
    logging.basicConfig(level=logging.INFO)

    await db.init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
