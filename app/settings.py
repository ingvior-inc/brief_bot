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
ANALYSER_SYSTEM_CONTEXT = os.getenv('ANALYSER_SYSTEM_CONTEXT')
ANSWERER_SYSTEM_CONTEXT = os.getenv('ANSWERER_SYSTEM_CONTEXT')

# Покдлючение к БД SQLite
connect = sqlite3.connect('messages.db')
cur = connect.cursor()

# Лимит на количество сообщений с одного чата для анализа / записи в БД
MESSAGES_LIMIT = 200

# Лимит на количество сообщений в памяти бота
BOT_MESSAGES_LIMIT = 6

INCORRECT_VALUE_MESSAGE = (f'После /start укажите число N '
                           f'(от 10 до {MESSAGES_LIMIT}) , где N - '
                           f'количество последних сообщений в группе, '
                           f'содержание которых нужно кратко пересказать')
