# Используйте официальный образ Python как родительский образ
FROM python:3.12

# Устанавливаем рабочую директорию для контейнера
WORKDIR /proj/psy_bot

# Скопируйте файлы требований и установите зависимости
COPY requirements.txt ./
RUN apt update -y
RUN apt install ffmpeg -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте текущий каталог в рабочую директорию внутри контейнера
COPY . .

# Дополнительные полезные шаги (для уменьшения размера образа)
RUN apt-get clean

# Запуск приложения при запуске контейнера
CMD ["python", "bot.py"]