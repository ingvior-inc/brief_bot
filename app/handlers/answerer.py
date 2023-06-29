from aiogram import types, Dispatcher

from app.custom_filters import ReplyFilterBot
from app.general_functions import only_from_groups, request_to_ai
from app.settings import (cur, ANSWERER_SYSTEM_CONTEXT,
                          ANSWERER_BASE_DIALOGUE, BOT_MESSAGES_LIMIT)
from . import historian


@only_from_groups
async def answerer(message: types.Message) -> None:
    if message.text.replace(' ', '') == '/ask':
        await message.reply(text='После /ask нужно что-то спросить '
                                 'или попросить.\n'
                                 'Например, /ask Где находится солнце?')
        return

    await historian.bot_historian(message)

    cur.execute(f'SELECT username, message_text '
                f'FROM bot_messages '
                f'WHERE chat_id = {message.chat.id} '
                f'ORDER BY id ASC '
                f'LIMIT {BOT_MESSAGES_LIMIT}')

    memory = (ANSWERER_BASE_DIALOGUE +
              [
                  {'role': 'assistant' if item[0] == 'Bot' else 'user',
                   'content': f"{item[1]}" if item[0] == 'Bot'
                   else f"{item[0]}: {item[1]}"}
                  for item in cur.fetchall()
              ]
              )

    text_to_process = (f'{message.from_user.first_name} '
                       f'({message.from_user.username}): '
                       f'{message.text}')

    proccessed_text = await request_to_ai(ANSWERER_SYSTEM_CONTEXT,
                                          text_to_process,
                                          memory)

    bot_response = await message.reply(text=proccessed_text)

    await historian.bot_historian(bot_response)
    return


async def setup(dp: Dispatcher):
    """
    Registering handlers in Dispatcher.
    """
    dp.register_message_handler(answerer, commands='ask')
    dp.register_message_handler(answerer, ReplyFilterBot())
