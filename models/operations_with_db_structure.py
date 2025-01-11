import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

# Создание базы данных на основании моделей
load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Асинхронная функция для получения асинхронного движка базы данных
async def get_async_engine():
    # Создаем и возвращаем асинхронный движок с URL из настроек
    return create_async_engine(url=DATABASE_URL, echo=True)


# Асинхронная функция для создания базы данных
async def create_db():
    engine = await get_async_engine()  # Получаем асинхронный движок базы данных
    async with engine.begin() as conn:  # Открываем асинхронный контекст для начала транзакции
        # Удаляем все таблицы из базы данных
        await conn.run_sync(Base.metadata.drop_all)
        # Создаем все таблицы на основе метаданных
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    confirm = input("Выполнить первичное создание ДБ? y/n")
    if confirm.lower() == "y":
        asyncio.run(create_db())
