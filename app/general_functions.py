import logging

import openai
from aiogram import types

from app.settings import OPENAI_MODEL


def only_from_groups(func):
    """
    Декоратор.
    Проверяет, пришло ли сообщение из группы Telegram.
    В личке и в каналах бот не работает.
    """
    async def wrapper(message: types.Message):
        if message.chat.type in ('group', 'supergroup'):
            return await func(message)
    return wrapper


async def request_to_ai(system_context: str, text_to_proccess: str,
                        memory: list = None) -> str:
    """
    Отправляет запрос в OpenAI с указанием системного контекста (роль GPT в
    обработке текста + сам текст).
    """
    if memory is None:
        memory = []

    messages = [
        {'role': 'system',
         'content': system_context}
                ]
    for i in memory:
        messages.append(i)

    messages.append({'role': 'user', 'content': text_to_proccess})

    try:
        response = openai.ChatCompletion.create(model=OPENAI_MODEL,
                                                messages=messages,
                                                temperature=0.9)

        if 'choices' in response:
            choices = response['choices']
            if len(choices) > 0 and 'message' in choices[0]:
                ai_response_text = choices[0]['message']['content']
                return ai_response_text

        logging.error(response)
        return ('Что-то не так с парсингом ответа OpenAI :(\n'
                'Обратитесь к дебичу, который это кодил')

    except openai.error.RateLimitError:
        return ('Перегружен запросами.\n'
                'Попробуйте ещё раз позже')

    except openai.error.InvalidRequestError:
        return ('Что-то не так со структурой запроса в OpenAI '
                '(некорректные параметры, слишком объёмные данные и т.д.).\n'
                'Обратитесь к дебичу, который это кодил')

    except Exception as E:
        logging.error(E)
        return ('Что-то не так с серверами OpenAI :(\n'
                'Попробуйте ещё раз позже')
