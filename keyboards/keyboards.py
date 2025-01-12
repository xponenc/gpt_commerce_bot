from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# Клавиатура для изменения настроек (Reply версия) -------------------------------
def options_keyboard():
    builder = ReplyKeyboardBuilder()
    buttons = ["📝 Посмотреть действующие опции",
               "📝 Изменить имя",
               "🎚️ Изменить скорость звука",
               "🌡️ Изменить температуру",
               "🎧 Аудио ответы в чатах",
               "🔄 Включить/отключить автоплатежи"]
    for button in buttons:
        builder.button(text=button)
    builder.adjust(2)  # Устанавливаем по 2 кнопки в ряд
    return builder.as_markup(
        resize_keyboard=True,  # Клавиатура подстраивается под размер экрана
        one_time_keyboard=True,  # Клавиатура исчезнет после выбора варианта
        input_field_placeholder="Изменение настроек")  # Подсказка для поля ввода


# Клавиатура для изменения настроек (Inline версия)
def options_inline_keyboard():
    builder = InlineKeyboardBuilder()
    buttons = [("📝 Изменить имя", "change_name"),
               ("🎚️ Изменить скорость звука", "change_speed"),
               ("🌡️ Изменить температуру", "change_temperature"),
               ("🎧 Аудио ответы в чатах", "change_audio_responses")]
    for text, callback_data in buttons:
        builder.button(text=text, callback_data=callback_data)
    builder.adjust(1)  # Устанавливаем по одной кнопке в ряд
    return builder.as_markup()
# ---------------------------------------------------------------------------------


# Клавиатура управления по разделам урока
def part_lesson_navigation_keyboard(current_index: int, total_items: int):
    builder = InlineKeyboardBuilder()
    # Добавление кнопки "Предыдущий раздел", если это не первый раздел
    if current_index > 0:
        builder.button(
            text="◀️ Предыдущий раздел",
            callback_data=f"part_lesson_prev_{current_index - 1}")
    # Добавление кнопки "Следующий раздел", если это не последний раздел
    if current_index < total_items - 1:
        builder.button(
            text="Следующий раздел ▶️",
            callback_data=f"part_lesson_next_{current_index + 1}")
    # Добавление кнопки "Назад к меню уроков"
    builder.button(
        text="📚 Назад к меню уроков",
        callback_data="part_lesson_back")
    # Устанавливаем кнопки в один ряд
    builder.adjust(1)
    # Возвращаем объект InlineKeyboardMarkup
    return builder.as_markup()


# Клавиатура для начала диалога
def start_dialog_keyboard():
    keyboard = [[KeyboardButton(text="🔙 Назад"),
                 KeyboardButton(text="💬 Начать диалог")]]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,  # Передаем список кнопок
        resize_keyboard=True,  # Клавиатура будет адаптироваться под экран
        one_time_keyboard=True)  # Клавиатура исчезнет после выбора варианта


# Клавиатура с выбором температуры
def get_temperature_reply_keyboard():
    builder = ReplyKeyboardBuilder()
    for button in ["0.0 ❄️ Логичный",
                   "0.2 🌬️ Рассудительный",
                   "0.6 🌿 Сбалансированный",
                   "1.0 🔥 Творческий",
                   "2.0 💥 Фантазер"]:
        builder.button(text=button)
    builder.adjust(2)  # Устанавливаем по 2 кнопки в ряд
    return builder.as_markup(
        resize_keyboard=True,  # Клавиатура подстраивается под размер экрана
        one_time_keyboard=True,  # Клавиатура исчезнет после выбора варианта
        input_field_placeholder="Выберите температуру модели")  # Подсказка для поля ввода


# Клавиатура для техподдержки с кнопкой "Часто задаваемые вопросы"
def get_support_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❓ Часто задаваемые вопросы")]],
        resize_keyboard=True,  # Клавиатура будет адаптироваться к экрану
        one_time_keyboard=True)  # Клавиатура исчезнет после выбора варианта


# Клавиатура для выбора скорости звука
def get_speed_reply_keyboard():
    builder = ReplyKeyboardBuilder()
    for button in ["0.9 🐢 Замедленная",
                   "1.0 ⚖️ Обычная",
                   "1.1 🚀 Ускоренная",
                   "2.0 🏎️ Очень быстрая"]:
        builder.button(text=button)
    builder.adjust(2)  # Установка количества кнопок в одной строке
    return builder.as_markup(
        resize_keyboard=True,  # Клавиатура будет подстраиваться под размер экрана
        one_time_keyboard=True,  # Клавиатура исчезнет после выбора варианта
        input_field_placeholder="Выберите скорость звука")  # Подсказка для поля ввода


# Клавиатура для выбора аудио включено/выключено
def get_audio_reply_keyboard():
    keyboard = [[KeyboardButton(text="🔊 Включено"),
                 KeyboardButton(text="🔇 Выключено")]]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,  # Передаем список кнопок
        resize_keyboard=True,  # Клавиатура адаптируется под экран
        one_time_keyboard=True)  # Клавиатура исчезнет после выбора варианта


# Inline клавиатура с кнопкой "Назад"
def get_back_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад",
                                               callback_data="back")]])


# Inline клавиатура с кнопкой "Назад"
def start_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🚀 Старт",
                                               callback_data="start")]])


# Reply клавиатура с кнопкой "Назад"
def get_back_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Назад")]],
        resize_keyboard=True,
        one_time_keyboard=True)


# Клавиатура для подтверждения оплаты
def get_payment_confirmation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Оплатить"),
                   KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True,  # Клавиатура подстраивается под экран
        one_time_keyboard=True)  # Клавиатура исчезнет после выбора варианта


# Клавиатура для подтверждения автооплаты
def get_autopayments_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Включить автоплатежи"),
                   KeyboardButton(text="❌ Отключить автоплатежи")]],
        resize_keyboard=True,  # Клавиатура подстраивается под экран
        one_time_keyboard=True)  # Клавиатура исчезнет после выбора варианта
