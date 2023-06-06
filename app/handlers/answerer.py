from aiogram import types, Dispatcher

from app.general_functions import only_from_groups, request_to_ai
from app.settings import ANSWERER_SYSTEM_CONTEXT


@only_from_groups
async def answerer(message: types.Message) -> None:
    if message.get_args():
        await message.bot.send_message(chat_id=message.chat.id,
                                       text='Готовлю ответ, пару сек')
        proccessed_text = await request_to_ai(ANSWERER_SYSTEM_CONTEXT,
                                              message.get_args())
        await message.bot.send_message(chat_id=message.chat.id,
                                       text=proccessed_text)
        return

    await message.bot.send_message(chat_id=message.chat.id,
                                   text='После /ask нужно что-то '
                                        'спросить или попросить. '
                                        'Например /ask Где находится солнце?')
    return


async def setup(dp: Dispatcher):
    """
    Registering handlers in Dispatcher.
    """
    dp.register_message_handler(answerer, commands='ask')