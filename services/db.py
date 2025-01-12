from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import (Table, MetaData, Column, String, Integer, BigInteger, Text, Numeric,
                        ForeignKey, DateTime, Boolean)


load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Создание асинхронного сессионного объекта
async_session = async_sessionmaker(
    create_async_engine(url=DATABASE_URL, echo=False),
    expire_on_commit=False,
    class_=AsyncSession)


# объект MetaData для хранения информации о схеме базы данных
metadata = MetaData()


# описание существующей таблицы psychologists из базы данных
psychologists_table = Table('psychologists',
                            metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String),
                            Column('description', String),
                            Column('avatar', String),
                            Column('display_name', String),
                            Column('psychologist_name', String))


# описание существующей таблицы courses из базы данных
courses_table = Table('courses',
                      metadata,
                      Column('course_id', Integer, primary_key=True),
                      Column('category', String),
                      Column('course_name', String),
                      Column('description', String),
                      Column('picture', String))


# описание существующей таблицы lessons
lessons_table = Table('lessons',
                      metadata,
                      Column('block_id', Integer, primary_key=True,
                             autoincrement=True),  # Первичный ключ
                      Column('course_id', Integer, ForeignKey('courses.course_id'),
                             nullable=False),  # Внешний ключ на courses
                      Column('lesson_name', Text, nullable=False),
                      Column('content', Text, nullable=False))  # Содержимое урока


# описание части существующей таблицы users
users_table = Table('users',
                    metadata,
                    Column('user_id', BigInteger, primary_key=True),
                    Column('registration_date', DateTime,
                           nullable=False, default=datetime),
                    Column('username', String(255), nullable=True),
                    Column('name', String(255), nullable=True),
                    Column("temperature", Numeric, nullable=True),
                    Column("speed", Numeric, nullable=True),
                    Column("audio", Boolean, nullable=True),
                    Column('auto_renewal', Boolean, nullable=True))


# описание таблицы psy_messages
psy_messages_table = Table(
    'psy_messages',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', BigInteger, ForeignKey('users.user_id'), nullable=False),
    Column('day_time', DateTime, nullable=False, default=datetime),
    Column('psy_name', String(50), nullable=False),
    Column('message', Text, nullable=True))


# описание таблицы lessons_messages
lessons_messages_table = Table(
    'lessons_messages',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', BigInteger, ForeignKey('users.user_id'), nullable=False),
    Column('day_time', DateTime, nullable=False, default=datetime),
    Column('course_id', Integer, nullable=True),
    Column('block_id', Integer, nullable=True),
    Column('message', Text, nullable=True))


# описание таблицы lessons_messages
support_query_table = Table(
    'support_query',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', BigInteger, ForeignKey('users.user_id'), nullable=False),
    Column('date_time', DateTime, nullable=False, default=datetime),
    Column('query', Text, nullable=True))
