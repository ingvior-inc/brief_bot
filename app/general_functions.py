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
