import asyncio
import logging
import time
import tracemalloc

from aiogram import Bot
from DATA_BASE import db

from LOGIC import config
from LOGIC.handlers import dp

db_process = db.options_db()
tracemalloc.start()

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    db_process.start_scheduler()
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print(f'Ошибка: {e}')
            time.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())