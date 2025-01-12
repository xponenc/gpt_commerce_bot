from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import *
from keyboards.keyboards import options_keyboard, get_speed_reply_keyboard, get_temperature_reply_keyboard, \
    get_audio_reply_keyboard, get_autopayments_reply_keyboard
from services.process_options import update_user_name, update_user_speed, update_user_temperature, update_user_audio, \
    update_user_auto_renewal, get_user_options


# Класс, описывающий состояния
class OptionState(StatesGroup):
    choosing_option = State()  # Ожидание выбора опции
    changing_name = State()  # Ввод нового имени
    changing_speed = State()  # Выбор новой скорости звука
    changing_temperature = State()  # Выбор новой температуры
    changing_audio_responses = State()  # Аудио ответы в чатах
    changing_autopayments = State()  # Включение автоплатежей


# Создание экземпляра класса Router, который будет управлять маршрутами
options_router = Router()


# /options *************************************************************************
@options_router.message(Command('options'))
async def cmd_options(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🛠️ Выберите опцию, которую хотите изменить:",
                         reply_markup=options_keyboard())
    await state.set_state(OptionState.choosing_option)  # Устанавливаем состояние "ожидание выбора"


# Обработчик выбора опции из get_options_keyboard()
@options_router.message(OptionState.choosing_option)
async def process_option(message: Message, state: FSMContext):
    if message.text == "📝 Посмотреть действующие опции":
        options = await get_user_options(user_id=message.from_user.id)
        options_output = (f"Температура модели: {options.get("temperature")}\n"
                          f"Скорость воспроизведения: {options.get("speed")}\n"
                          f"Аудио ответы в чатах: {'ВКЛ' if options.get("audio") else 'ОТКЛ'}\n"
                          f"Автоплатежи: {'ВКЛ' if options.get("autopayments") else 'ОТКЛ'}\n"
                          )
        await message.answer(f"📝 Действующие опции:\n{options_output}")
        await state.clear()

        # Переходим в состояние ожидания имени

    elif message.text == "📝 Изменить имя":
        await message.answer("📝 Введите новое имя:")
        # Переходим в состояние ожидания имени
        await state.set_state(OptionState.changing_name)

    elif message.text == "🎚️ Изменить скорость звука":
        await message.answer("🎚️ Выберите скорость звука:",
                             reply_markup=get_speed_reply_keyboard())
        # Переходим в состояние выбора скорости
        await state.set_state(OptionState.changing_speed)

    elif message.text == "🌡️ Изменить температуру":
        await message.answer("🌡️ Выберите температуру:",
                             reply_markup=get_temperature_reply_keyboard())
        # Переходим в состояние выбора температуры
        await state.set_state(OptionState.changing_temperature)

    elif message.text == "🎧 Аудио ответы в чатах":
        await message.answer("🎧 Выберите режим для аудио ответов в чатах:",
                             reply_markup=get_audio_reply_keyboard())
        # Переходим в состояние изменения аудио ответов
        await state.set_state(OptionState.changing_audio_responses)

    elif message.text == "🔄 Включить/отключить автоплатежи":
        await message.answer("🔄 Вы хотите включить/отключить автоплатежи?",
                             reply_markup=get_autopayments_reply_keyboard())
        # Переходим в состояние изменения автоплатежей
        await state.set_state(OptionState.changing_autopayments)
    else:
        await message.answer("Выберите одну из опций с клавиатуры:",
                             reply_markup=options_keyboard())


@options_router.message(OptionState.changing_name)
async def change_name(message: Message, state: FSMContext):
    """Обработчик изменения имени"""
    new_name = message.text
    await update_user_name(user_id=message.from_user.id, new_name=new_name)
    await message.answer(f"Ваше новое имя: {new_name}. Настройка завершена.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Обработчик изменения скорости звука
@options_router.message(OptionState.changing_speed)
async def change_speed(message: Message, state: FSMContext):
    new_speed = message.text
    try:
        new_speed = new_speed.split()[0]
        new_speed = float(new_speed)
        if 0.5 > new_speed or new_speed > 2.0:
            raise ValueError
        await update_user_speed(user_id=message.from_user.id, new_speed=new_speed)
        await message.answer(f"Скорость звука изменена на: {new_speed}. Настройка завершена.",
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()
    except ValueError:
        await message.answer(f"Ошибка ввода {new_speed}, введите число от 0.5 до 2.0",
                             reply_markup=get_speed_reply_keyboard())


# Обработчик изменения температуры
@options_router.message(OptionState.changing_temperature)
async def change_temperature(message: Message, state: FSMContext):
    new_temperature = message.text  # Получаем выбранную температуру
    try:
        new_temperature = new_temperature.split()[0]
        new_temperature = float(new_temperature)
        if 0.0 > new_temperature or new_temperature > 2.0:
            raise ValueError
        await update_user_temperature(user_id=message.from_user.id, new_temperature=new_temperature)
        await message.answer(f"Температура модели изменена на: {new_temperature}. Настройка завершена.",
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()
    except ValueError:
        await message.answer(f"Ошибка ввода {new_temperature}, введите число от 0.0 до 2.0",
                             reply_markup=get_speed_reply_keyboard())


# Обработчик изменения аудио ответов в чатах
@options_router.message(OptionState.changing_audio_responses)
async def change_audio_responses(message: Message, state: FSMContext):
    audio_responses = message.text
    if "включено" in audio_responses.lower():
        audio_responses = True
    elif "выключено" in audio_responses.lower():
        audio_responses = False
    else:
        await message.answer(f"Некорректный ввод, повторите выбор",
                             reply_markup=get_speed_reply_keyboard())
    await update_user_audio(user_id=message.from_user.id, new_audio=audio_responses)
    await message.answer(f"Аудио ответы в чатах: {'Вкл' if audio_responses else 'Откл'}. Настройка завершена.",
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Обработчик изменения автоплатежей
@options_router.message(OptionState.changing_autopayments)
async def change_autopayments(message: Message, state: FSMContext):
    autopayments = message.text
    if "включить автоплатежи" in autopayments.lower():
        autopayments = True
    elif "отключить автоплатежи" in autopayments.lower():
        autopayments = False
    else:
        await message.answer(f"Некорректный ввод, повторите выбор",
                             reply_markup=get_autopayments_reply_keyboard())
    await update_user_auto_renewal(user_id=message.from_user.id, new_auto_renewal=autopayments)
    await message.answer(f"Автоплатежи: {'Вкл' if autopayments else 'Откл'}. Настройка завершена.",
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()  # Завершаем состояние
