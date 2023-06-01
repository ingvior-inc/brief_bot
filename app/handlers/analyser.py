import logging
import openai

from aiogram import types, Dispatcher

from app.general_functions import only_from_groups
from app.settings import cur, MESSAGES_LIMIT, SYSTEM_CONTEXT


@only_from_groups
async def analyser(message: types.Message) -> None:
    try:
        count_messages = int(message.get_args())

        if MESSAGES_LIMIT >= count_messages >= 10:
            await message.bot.send_message(chat_id=message.chat.id,
                                           text='Читаю ваши буквы, '
                                                'подождите несколько секунд')
            logging.warning(f'{message.chat.title}({message.chat.id}) '
                            f'- успешно вызвана команда /start')

            cur.execute(f'SELECT username, message '
                        f'FROM messages '
                        f'WHERE chat_id = {message.chat.id} '
                        f'ORDER BY id DESC '
                        f'LIMIT {count_messages}')

            text_to_proccess = ('\n'.join(f'{item[0]}: {item[1]}'
                                for item in reversed(cur.fetchall())))

            proccessed_text = await request_to_ai(text_to_proccess)

            await message.bot.send_message(chat_id=message.chat.id,
                                           text=proccessed_text)

        else:
            logging.error(f'{message.chat.title}({message.chat.id}) '
                          f'- Попытка превысить лимит')
            await message.bot.send_message(chat_id=message.chat.id,
                                           text=f'После /start укажите '
                                                f'число от 10 до '
                                                f'{MESSAGES_LIMIT}')

    except ValueError:
        logging.error(f'{message.chat.title}({message.chat.id}) '
                      f'- Некорректный вызов команды /start')
        await message.bot.send_message(chat_id=message.chat.id,
                                       text='После /start должно идти число')


async def request_to_ai(text_to_proccess: str) -> str:

    response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                            messages=[
                                                {'role': 'system',
                                                 'content': SYSTEM_CONTEXT},
                                                {'role': 'user',
                                                 'content': text_to_proccess}
                                            ],
                                            temperature=0.7)

    if 'choices' in response:
        choices = response['choices']
        if len(choices) > 0 and 'message' in choices[0]:
            ai_response_text = choices[0]['message']['content']
            return ai_response_text

    logging.error(response)
    return 'Что-то не так с AI :('


async def setup(dp: Dispatcher):
    """
    Registering handlers in Dispatcher.
    """
    dp.register_message_handler(analyser, commands='start')
