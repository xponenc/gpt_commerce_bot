import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from handlers.handler_memory import memory_router
from handlers.handlers_courses import courses_router
from handlers.handlers_gpt import gpt_router
from handlers.handlers_menu_options import options_router
from handlers.handlers_start import start_router
from services.loggers import logger

load_dotenv()

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())

dp.include_routers(
    start_router,
    memory_router,
    options_router,
    courses_router,
    gpt_router,
    # handlers_menu_options.router,
    # handlers_menu_options_inline.router,
    # handlers_courses.router,
    # handlers_psychologist.router,
)


async def main():
    try:
        logger.info("Запуск бота...")
        await dp.start_polling(bot)
    finally:
        logger.info("Остановка бота...")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
