from aiogram.types import Message, BotCommand
from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


# Создание экземпляра класса Router, который будет управлять маршрутами
router = Router()


# Menu команд
@router.startup()
async def set_menu_button(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Старт'),
        BotCommand(command='/courses', description='Курсы по психологии'),
        BotCommand(command='/personal_psychologist',
                   description='Личный психолог'),
        BotCommand(command='/payment', description='Оплата и кредиты'),
        BotCommand(command='/options', description='Изменить настройки'),
        BotCommand(command='/support', description='Тех. поддержка')]
    await bot.set_my_commands(main_menu_commands)


# /start
@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "В нашем боте Вам доступны следующие опции:\n\n"
        "1. 📚 - Курсы по психологии: Ознакомьтесь с доступными курсами (/courses).\n"
        "2. 🧑‍💼 - Личный психолог: Общайтесь с виртуальным психологом (/personal_psychologist).\n"
        "3. 💳 - Оплата и кредиты: Просмотрите информацию об оплате и кредитах (/payment).\n"
        "4. ⚙️ - Изменить настройки: Измените настройки вашего профиля (/options).\n"
        "5. 🆘 - Тех.поддержка: Обратитесь за технической поддержкой (/support).")
