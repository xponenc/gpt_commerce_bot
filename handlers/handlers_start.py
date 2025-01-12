from aiogram.types import Message, BotCommand
from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from handlers.handlers_psychologist import PSYCHOLOGIST_COMMANDS
from services.loggers import logger
from services.memory import clear_id_memory
from services.users import set_new_user


# Создание экземпляра класса Router, который будет управлять маршрутами
start_router = Router()


BASE_COMMANDS = {
    "start": {
        "name": "Старт",
        "info": "начать работу со мной"},
}

START_COMMANDS = BASE_COMMANDS.copy()
START_COMMANDS.update(PSYCHOLOGIST_COMMANDS)


@start_router.startup()
async def set_menu_button(bot: Bot):
    # Определение основных команд для главного меню - кнопка (Menu) слева внизу
    main_menu_commands = [
        BotCommand(command=f'/{key}', description=value.get("name", "")) for key, value in START_COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)


# /start
@start_router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await clear_id_memory(message.from_user.id)
    await set_new_user(message)
    logger.info(f"Start new session for user {message.from_user.id}")
    await message.answer(
        "В нашем боте Вам доступны следующие опции:\n\n" +
        "\n".join(f"{value.get("info")} (/{key})." for key, value in PSYCHOLOGIST_COMMANDS.items())
        )
