import logging

from aiogram import types, Dispatcher

from app.general_functions import only_from_groups
from app.settings import connect, cur, MESSAGES_LIMIT


@only_from_groups
async def historian(message: types.Message) -> None:
    """
    Функция записывает все сообщения из групп Telegram в базу данных.
    """
    cur.execute('CREATE TABLE IF NOT EXISTS messages '
                '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'chat_id INTEGER NOT NULL,'
                'username TEXT NOT NULL,'
                'message TEXT)')

    await check_db_limit(chat_id=message.chat.id)

    user_profile_name = (f'{message.from_user.first_name} '
                         f'({message.from_user.username})')

    cur.execute(f"INSERT INTO messages(chat_id, username, message) VALUES "
                f"({message.chat.id}, '{user_profile_name}', "
                f"'{message.text}')")
    connect.commit()


async def check_db_limit(chat_id: int) -> None:
    """
    Проверяет, достигло ли число записей в конкретном чате Telegram
    произвольного лимита. При его достижении удаляет все
    старые записи за рамками этого самого лимита.
    """
    cur.execute(f'SELECT COUNT(*) FROM messages WHERE chat_id = {chat_id}')
    rows_count = cur.fetchone()[0]

    if rows_count > MESSAGES_LIMIT:
        cur.execute(f'DELETE FROM messages '
                    f'WHERE chat_id = {chat_id} '
                    f'AND id NOT IN (SELECT id FROM messages '
                    f'               WHERE chat_id = {chat_id}'
                    f'               ORDER BY id DESC'
                    f'               LIMIT {MESSAGES_LIMIT})')
        connect.commit()


async def setup(dp: Dispatcher):
    """
    Registering handlers in Dispatcher.
    """
    dp.register_message_handler(historian)
