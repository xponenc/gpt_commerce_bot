from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import *


# Определяем состояния для процесса настройки
class OptionState(StatesGroup):
    choosing_option = State()  # Ожидание выбора опции
    changing_name = State()    # Ввод нового имени
    changing_speed = State()   # Выбор новой скорости звука
    changing_temperature = State()  # Выбор новой температуры
    changing_audio_responses = State()  # Аудио ответы в чатах
    changing_autopayments = State()  # Включение автоплатежей


# Создание экземпляра класса Router, который будет управлять маршрутами
router = Router()


# /options *************************************************************************
@router.message(Command('options'))
async def cmd_options(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('🛠️ Выберите опцию, которую хотите изменить:',
                         reply_markup=options_inline_keyboard())
    # Устанавливаем состояние "ожидание выбора"
    await state.set_state(OptionState.choosing_option)


# Универсальный обработчик для выбора настройки
@router.callback_query(F.data, OptionState.choosing_option)
async def process_option(callback_query: CallbackQuery, state: FSMContext):
    # Сохраняем выбор опции в состоянии
    await state.update_data(choosing_option=callback_query.data)

    # Ловим callback_data и обрабатываем
    if callback_query.data == "change_name":
        await state.set_state(OptionState.changing_name)
        await callback_query.message.answer("📝 Введите новое имя:")

    elif callback_query.data == "change_speed":
        await state.set_state(OptionState.changing_speed)
        await callback_query.message.answer("🎚️ Выберите скорость звука:",
                                            reply_markup=get_speed_reply_keyboard())

    elif callback_query.data == "change_temperature":
        await state.set_state(OptionState.changing_temperature)
        await callback_query.message.answer("🌡️ Выберите температуру:",
                                            reply_markup=get_temperature_reply_keyboard())

    elif callback_query.data == "change_audio_responses":
        await state.set_state(OptionState.changing_audio_responses)
        await callback_query.message.answer("🎧 Выберите режим для аудио ответов в чатах:",
                                            reply_markup=get_audio_reply_keyboard())

    elif callback_query.data == "change_autopayments":
        await state.set_state(OptionState.changing_autopayments)
        await callback_query.message.answer("🔄 Вы хотите включить/отключить автоплатежи?",
                                            reply_markup=get_autopayments_reply_keyboard())
    # Убираем Inline-клавиатуру из сообщения
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()  # Закрываем callback-запрос


# Обработчик изменения имени
@router.message(F.text, OptionState.changing_name)
async def change_name(message: Message, state: FSMContext):
    # Сохраняем имя в состоянии
    await state.update_data(changing_name=message.text)
    new_name = message.text  # Получаем введенное имя
    # Здесь обрабатываем new_name ...
    await message.answer(f"Ваше новое имя: {new_name}. Настройка завершена.")

    print(await state.get_data())  # Посмотрим на сохраненные данные в консоли
    await state.clear()  # Завершаем состояние


# Обработчик изменения скорости звука
@router.message(OptionState.changing_speed)
async def change_speed(message: Message, state: FSMContext):
    # Сохраняем скорость звука в состоянии
    await state.update_data(changing_speed=message.text)
    new_speed = message.text  # Получаем выбранную скорость
    # Здесь обрабатываем ...
    await message.answer(f"Скорость звука изменена на: {new_speed}. Настройка завершена.")

    print(await state.get_data())  # Посмотрим на сохраненные данные в консоли
    await state.clear()  # Завершаем состояние


# Обработчик изменения температуры
@router.message(OptionState.changing_temperature)
async def change_temperature(message: Message, state: FSMContext):
    # Сохраняем температуру в состоянии
    await state.update_data(changing_temperature=message.text)
    new_temperature = message.text  # Получаем выбранную температуру
    # Здесь обрабатываем ...
    await message.answer(f"Температура модели изменена на: {new_temperature}. Настройка завершена.")

    print(await state.get_data())  # Посмотрим на сохраненные данные в консоли
    await state.clear()  # Завершаем состояние


# Обработчик изменения аудио ответов в чатах
@router.message(OptionState.changing_audio_responses)
async def change_audio_responses(message: Message, state: FSMContext):
    # Сохраняем выбор аудио ответов в чатах в состоянии
    await state.update_data(changing_audio_responses=message.text)
    audio_responses = message.text  # Получаем ответ
    # Здесь обрабатываем ...
    await message.answer(f"Аудио ответы в чатах: {audio_responses}. Настройка завершена.")

    print(await state.get_data())  # Посмотрим на сохраненные данные в консоли
    await state.clear()  # Завершаем состояние


# Обработчик изменения автоплатежей
@router.message(OptionState.changing_autopayments)
async def change_autopayments(message: Message, state: FSMContext):
    # Сохраняем режим автоплатежей в состоянии
    await state.update_data(changing_autopayments=message.text)
    autopayments = message.text  # Получаем ответ
    # Здесь обрабатываем ...
    await message.answer(f"Автоплатежи: {autopayments}. Настройка завершена.")

    print(await state.get_data())  # Посмотрим на сохраненные данные в консоли
    await state.clear()  # Завершаем состояние
