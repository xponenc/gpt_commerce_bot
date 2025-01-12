from aiogram.types import FSInputFile, Message
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import start_dialog_keyboard
from keyboards.keyboards_db import *
from sqlalchemy import select

from models.db_models import Psychologist
from services.db import async_session


PSYCHOLOGIST_COMMANDS = {
    "courses": {
        "name": "Курсы по психологии",
        "info": "1. 📚 - Курсы по психологии: Ознакомьтесь с доступными курсами"},
    "personal_psychologist": {
        "name": "Личный психолог",
        "info": "2. 🧑 - Личный психолог: Общайтесь с виртуальным психологом"},
    "payment": {
        "name": "Оплата и кредиты",
        "info": "3. 💳 - Оплата и кредиты: Просмотрите информацию об оплате и кредитах"},
    "options": {
        "name": "Настройки",
        "info": "4. ⚙️ - Изменить настройки: Измените настройки вашего профиля"},
    "support": {
        "name": "Тех. поддержка",
        "info": "5. 🆘 - Тех.поддержка: Обратитесь за технической поддержкой"},
}


# Класс, описывающий состояния
class PsychologistState(StatesGroup):
    choosing_psychologist = State()  # Выбор психолога


# Создание экземпляра класса Router, который будет управлять маршрутами
router = Router()


# /personal_psychologist
@router.message(Command('personal_psychologist'))
async def cmd_psychologist(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("👁️ Выберите персонального психолога для общения:",
                         reply_markup=await psychologist_keyboard())
    # Устанавливаем состояние ожидание выбора психолога
    await state.set_state(PsychologistState.choosing_psychologist)


# Обработчик выбора психолога из psychologist_keyboard()
@router.message(F.text & ~F.text.startswith('/') & ~F.text.in_(['🔙 Назад', '💬 Начать диалог']),
                PsychologistState.choosing_psychologist)
async def process_psychologist(message: Message, state: FSMContext):
    # Сохраняем выбор психолога в состоянии
    await state.update_data(chosen_psychologist=message.text)

    async with async_session() as session:  # Открываем асинхронный контекст для сессии

        # Через psychologists_table. Объединенный запрос для получения аватара и описания психолога
        # result = await session.execute(select(
        #     psychologists_table.c.avatar,
        #     psychologists_table.c.description
        # ).where(psychologists_table.c.display_name == message.text))

        # Через модель Psychologist. Объединенный запрос для получения аватара и описания психолога
        result = await session.execute(select(
            Psychologist.avatar,
            Psychologist.description
        ).where(Psychologist.display_name == message.text))

        avatar, description = result.one()  # Получаем сразу оба значения

        # Отправляем аватар пользователю
        photo = FSInputFile(f"UIA_Work/TG_Bot_Psy/06/picture/{avatar}")
        await message.answer_photo(photo=photo)

        # Отправляем описание психолога пользователю
        await message.answer(description, reply_markup=start_dialog_keyboard())


# Обработка начала диалога с персональным психологом
@ router.message(F.text == '💬 Начать диалог', PsychologistState.choosing_psychologist)
async def start_dialog(message: Message, state: FSMContext):
    data = await state.get_data()  # Получаем сохраненные данные выбора психолога
    if data:
        await message.answer(f"{data['chosen_psychologist']}.")


# Назад в меню выбора персонального психолога
@ router.message(F.text == '🔙 Назад', PsychologistState.choosing_psychologist)
async def back_cmd_psychologist(message: Message, state: FSMContext):
    await state.clear()  # Завершаем состояние
    await cmd_psychologist(message, state)
