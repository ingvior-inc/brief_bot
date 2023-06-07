from aiogram import types, Dispatcher

from app.general_functions import only_from_groups, request_to_ai
from app.settings import ANSWERER_SYSTEM_CONTEXT
from . import historian


@only_from_groups
async def answerer(message: types.Message) -> None:
    if message.get_args():
        text_to_process = (f'{message.from_user.first_name} '
                           f'({message.from_user.username}): '
                           f'{message.get_args()}')

        proccessed_text = await request_to_ai(ANSWERER_SYSTEM_CONTEXT,
                                              text_to_process)

        await historian.chat_historian(message)

        response_text = await message.reply(text=proccessed_text)

        await historian.chat_historian(response_text)
        return

    await message.reply(text='После /ask нужно что-то '
                             'спросить или попросить. '
                             'Например /ask Где находится солнце?')
    return


async def setup(dp: Dispatcher):
    """
    Registering handlers in Dispatcher.
    """
    dp.register_message_handler(answerer, commands='ask')
