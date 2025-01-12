from aiogram import Router, F
from aiogram.types import CallbackQuery

from services.loggers import logger
from services.memory import clear_id_memory

memory_router = Router()


# Декоратор для callback запроса 'clear_memory'
@memory_router.callback_query(F.data == 'clear_memory')
async def handle_callback(callback: CallbackQuery):
    # Удаляем Inline-клавиатуру из сообщения
    # await callback.message.edit_reply_markup(reply_markup=None)
    await clear_id_memory(callback.from_user.id)
    await callback.message.delete()
    await callback.answer()

