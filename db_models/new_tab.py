import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from datetime import datetime  # Импортируем класс datetime для работы с датами
from sqlalchemy import (DateTime, BigInteger, Text, ForeignKey, Integer, String,
                        Boolean, TIMESTAMP, Numeric, JSON, Date)
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from datetime import datetime
from typing import Optional, List
import asyncio
from models import User, Lesson, Psychologist


# Создаем базовый класс для декларативного стиля SQLAlchemy, который будет служить основой для других моделей.
class Base(DeclarativeBase):
    pass  # Класс не содержит дополнительных атрибутов или методов


# Модель таблицы "psy_messages"
class PsyMessages(Base):
    __tablename__ = 'psy_messages'
    # Поле id - INTEGER, первичный ключ
    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Поле user_id - BIGINT, внешний ключ, ссылается на таблицу users
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(User.user_id), nullable=False)
    # Поле day_time с типом DATETIME
    day_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime)
    # Поле psy_name - VARCHAR(50), обязательное
    psy_name: Mapped[str] = mapped_column(String(50), nullable=True)
    # Поле message - TEXT, необязательное
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


# Модель таблицы "lessons_messages"
class LessonsMessages(Base):
    __tablename__ = 'lessons_messages'
    # Поле id - INTEGER, первичный ключ
    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Поле user_id - BIGINT, внешний ключ, ссылается на таблицу users
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(User.user_id), nullable=False)
    # Поле day_time с типом DATETIME
    day_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime)
    # Поле course_id
    course_id: Mapped[int] = mapped_column(Integer, nullable=True)
    # Поле block_id
    block_id: Mapped[int] = mapped_column(Integer, nullable=True)
    # Поле message - TEXT, необязательное
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


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
