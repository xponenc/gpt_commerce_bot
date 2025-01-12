# from google.cloud import speech  # pip install google-cloud-speech
# from google.cloud import texttospeech   # pip install google-cloud-texttospeech
import asyncio
import io
import sys
from concurrent.futures import thread

import aiohttp
import openai
from openai import OpenAI
from pydub import AudioSegment
from io import BytesIO
from aiogram import Bot
from aiogram.types import Voice, BufferedInputFile
from dotenv import load_dotenv
import os

load_dotenv()

# Для использования сервиса Google Cloud - TTS и STT
# Нужна регистрация на https://cloud.google.com/ и активация услуг,
# после этого нужно будет скачать и использовать сервисный json файл
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GOOGLE_SERVICE_JSON')
# client_google_STT = speech.SpeechClient()
# client_google_TTS = texttospeech.TextToSpeechClient()

# Для использования TTS от Yandex https://auth.yandex.cloud/login
api_key_yandex = os.getenv('YANDEX_API_KEY')
folder_id_yandex = os.getenv('YANDEX_FOLDER_ID')

client = OpenAI()


# FFMPEG добавление пути
FFMPEG_PATH = os.path.join(r"d:\\", "ffmpeg", "bin")
os.environ["PATH"] = FFMPEG_PATH + os.pathsep + os.environ["PATH"]


async def tts_acting(text_message: str,
                     user_options: dict,
                     name_psychologist: str = 'Татьяна',
                     voice_servise='yandex'):
    if user_options['audio']:  # if True
        speaking_rate = user_options.get('speed', 1)
        voice_female = True if name_psychologist in ["Татьяна",  # женские имена в базе психологов
                                                     "Марина",
                                                     "Анна",
                                                     "Ольга",
                                                     "Елена"] else False
        # TTS Google
        if voice_servise == 'google':
            pass
            # voice_answer = await tts_google(text_message,
            #                                 speaking_rate=speaking_rate,
            #                                 voice_female=voice_female)
        # TTS Yandex
        else:
            voice_answer = await tts_yandex(text_message,
                                            speaking_rate=speaking_rate,
                                            voice_female=voice_female)

        return BufferedInputFile(file=voice_answer.read(),
                                 filename="message.mp3")  # Это логическое имя, не требующее физического файла


# async def tts_google(text,
#                      speaking_rate=1,
#                      voice_female=True,
#                      client=client_google_TTS):
#     input_text = texttospeech.SynthesisInput(text=text)
#     # https://cloud.google.com/text-to-speech/docs/voices
#     name = "ru-RU-Wavenet-E" if voice_female else "ru-RU-Wavenet-D"
#     voice = texttospeech.VoiceSelectionParams(
#         language_code="ru-RU",
#         name=name)
#     audio_config = texttospeech.AudioConfig(
#         speaking_rate=speaking_rate,
#         volume_gain_db=6,
#         audio_encoding=texttospeech.AudioEncoding.MP3)
#     response = client.synthesize_speech(input=input_text,
#                                         voice=voice,
#                                         audio_config=audio_config)
#     audio_stream = BytesIO(response.audio_content)
#     audio_stream.seek(0)  # Возвращаем указатель в начало потока
#     return audio_stream


async def tts_yandex(text,
                     speaking_rate=1,
                     voice_female=True,
                     api_key=api_key_yandex,
                     folder_id=folder_id_yandex):
    voice = "jane" if voice_female else "madirus"
    # URL для синтеза речи через Yandex Speech API
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    # Заголовки для авторизации с использованием API-токена
    headers = {"Authorization": f"Api-Key {api_key}"}
    # Параметры запроса для синтеза речи
    data = {'text': text,
            'lang': 'ru-RU',
            'voice': voice,
            'folderId': folder_id,
            'format': 'lpcm',
            'sampleRateHertz': 48000,
            'emotion': "good",
            'speed': speaking_rate}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Ошибка синтеза речи: {resp.status}, {await resp.text()}")
            raw_audio = BytesIO(await resp.read())
    # Преобразуем RAW в OGG
    audio = AudioSegment.from_file(
        raw_audio, format="raw", frame_rate=48000, channels=1, sample_width=2)
    ogg_audio = BytesIO()
    audio.export(ogg_audio, format="ogg", codec="libopus")
    ogg_audio.seek(0)  # Возвращаем указатель в начало
    return ogg_audio  # тип BytesIO


# Голосовое сообщение пользователя в текст
async def stt_acting(bot: Bot,
                     message: Voice,
                     model: str = "whisper-1"):
    file_id = message.voice.file_id
    file_info = await bot.get_file(file_id=file_id)
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp", "voice_msgs")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_name = os.path.join(temp_dir, f"audio_{file_id}.ogg")
    file = await bot.download_file(file_info.file_path, file_name)
    if model == "whisper-1":
        return await stt_whisper(audio_file=file_name)
    os.remove(file_name)

    return await stt_google(file)


# async def stt_google(voice,
#                      client=client_google_STT):
#     audio = speech.RecognitionAudio(content=voice.getvalue())
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
#         sample_rate_hertz=48000,
#         language_code="ru-RU")
#     response = client.recognize(config=config, audio=audio)
#     for result in response.results:
#         return result.alternatives[0].transcript

import tempfile


async def stt_whisper(audio_file):
    with open(file=audio_file, mode="rb") as f:
        print(audio_file)
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text",
            # timestamp_granularities=["word"],
        )
        print(transcription)
        return transcription
