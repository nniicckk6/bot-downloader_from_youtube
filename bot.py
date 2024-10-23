import re
import os
import datetime
from config import TOKEN
import telebot
from pytube import YouTube
from pytube import Playlist
import yt_dlp

# Token in config.py
token = TOKEN
bot = telebot.TeleBot(token)

def writes_logs(_ex):
    """Записывает логи в файл 'logs.log', в котором будет время и ошибка"""
    with open('logs.log', 'a') as file_log:
        file_log.write('\n' + str(datetime.datetime.now()) + ': ' + str(_ex))

def clean_filename(filename):
    """Очищает имя файла от нежелательных символов"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def create_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Выбор наилучшего качества
        'outtmpl': 'videos/%(title)s.%(ext)s',  # Шаблон для имени файла
        'merge_output_format': 'mp4',  # Слияние аудио и видео в mp4
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        # Получаем информацию о скачанном видео
        info_dict = ydl.extract_info(url, download=False)
        video_title = clean_filename(info_dict.get('title', 'video'))
        video_ext = info_dict.get('ext', 'mp4')
        path = f'videos/{video_title}.{video_ext}'  # Полный путь к видео

    # Проверяем, существует ли файл
    if os.path.exists(path):
        video = open(path, 'rb')
        return video, path  # Возвращаем путь к видео
    else:
        writes_logs(f"Файл не найден: {path}")
        return None, path

def delete_all_videos_in_directory():
    """Удаляет все скаченные видео из папки 'videos'"""
    if not os.path.exists('videos'):
        os.mkdir('videos')
    for file in os.listdir('videos'):
        try:
            if re.search(r'\.mp4$', file):  # Проверяем расширение
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
    writes_logs(f"Получена ссылка: {message.text}")

    if re.match(r'https://www\.youtube\.com/playlist\?list=', message.text):
        # Для плейлиста
        bot.send_message(message.chat.id, "Начинаю обработку плейлиста...")
        writes_logs("Начинается обработка плейлиста")

        playlist = Playlist(message.text)

        for url in playlist.video_urls:
            try:
                video, path = create_video(url)
                if video:
                    bot.send_video(message.chat.id, video)
                    video.close()  # Закрываем файл
                    os.remove(path)  # Удаляем файл после отправки
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
            video, path = create_video(url)
            if video:
                bot.send_video(message.chat.id, video)
                video.close()  # Закрываем файл
                os.remove(path)  # Удаляем файл после отправки
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