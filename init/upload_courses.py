import asyncio

from services.db import async_session


async def execute_sql_file(file_path: str):
    # Открываем файл и читаем его содержимое
    with open(file_path, 'r', encoding="utf-8") as file:
        sql_queries = file.read()

    # Подключаемся к базе и выполняем SQL-запросы
    async with async_session() as session:
        await session.execute(sql_queries)
        print(f"SQL файл '{file_path}' успешно загружен!")


if __name__ == "__main__":
    confirm = input("Загрузить данные в таблицу курсов? y/n ")
    if confirm == "y":
        asyncio.run(execute_sql_file('courses_data.sql'))

