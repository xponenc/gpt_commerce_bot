from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import *


# Класс, описывающий состояния
class OptionState(StatesGroup):
    choosing_option = State()  # Ожидание выбора опции
    changing_name = State()    # Ввод нового имени
    changing_speed = State()   # Выбор новой скорости звука
    changing_temperature = State()  # Выбор новой температуры
    changing_audio_responses = State()  # Аудио ответы в чатах
    changing_autopayments = State()  # Автоплатеж


# Создание экземпляра класса Router, который будет управлять маршрутами
router = Router()


# /options *************************************************************************
@router.message(Command('options'))
async def cmd_options(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🛠️ Выберите опцию, которую хотите изменить:",
                         reply_markup=options_keyboard())
    # Устанавливаем состояние "ожидание выбора"
    await state.set_state(OptionState.choosing_option)


# Обработчик выбора опции из get_options_keyboard()
@router.message(OptionState.choosing_option)
async def process_option(message: Message, state: FSMContext):
    if message.text == "📝 Изменить имя":
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


# Обработчик изменения имени
@router.message(OptionState.changing_name)
async def change_name(message: Message, state: FSMContext):
    new_name = message.text  # Получаем введенное имя
    # Здесь обрабатываем new_name ...
    await message.answer(f"Ваше новое имя: {new_name}. Настройка завершена.")
    await state.clear()  # Завершаем состояние


# Обработчик изменения скорости звука
@router.message(OptionState.changing_speed)
async def change_speed(message: Message, state: FSMContext):
    new_speed = message.text  # Получаем выбранную скорость
    # Здесь обрабатываем new_speed ...
    await message.answer(f"Скорость звука изменена на: {new_speed}. Настройка завершена.")
    await state.clear()  # Завершаем состояние


# Обработчик изменения температуры
@router.message(OptionState.changing_temperature)
async def change_temperature(message: Message, state: FSMContext):
    new_temperature = message.text  # Получаем выбранную температуру
    # Здесь обрабатываем new_temperature ...
    await message.answer(f"Температура модели изменена на: {new_temperature}. Настройка завершена.")
    await state.clear()  # Завершаем состояние


# Обработчик изменения аудио ответов в чатах
@router.message(OptionState.changing_audio_responses)
async def change_audio_responses(message: Message, state: FSMContext):
    audio_responses = message.text
    # Здесь обрабатываем audio_responses ...
    await message.answer(f"Аудио ответы в чатах: {audio_responses}. Настройка завершена.")
    await state.clear()  # Завершаем состояние


# Обработчик изменения автоплатежей
@router.message(OptionState.changing_autopayments)
async def change_autopayments(message: Message, state: FSMContext):
    autopayments = message.text
    # Здесь обрабатываем autopayments ...
    await message.answer(f"Автоплатежи: {autopayments}. Настройка завершена.")
    await state.clear()  # Завершаем состояние
