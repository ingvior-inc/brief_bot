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
SYSTEM_CONTEXT = ('Перескажи вкратце содержание переписки между '
                  'пользователями, с упоминанием имён этих пользователей')

# Покдлючение к БД SQLite
connect = sqlite3.connect('messages.db')
cur = connect.cursor()

# Лимит на количество сообщений с одного чата для анализа / записи в БД
MESSAGES_LIMIT = 150
