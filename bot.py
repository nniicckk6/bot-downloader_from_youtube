# System
import re
import os
import datetime
from config import TOKEN

# Add app
import telebot
import yt_dlp

# Token in config.py
token = TOKEN
bot = telebot.TeleBot(token)

def writes_logs(_ex):
    """Записывает логи в файл 'logs.log', в котором будет время и ошибка"""
    with open('logs.log', 'a') as file_log:
        file_log.write('\n' + str(datetime.datetime.now()) + ': ' + str(_ex))

def create_video(url):
    """Скачивает видео и возвращает файл на бинарное чтение"""
    ydl_opts = {
        'format': 'best',  # Выбор наилучшего качества
        'outtmpl': 'videos/%(title)s.%(ext)s',  # Шаблон для имени файла
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            video_file_path = os.path.join('videos', f"{video_title}.mp4")  # Путь к файлу видео
            writes_logs(f"Скачано видео: {video_title}")
            return open(video_file_path, 'rb')  # Открываем файл на чтение
    except Exception as _ex:
        writes_logs(f"Ошибка при создании видео: {url} - {_ex}")
        return None

def delete_all_videos_in_directory():
    """Удаляет все скаченные видео из папки 'videos'"""
    if not os.path.exists('videos'):
        os.mkdir('videos')
    for file in os.listdir('videos'):
        try:
            if re.search('mp4', file):
                mp4_path = os.path.join('videos', file)
                os.remove(mp4_path)
        except Exception as _ex:
            writes_logs(_ex)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Стартовое приветствие"""
    bot.send_message(message.chat.id, "Привет ✌\nПришли мне ссылку на плейлист или видео с YouTube!")

@bot.message_handler(content_types=['text'])
def get_files(message):
    """Ждёт от пользователя ссылку на ютуб плейлист или видео и начинает его скачивать, и отравляет пользователю"""
    # Логируем ссылку для отладки
    writes_logs(f"Получена ссылка: {message.text}")

    if re.match(r'https://www\.youtube\.com/playlist\?list=', message.text):
        # Для плейлиста
        bot.send_message(message.chat.id, "Начинаю обработку плейлиста...")
        writes_logs("Начинается обработка плейлиста")

        playlist = yt_dlp.YoutubeDL().extract_info(message.text, download=False)  # Получаем информацию о плейлисте
        for video in playlist['entries']:
            try:
                url = video['url']
                video_file = create_video(url)
                if video_file:
                    bot.send_video(message.chat.id, video_file)
                else:
                    bot.send_message(message.chat.id, "Не удалось скачать видео.")
            except Exception as _ex:
                writes_logs(f"Ошибка при отправке видео: {url} - {_ex}")
                bot.send_message(message.chat.id, f"Ошибка при скачивании видео: {_ex}")
        bot.send_message(message.chat.id, "Плейлист успешно обработан.")

    elif re.match(r'(https://www\.youtube\.com/watch\?v=|https://youtu\.be/)', message.text):
        # Для видео
        bot.send_message(message.chat.id, "Начинаю обработку видео...")
        writes_logs("Начинается обработка видео")

        try:
            url = message.text
            video_file = create_video(url)
            if video_file:
                bot.send_video(message.chat.id, video_file)
            else:
                bot.send_message(message.chat.id, "Не удалось скачать видео.")
        except Exception as _ex:
            writes_logs(f"Ошибка при отправке видео: {url} - {_ex}")
            bot.send_message(message.chat.id, f"Ошибка при скачивании видео: {_ex}")
    else:
        bot.send_message(message.chat.id, "Не удалось распознать ссылку. Пожалуйста, проверьте её корректность.")
        writes_logs(f"Не удалось распознать ссылку: {message.text}")

delete_all_videos_in_directory()
bot.infinity_polling()