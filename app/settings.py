import json
import logging
import os
import sqlite3

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

script_directory = os.path.dirname(os.path.abspath(__file__))

# Logging settings
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%d.%m.%Y, %H:%M:%S')

# Telegram Bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')
# Bot object
BOT = Bot(token=BOT_TOKEN)

OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
OPENAI_MODEL = 'gpt-3.5-turbo-16k-0613'

ANALYSER_SYSTEM_CONTEXT = ('Перескажи вкратце содержание переписки между '
                           'пользователями, с упоминанием имён этих '
                           'пользователей. В ответе не указывать '
                           'id сообщений (message_id).')

context_path = os.path.join(script_directory, '..', 'context.json')

if not os.path.exists(context_path):
    default_context = {
        "MESSAGES_LIMIT": 100,
        "BOT_MESSAGES_LIMIT": 4,
        "ANSWERER_SYSTEM_CONTEXT": "Ответь на вопрос или просьбу пользователя",
        "ANSWERER_BASE_DIALOGUE": []
    }
    with open(context_path, 'w', encoding='utf-8') as f:
        json.dump(default_context, f, ensure_ascii=False, indent=4)

with open(context_path, 'r', encoding='utf-8') as f:
    SYSTEM_CONTEXT = json.load(f)
    # Лимит на количество сообщений с одного чата для анализа / записи в БД
    MESSAGES_LIMIT = SYSTEM_CONTEXT['MESSAGES_LIMIT']
    # Лимит на количество сообщений в памяти бота (диалог с юзером)
    BOT_MESSAGES_LIMIT = SYSTEM_CONTEXT['BOT_MESSAGES_LIMIT']
    # Описание личности бота
    ANSWERER_SYSTEM_CONTEXT = SYSTEM_CONTEXT['ANSWERER_SYSTEM_CONTEXT']
    # Диалог с ботом с ответами, которые должны соответствовать личности
    ANSWERER_BASE_DIALOGUE = SYSTEM_CONTEXT['ANSWERER_BASE_DIALOGUE']

# Создание / покдлючение БД SQLite
database_path = os.path.join(script_directory, '..', 'messages.db')
connect = sqlite3.connect(database_path)
cur = connect.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS messages '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'chat_id INTEGER NOT NULL,'
            'message_id INTEGER NOT NULL,'
            'username TEXT NOT NULL,'
            'message_text TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS bot_messages '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'chat_id INTEGER NOT NULL,'
            'username TEXT NOT NULL,'
            'message_text TEXT)')
