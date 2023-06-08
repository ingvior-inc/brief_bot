import logging
import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

# Настройки логгирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%d.%m.%Y, %H:%M:%S')

# Токен бота Telegram
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Токен OPENAI (chatGPT)
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
ANALYSER_SYSTEM_CONTEXT = ('Перескажи вкратце содержание переписки между '
                           'пользователями, с упоминанием имён '
                           'этих пользователей.'
                           'В ответе не указывать id сообщений (message_id).')
ANSWERER_SYSTEM_CONTEXT = ('Дай ответ на вопрос или просьбу пользователя '
                           'в стиле злого философа-извращенца.')

# Покдлючение к БД SQLite
connect = sqlite3.connect('messages.db')
cur = connect.cursor()

# Лимит на количество сообщений с одного чата для анализа / записи в БД
MESSAGES_LIMIT = 200

INCORRECT_VALUE_MESSAGE = (f'После /start укажите число N '
                           f'(от 10 до {MESSAGES_LIMIT}) , где N - '
                           f'количество последних сообщений в группе, '
                           f'содержание которых нужно кратко пересказать')
