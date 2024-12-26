import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect
from dotenv import load_dotenv
import os


load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Создание асинхронного движка
async_engine = create_async_engine(DATABASE_URL)


async def get_table_info():
    async with async_engine.connect() as connection:
        # Получаем список таблиц и информацию о колонках через run_sync
        tables = await connection.run_sync(lambda conn: inspect(conn).get_table_names())

        for table_name in tables:
            print(f"\nТаблица: {table_name}")

            # Получение информации о первичном ключе
            pk_constraint = await connection.run_sync(lambda conn: inspect(conn).get_pk_constraint(table_name))
            pk_columns = pk_constraint['constrained_columns']
            print(f"  Primary Key: {', '.join(pk_columns)}")

            # Получение информации о внешних ключах
            foreign_keys = await connection.run_sync(lambda conn: inspect(conn).get_foreign_keys(table_name))
            if foreign_keys:
                for fk in foreign_keys:
                    print(f"  Foreign Key: {fk['constrained_columns']} -> "
                          f"таблица: {fk['referred_table']}({fk['referred_columns']})")
            else:
                print("  Foreign Key: нет внешних ключей")

            # Получение информации о колонках
            columns = await connection.run_sync(lambda conn: inspect(conn).get_columns(table_name))
            for column in columns:
                print(
                    f"  - Колонка: {column['name']}, Тип: {column['type']}, Обязательное: {column['nullable']}")


# Асинхронный запуск
asyncio.run(get_table_info())
