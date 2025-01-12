from datetime import datetime, timezone

from aiogram import Router, F, Bot
from aiogram.types import Message, Voice

from models.service_gpt_history_table import write_data_to_table
from services.loggers import logger
from services.process_gpt import gpt_chat, answer_gpt_memory
from services.process_options import get_user_options
from services.process_tts_stt import tts_acting, stt_acting
from services.prompts import prompts

gpt_router = Router()


# Обработка голосового сообщения пользователя психологу
@gpt_router.message(F.voice)
async def voice_msg_psy(message: Voice, bot: Bot, ):
    user_options = await get_user_options(message.from_user.id)
    # data = await state.get_data()
    # name_psychologist = data['name_psychologist']
    name_psychologist = "Татьяна"
    system_psy = prompts[name_psychologist]['system']
    add_psy = prompts[name_psychologist]['user']
    logger.info(
        f'Voice message from user {message.from_user.id} to Psy {name_psychologist}')

    msg = await message.answer('Обработка голосового сообщения...')
    text_from_voice = await stt_acting(bot=bot, message=message, model="whisper-1")
    await msg.edit_text(f'Ваше сообщение психологу: {text_from_voice}')
    session_data = [{
        "message": text_from_voice,
        "user_id": message.from_user.id,
        "date_time": message.date.replace(tzinfo=None),
    }]
    await write_data_to_table(data=session_data)

    msg2 = await message.answer('Формирование ответа...')
    answer_gpt = await answer_gpt_memory(message.from_user.id,
                                         system_psy,
                                         add_psy,
                                         text_from_voice,
                                         model='gpt-4o-mini',
                                         temp=user_options['temperature'])
    sent_message = await msg2.edit_text(answer_gpt)

    session_data = [{
        "message": answer_gpt,
        "user_id": message.from_user.id,
        "date_time": sent_message.date.replace(tzinfo=None),
        "is_bot_msg": True
    }]
    await write_data_to_table(data=session_data)

    # Озвучка ответа психолога
    voice_file = await tts_acting(answer_gpt, user_options, name_psychologist)
    if voice_file:
        await message.answer_voice(voice_file)


@gpt_router.message(F.text)
async def message_with_text(message: Message):
    session_data = [{
        "message": message.text,
        "user_id": message.from_user.id,
        "date_time": message.date.replace(tzinfo=None),
    }]
    await write_data_to_table(data=session_data)
    msg2 = await message.answer('Формирование ответа...')
    user_options = await get_user_options(message.from_user.id)
    model_temperature = user_options.get("temperature", 0)
    # answer = gpt_chat(user_msg=message.text, model_temperature=model_temperature)
    name_psychologist = "Татьяна"
    system_psy = prompts[name_psychologist]['system']
    add_psy = prompts[name_psychologist]['user']
    answer_gpt = await answer_gpt_memory(message.from_user.id,
                                         system_psy,
                                         add_psy,
                                         message.text,
                                         model='gpt-4o-mini',
                                         temp=model_temperature)
    sent_message = await msg2.edit_text(answer_gpt)
    session_data = [{
        "message": answer_gpt,
        "user_id": message.from_user.id,
        "date_time": sent_message.date.replace(tzinfo=None),
        "is_bot_msg": True
    }]
    await write_data_to_table(data=session_data)
    # Озвучка ответа gpt
    voice_file = await tts_acting(answer_gpt, user_options, name_psychologist)
    if voice_file:
        await message.answer_voice(voice_file)