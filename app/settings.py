import logging
import json
import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

script_directory = os.path.dirname(os.path.abspath(__file__))

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

ANALYSER_SYSTEM_CONTEXT = ('Перескажи вкратце содержание переписки между '
                           'пользователями, с упоминанием имён этих '
                           'пользователей. В ответе не указывать '
                           'id сообщений (message_id).')

try:
    context_path = os.path.join(script_directory, '..', 'context.json')
    with open(context_path, 'r', encoding='utf-8') as f:
        SYSTEM_CONTEXT = json.load(f)
        ANSWERER_SYSTEM_CONTEXT = SYSTEM_CONTEXT['ANSWERER_SYSTEM_CONTEXT']
        ANSWERER_BASE_DIALOGUE = SYSTEM_CONTEXT['ANSWERER_BASE_DIALOGUE']
except Exception:
    ANSWERER_SYSTEM_CONTEXT = 'Ответь на вопрос или просьбу пользователя'
    ANSWERER_BASE_DIALOGUE = []

# Создание / покдлючение БД SQLite
database_path = os.path.join(script_directory, '..', 'messages.db')
connect = sqlite3.connect(database_path)
cur = connect.cursor()

# Лимит на количество сообщений с одного чата для анализа / записи в БД
MESSAGES_LIMIT = 200

# Лимит на количество сообщений в памяти бота
BOT_MESSAGES_LIMIT = 4
