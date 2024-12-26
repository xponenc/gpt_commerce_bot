from collections import OrderedDict
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy import select
from db_start import (async_session, courses_table, lessons_table,
                      psychologists_table)


def reply_keyboard(buttons_list: list,  # Спискок названий кнопок
                   adj: int,            # Устанавливаем к-во кнопок в ряд
                   placeholder: str):   # Подсказка для поля ввода
    builder = ReplyKeyboardBuilder()
    for button in buttons_list:
        builder.button(text=button)
    builder.adjust(adj)  # Устанавливаем к-во кнопок в ряд
    return builder.as_markup(
        resize_keyboard=True,  # Клавиатура подстраивается под размер экрана
        one_time_keyboard=True,  # Клавиатура исчезнет после выбора варианта
        input_field_placeholder=placeholder)  # Подсказка для поля ввода


# Клавиатура категорий курсов из базы данных
async def categories_keyboard():
    async with async_session() as session:  # Открываем асинхронный контекст для сессии
        result = await session.execute(select(courses_table.c.category).
                                       distinct().order_by(courses_table.c.category))
        buttons = result.scalars().all()  # Извлекаем список категорий
    return reply_keyboard(buttons, 2, "Выберите категорию курсов")


# Клавиатура для курсов из базы данных на основе выбранной категории
async def courses_keyboard(category_name):
    async with async_session() as session:  # Открываем асинхронный контекст для сессии
        result = await session.execute(select(courses_table.c.course_name).
                                       where(courses_table.c.category == category_name).
                                       order_by(courses_table.c.course_name))
    buttons = result.scalars().all()  # Извлекаем список курсов из таблицы базы данных
    return reply_keyboard(buttons, 2, "Выберите курс для обучения")


# Клавиатура для уроков из базы данных на основе выбранного курса
async def lessons_keyboard(course_name):
    async with async_session() as session:  # Открываем асинхронный контекст для сессии
        result = await session.execute(
            select(lessons_table.c.lesson_name).
            where(lessons_table.c.course_id ==
                  select(courses_table.c.course_id).
                  where(courses_table.c.course_name == course_name).
                  scalar_subquery()).
            order_by(lessons_table.c.block_id))
    lesson_names = result.scalars().all()
    # Сохраняем уникальные, упорядоченные значения
    buttons = list(OrderedDict.fromkeys(lesson_names))
    return reply_keyboard(buttons, 1, "Выберите урок для обучения")


# Клавиатура для выбора психолога из базы данных
async def psychologist_keyboard():
    async with async_session() as session:  # Открываем асинхронный контекст для сессии
        result = await session.execute(select(psychologists_table.c.display_name).
                                       order_by(psychologists_table.c.id))
        buttons = result.scalars().all()  # Извлекаем список психологов
    return reply_keyboard(buttons, 2, "Выберите психолога")
