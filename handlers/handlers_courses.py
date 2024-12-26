from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboards_db import *
from sqlalchemy import select
from db_start import async_session, courses_table, lessons_table


# Класс, описывающий состояния
class CategoryState(StatesGroup):
    choosing_category = State()
    choosing_course = State()
    choosing_lesson = State()


# Создание экземпляра класса Router, который будет управлять маршрутами
router = Router()


# /courses
@router.message(Command('courses'))
async def cmd_courses(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("👁️ Выберите категорию курсов для обучения:",
                         reply_markup=await categories_keyboard())
    # Устанавливаем состояние "ожидание выбора"
    await state.set_state(CategoryState.choosing_category)


# Обработчик выбора категории
@router.message(~F.text.startswith('/'), CategoryState.choosing_category)
async def process_category(message: Message, state: FSMContext):
    await state.update_data(choosing_category=message.text)
    await message.answer("---", reply_markup=get_back_inline_keyboard())
    await message.answer(f"👁️ Выберите курс в категории: {message.text}:",
                         reply_markup=await courses_keyboard(message.text))
    # Переходим в состояние выбора курса
    await state.set_state(CategoryState.choosing_course)


# Обработчик выбора курса внутри категории
@router.message(~F.text.startswith('/'), CategoryState.choosing_course)
async def process_course(message: Message, state: FSMContext):
    await state.update_data(choosing_course=message.text)

    async with async_session() as session:  # Открываем асинхронный контекст для сессии
        # Описание курса из таблицы базы данных
        result = await session.execute(select(courses_table.c.description).
                                       where(courses_table.c.course_name == message.text))
    await message.answer(result.scalars().all()[0],
                         reply_markup=get_back_inline_keyboard())

    await message.answer(f"👁️ Выберите урок курса:",
                         reply_markup=await lessons_keyboard(message.text))
    # Переходим в состояние выбора урока
    await state.set_state(CategoryState.choosing_lesson)


# Обработчик выбора урока
@router.message(~F.text.startswith('/'), CategoryState.choosing_lesson)
async def process_lesson(message: Message, state: FSMContext):
    await state.update_data(choosing_lesson=message.text)
    data = await state.get_data()

    async with async_session() as session:
        # Извлекаем содержимое урока
        result = await session.execute(
            select(lessons_table.c.content).where(
                lessons_table.c.lesson_name == message.text,
                lessons_table.c.course_id == select(courses_table.c.course_id)
                .where(courses_table.c.course_name == data.get('choosing_course'))
                .scalar_subquery()
            ).order_by(lessons_table.c.block_id)
        )
        lesson_contents = result.scalars().all()

    if not lesson_contents:
        await message.answer("Урок не содержит разделов.")
        return
    # Сохраняем данные о текущем уроке и текущем индексе
    await state.update_data(lesson_contents=lesson_contents, current_index=0)
    # Отправляем первый раздел с кнопками навигации
    await message.answer(
        lesson_contents[0],
        reply_markup=part_lesson_navigation_keyboard(0, len(lesson_contents)))


# ---------------------------------------------------------------------------------
@router.callback_query(F.data.startswith("part_lesson_"))
async def lesson_navigation_callback(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()  # Считываем данные состояния
    choosing_course = data.get('choosing_course')
    lesson_contents = data.get('lesson_contents', [])
    current_index = data.get('current_index', 0)
    if not lesson_contents:
        await callback_query.message.answer("Данные урока недоступны.")
        await callback_query.answer()
        return

    action = callback_query.data.split("_")[2]  # Извлекаем действие
    if action == "prev" and current_index > 0:
        current_index -= 1
    elif action == "next" and current_index < len(lesson_contents) - 1:
        current_index += 1
    elif action == "back":
        await callback_query.message.answer("---", reply_markup=get_back_inline_keyboard())
        # Вернуться к выбору уроков
        await callback_query.message.answer("Вы вернулись к меню уроков.",
                                            reply_markup=await lessons_keyboard(choosing_course))
        await callback_query.answer()
        return

    # Обновляем текущий индекс в состоянии
    await state.update_data(current_index=current_index)
    # Логирование для отладки
    print(f"current_index после обновления: {current_index}")
    # Получаем новый текст и клавиатуру
    new_text = lesson_contents[current_index]
    new_keyboard = part_lesson_navigation_keyboard(
        current_index, len(lesson_contents)
    )
    current_text = callback_query.message.text or ""
    current_markup = callback_query.message.reply_markup

    # Проверяем, изменился ли текст или клавиатура
    if current_text == new_text:
        current_keyboard = current_markup.inline_keyboard if current_markup else None
        new_keyboard_list = new_keyboard.inline_keyboard
        # Сравниваем только клавиатуры
        if current_keyboard == new_keyboard_list:
            # Если текст и клавиатура одинаковы, просто подтверждаем callback
            await callback_query.answer()
            return

    # Если есть изменения, обновляем сообщение
    await callback_query.message.answer(
        new_text,
        reply_markup=new_keyboard
    )
    # Подтверждаем обработку callback'а
    await callback_query.answer()


@ router.callback_query(F.data == "back")
async def back_menu(callback_query: CallbackQuery, state: FSMContext):
    # Получаем текущее состояние пользователя
    current_state = await state.get_state()
    # Получаем данные состояния
    data = await state.get_data()

    # Если пользователь находится на уровне выбора курса в категории
    if current_state == CategoryState.choosing_course.state:
        # Если курс не выбран, возвращаем в меню выбора категории
        await state.set_state(CategoryState.choosing_category)
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await cmd_courses(callback_query.message, state)

    # Если пользователь находится на уровне выбора урока в курсе
    if current_state == CategoryState.choosing_lesson.state:
        # Если курс не выбран, возвращаем в меню выбора категории
        await state.set_state(CategoryState.choosing_course)
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.message.answer(f"👁️ Выберите курс в категории: {data.get('choosing_category')}:",
                                            reply_markup=await courses_keyboard(data.get('choosing_category')))

    await callback_query.answer()
