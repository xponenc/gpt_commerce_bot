import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import handlers_gpt
import os


# Настройка логирования
logging.basicConfig(
    # Устанавливаем уровень INFO, чтобы записывать уровни логирования: INFO, WARNING, ERROR, CRITICAL
    level=logging.INFO,
    # Формат сообщения, включающий временную метку, имя логгера, уровень логирования и само сообщение
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot.log'),  # Запись логов в файл "bot.log" для дальнейшего анализа
              logging.StreamHandler()])  # Вывод логов в консоль для отслеживания работы в реальном времени


load_dotenv()  # Загружаем переменные окружения из файла .env
# Создание экземпляра бота
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))  # Передаем токен из .env
# Инициализация диспетчера для управления обработчиками событий (сообщения, команды, нажатие кнопок и т.д.)
dp = Dispatcher(storage=MemoryStorage())

# Включаем маршрутизаторы (роутеры) команд и обработчиков в объект dp для обработки входящих сообщений
dp.include_routers(
    handlers_gpt.gpt_router,
    # handlers_start.router,
    # handlers_menu_options.router,
    # handlers_menu_options_inline.router,
    # handlers_courses.router,
    # handlers_psychologist.router,
)


# Запуска бота
async def main():
    try:
        logging.info("Запуск бота...")  # Логируем информацию о запуске бота
        # Запускаем процесс polling для получения и обработки обновлений от Telegram
        await dp.start_polling(bot)
    finally:
        # Логируем информацию об остановке работы бота
        logging.info("Остановка бота...")
        # Закрываем сессию бота для корректного завершения работы и освобождения ресурсов
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
