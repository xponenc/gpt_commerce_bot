from datetime import datetime

from sqlalchemy import select, insert

from services.db import async_session, users_table
from services.loggers import logger
from services.loggers_config import get_logger
from aiogram.types import Message, BotCommand


# Запись нового пользователя в таблицу users в базу данных
async def set_new_user(message: Message):
    async with async_session() as session:
        # Проверяем, существует ли уже пользователь с таким user_id
        stmt_check = select(users_table).where(
            users_table.c.user_id == message.from_user.id)
        result = await session.execute(stmt_check)
        user = result.fetchone()  # Получаем первую строку результата запроса

        if user is None:
            # Вставляем все поля для нового пользователя
            stmt_insert = insert(users_table).values(
                user_id=message.from_user.id,
                registration_date=datetime.utcnow(),  # Устанавливаем текущую дату и время
                username=message.from_user.username,  # username пользователя Telegram
                name=message.from_user.full_name)  # Полное имя пользователя Telegram
            await session.execute(stmt_insert)
            await session.commit()  # Фиксируем изменения
            logger.info(f"User {message.from_user.id} added into users_table")
