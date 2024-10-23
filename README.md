## Бот скачает ваше видео с YouTube или весь плейлист видеороликов

### Для использования:

* Получить токен бота:

Ссылка как получить токен: https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token

* Клонировать репозиторий:

```
git clone https://github.com/nniicckk6/bot-downloader_from_youtube.git
```

* Перейти в репозиторий:

```
cd bot-downloader_from_youtube
```

* Запустить виртуальную среду

```
python -m venv venv
```

* Активировать

```
venv\Scripts\activate
```

* Скачать все зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

* Запустить бота через консоль или через файл

#### Возможная ошибка, что python не будет находить декоратор, эта проблема решается с помощью установления нового виртуального окружения и скачивания всех зависимостей
#### P.s. : Если у вас слабый интернет, то загрузка файлов в телеграм возможно будет долгая или телеграм api выдаст ошибку
#### Можно использовать для простого быстрого скачивания аудио с ютуб, если не загружать в телеграм
#### Сделал для себя, тк слушаю музыку на ютубе и уже накопился большой плейлист, хотел как-то проявлять свой интерес к музыке без использования интернета, вот и быстро написал бота
