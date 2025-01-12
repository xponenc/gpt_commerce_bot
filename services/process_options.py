from sqlalchemy import select

from services.db import async_session, users_table
from services.loggers import logger


async def update_user_name(user_id: int, new_name: str):
    """Обновление имени пользователя"""
    async with async_session() as session:
        query = select(users_table.c.name).where(users_table.c.user_id == user_id)
        result = await session.execute(query)
        current_user_name = result.fetchone()[0]
        if current_user_name != new_name:
            stmt_update = (users_table.update()
                           .where(users_table.c.user_id == user_id)
                           .values(name=new_name))  # Устанавливаем новое значение поля name
            await session.execute(stmt_update)  # Выполняем запрос
            await session.commit()  # Фиксируем изменения
            logger.info(
                f"Updated name for user {user_id} from {current_user_name} to {new_name}")


async def update_user_speed(user_id: int, new_speed: float):
    """Обновление скорости воспроизведения голосовых ответов"""
    async with async_session() as session:
        stmt_update = (users_table.update()
                       .where(users_table.c.user_id == user_id)
                       .values(speed=new_speed))
        await session.execute(stmt_update)
        await session.commit()
        logger.info(
            f"Updated speed for user {user_id} to speed: {new_speed}")


async def update_user_temperature(user_id: int, new_temperature: float):
    """Обновление температуры ответов модели"""
    async with async_session() as session:
        stmt_update = (users_table.update()
                       .where(users_table.c.user_id == user_id)
                       .values(temperature=new_temperature))
        await session.execute(stmt_update)
        await session.commit()
        logger.info(
            f"Updated temperature for user {user_id} to temperature: {new_temperature}")


async def update_user_audio(user_id: int, new_audio: bool):
    """Обновление выбора озвучивания сообщений"""
    async with async_session() as session:
        stmt_update = (users_table.update()
                       .where(users_table.c.user_id == user_id)
                       .values(audio=new_audio))
        await session.execute(stmt_update)
        await session.commit()
        logger.info(
            f"Updated audio for user {user_id} to audio: {new_audio}")


# Обновление только поля auto_renewal в таблице users
async def update_user_auto_renewal(user_id: int, new_auto_renewal: bool):
    """Обновление поля Автоплатежи"""
    async with async_session() as session:
        stmt_update = (users_table.update()
                       .where(users_table.c.user_id == user_id)
                       .values(auto_renewal=new_auto_renewal))  # Устанавливаем новое значение поля auto_renewal
        await session.execute(stmt_update)  # Выполняем запрос
        await session.commit()  # Фиксируем изменения
        logger.info(
            f"Updated auto_renewal for user {user_id} to autopayments: {new_auto_renewal}")


# Получение temperature, speed, audio, auto_renewal по user_id
async def get_user_options(user_id: int):
    async with async_session() as session:
        stmt = select(users_table.c.temperature,
                      users_table.c.speed,
                      users_table.c.audio,
                      users_table.c.auto_renewal
                      ).where(users_table.c.user_id == user_id)
        result = await session.execute(stmt)
        user_data = result.fetchone()  # Получаем первую строку результата
        if user_data:
            temperature, speed, audio, auto_renewal = user_data
            temperature = temperature if temperature else 0.
            speed = speed if speed else 1.
            res = {"temperature": float(round(temperature, 1)),
                   "speed": float(round(speed, 1)),
                   "audio": audio,
                   "autopayments": auto_renewal}
            logger.info(f'user_options: {res}')
        else:
            logger.warning(f"User options {user_id} not found.")
            res = {"temperature": 0,
                   "speed": 1,
                   "audio": True,
                   "autopayments": False}
        return res

