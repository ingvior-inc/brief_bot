import logging

import openai.error
from aiogram import types, Dispatcher

from app.general_functions import only_from_groups, request_to_ai
from app.settings import (cur, ANALYSER_SYSTEM_CONTEXT, MESSAGES_LIMIT,
                          INCORRECT_VALUE_MESSAGE)


@only_from_groups
async def chat_analyser(message: types.Message) -> None:
    try:
        count_messages = int(message.get_args())

        if MESSAGES_LIMIT >= count_messages >= 10:
            await message.reply(text='Читаю ваши буквы, '
                                     'подождите несколько секунд')
            logging.warning(f'{message.chat.title}({message.chat.id}) '
                            f'- успешно вызвана команда /start')

            cur.execute(f'SELECT message_id, username, message_text '
                        f'FROM messages '
                        f'WHERE chat_id = {message.chat.id} '
                        f'ORDER BY id DESC '
                        f'LIMIT {count_messages}')

            text_to_proccess = ('\n'.join(f'(message_id {item[0]}) {item[1]}: '
                                          f'{item[2]}'
                                for item in reversed(cur.fetchall())))

            try:
                proccessed_text = await request_to_ai(ANALYSER_SYSTEM_CONTEXT,
                                                      text_to_proccess)
            except openai.error.InvalidRequestError:
                proccessed_text = ('Слишком много анализировать :( '
                                   'Давай поменьше')

            await message.bot.send_message(chat_id=message.chat.id,
                                           text=proccessed_text)
            return

        logging.error(f'{message.chat.title}({message.chat.id}) '
                      f'- Попытка превысить лимит')
        await message.bot.send_message(chat_id=message.chat.id,
                                       text=INCORRECT_VALUE_MESSAGE)
        return

    except ValueError:
        logging.error(f'{message.chat.title}({message.chat.id}) '
                      f'- Некорректный вызов команды /start')
        await message.bot.send_message(chat_id=message.chat.id,
                                       text=INCORRECT_VALUE_MESSAGE)
        return


async def setup(dp: Dispatcher):
    """
    Registering handlers in Dispatcher.
    """
    dp.register_message_handler(chat_analyser, commands='start')
