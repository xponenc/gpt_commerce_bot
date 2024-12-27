from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.types import Message

from db_models.service_gpt_history_table import write_data_to_table
from gpt import gpt_chat

gpt_router = Router()


@gpt_router.message(F.text)
async def message_with_text(message: Message):
    session_data = [{
        "message": message.text,
        "user_id": message.from_user.id,
        "date_time": message.date.replace(tzinfo=None),
    }]

    answer = gpt_chat(user_msg=message.text, )
    if answer:
        session_data.append({
            "message": answer,
            "user_id": message.from_user.id,
            "date_time": datetime.now(timezone.utc).replace(tzinfo=None),
            "is_bot_msg": True
        })
        await message.answer(answer)

    await write_data_to_table(data=session_data)
