import logging

import openai
from aiogram import Dispatcher, executor

from app import handlers
from app.settings import BOT, OPENAI_TOKEN
from app.commands import set_commands


async def on_startup(dp: Dispatcher):
    logging.warning('Setting handlers...')
    await handlers.setup_all(dp)
    logging.warning('Setting commands...')
    await set_commands(dp)


async def on_shutdown(dp: Dispatcher):
    logging.warning('Shutting down..')

    await dp.storage.close()
    await dp.storage.wait_closed()

    await BOT.delete_webhook()
    logging.warning('Webhook down')


if __name__ == '__main__':
    dp = Dispatcher(BOT)
    openai.api_key = OPENAI_TOKEN
    try:
        executor.start_polling(dp, on_startup=on_startup,
                               skip_updates=True)
    except Exception as E:
        logging.error(f'An error occurred while launching the bot - {E}')
