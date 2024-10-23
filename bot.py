# System
import re
import os
import datetime
from config import TOKEN

# Add app
import telebot
from pytube import YouTube
from pytube import Playlist

# Token in config.py
token = TOKEN

bot = telebot.TeleBot(token)


def writes_logs(_ex):
    """Записывает логи в файл 'logs.log', в котором будет время и ошибка"""
    with open('logs.log', 'a') as file_log:
        file_log.write('\n' + str(datetime.datetime.now()) + ': ' + str(_ex))


def create_video(url):
    """Скачивает видео и открывает файл на бинарное чтение"""
    try:
        yt = YouTube(url).streams.filter(progressive=True, file_extension='mp4').first()
        path = yt.download("videos")  # Скачиваем видео в папку 'videos'
        video = open(path, 'rb')  # Открываем файл на чтение
        return video
    except Exception as _ex:
        writes_logs(_ex)
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
        
        playlist = Playlist(message.text)

        for url in playlist.video_urls:
            try:
                video = create_video(url)
                if video:
                    bot.send_video(message.chat.id, video)
            except Exception as _ex:
                writes_logs(_ex)
                bot.send_message(message.chat.id, f"Ошибка при скачивании видео: {_ex}")
        bot.send_message(message.chat.id, "Плейлист успешно скачан и отправлен.")
    elif re.match(r'(https://www\.youtube\.com/watch\?v=|https://youtu\.be/)', message.text):
        # Для видео
        bot.send_message(message.chat.id, "Начинаю обработку видео...")
        writes_logs("Начинается обработка видео")
        
        try:
            url = message.text
            video = create_video(url)
            if video:
                bot.send_video(message.chat.id, video)
        except Exception as _ex:
            writes_logs(_ex)
            bot.send_message(message.chat.id, f"Ошибка при скачивании видео: {_ex}")
    else:
        bot.send_message(message.chat.id, "Не удалось распознать ссылку. Пожалуйста, проверьте её корректность.")
        writes_logs(f"Не удалось распознать ссылку: {message.text}")


delete_all_videos_in_directory()
bot.infinity_polling()
