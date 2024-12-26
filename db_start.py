from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import Table, MetaData, Column, String, Integer, Text, ForeignKey


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
                      Column('description', String))


# описание существующей таблицы lessons из базы данных
lessons_table = Table('lessons',
                      metadata,
                      Column('block_id', Integer, primary_key=True,
                             autoincrement=True),  # Первичный ключ
                      Column('course_id', Integer, ForeignKey('courses.course_id'),
                             nullable=False),  # Внешний ключ на courses
                      Column('lesson_name', Text, nullable=False),
                      Column('content', Text, nullable=False))  # Содержимое урока
