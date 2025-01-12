import asyncio
import os
from pprint import pprint

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from models.db_models import Base

# ********************************************************************
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
    return create_async_engine(url=DATABASE_URL, echo=False)


# Асинхронная функция для создания базы данных
async def create_db():
    engine = await get_async_engine()  # Получаем асинхронный движок базы данных
    async with engine.begin() as conn:  # Открываем асинхронный контекст для начала транзакции
        # Удаляем все таблицы из базы данных
        await conn.run_sync(Base.metadata.drop_all)
        # Создаем все таблицы на основе метаданных
        await conn.run_sync(Base.metadata.create_all)


# Асинхронная функция для создания отдельных таблиц
async def create_table_by_name(table_name: str):
    engine = await get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

        # Получаем объект таблицы по имени
        table = Base.metadata.tables[table_name]
        # Создаем таблицу
        await conn.run_sync(table.create)


# Очистка таблицы (удаление строк)
async def clear_table(table_name: str):
    engine = await get_async_engine()
    async with engine.begin() as conn:
        # Используем SQL выражение через `text`
        query = text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")
        await conn.execute(query)


async def operation_with_table(table_name: str):
    while True:
        operation_choice = input(
            f"Выберете операцию с таблицей {table_name}:\n"
            "\tСоздать таблицу - 1\n"
            "\tОчистить таблицу - 2\n"
            "\tВернуться в основное меню - q\n>> "
        )
        if operation_choice in "12":
            confirm_operation = input(
                f"Подтвердите операцию {'создания' if operation_choice == '1' else 'очистки'} для таблицы {table_name}\n"
                f">> y/n ")
            if confirm_operation.lower() == "y" and operation_choice == "1":
                await create_table_by_name(table_name)
                return
            if confirm_operation.lower() == "y" and operation_choice == "2":
                await clear_table(table_name)
                return
        elif operation_choice.lower() == "q":
            return


if __name__ == "__main__":
    TABLE_MENU = {str(index): table_name for index, table_name in enumerate(dict(Base.metadata.tables), start=1)}
    while True:
        main_choice = input(
            f"Выполнить первичное создание БД, создание таблиц: "
            f"{', '.join(table_name for table_name in (dict(Base.metadata.tables).keys()))} - нажмите 1\n"
            f"Начать работы с отдельными таблицами - нажмите 2\n"
            f"Для выхода нажмите q\n>> "
        )
        if main_choice == "1":
            confirm = input("Подтвердите первичное создание БД: y/n\n>> ")
            if confirm.lower() == "y":
                asyncio.run(create_db())
        elif main_choice == "2":
            tables = '\n\t'.join(f"{value}: {key}" for key, value in TABLE_MENU.items())
            choice_table = input(f"Выберите таблицу для операции\n\t{tables}\n\t>> ")
            if choice_table in TABLE_MENU.keys():
                print(TABLE_MENU[choice_table])
                asyncio.run(operation_with_table(TABLE_MENU[choice_table]))
                # asyncio.run(clear_table('payment_records'))
        elif main_choice.lower() == "q":
            break
