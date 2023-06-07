import logging

import openai
from aiogram import types


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


async def request_to_ai(system_context: str, text_to_proccess: str) -> str:
    """
    Отправляет запрос в OpenAI с указанием системного контекста (роль GPT в
    обработке текста + сам текст).
    """
    try:
        response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                                messages=[
                                                    {'role': 'system',
                                                     'content':
                                                         system_context},
                                                    {'role': 'user',
                                                     'content':
                                                         text_to_proccess}
                                                ],
                                                temperature=0.9)

        if 'choices' in response:
            choices = response['choices']
            if len(choices) > 0 and 'message' in choices[0]:
                ai_response_text = choices[0]['message']['content']
                return ai_response_text

        logging.error(response)
        return 'Что-то не так с AI :('

    except openai.error.RateLimitError:
        return 'Перегружен запросами. Обратитесь позже please'
