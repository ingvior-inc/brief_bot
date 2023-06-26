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

# Токен OpenAI
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
# Модель OpenAI
OPENAI_MODEL = 'gpt-3.5-turbo-16k-0613'
ANALYSER_SYSTEM_CONTEXT = os.getenv('ANALYSER_SYSTEM_CONTEXT')
ANSWERER_SYSTEM_CONTEXT = os.getenv('ANSWERER_SYSTEM_CONTEXT')

# Создание / покдлючение БД SQLite
connect = sqlite3.connect('./messages.db')
cur = connect.cursor()

# Лимит на количество сообщений с одного чата для анализа / записи в БД
MESSAGES_LIMIT = 200

# Лимит на количество сообщений в памяти бота
BOT_MESSAGES_LIMIT = 4
