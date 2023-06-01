from aiogram import Dispatcher
from aiogram.types import BotCommand

commands = {
    'start': 'Проанализировать последние N сообщений в группе. '
             'Например, /start 30',
}


async def set_commands(dp: Dispatcher) -> None:
    """
    Adding commands and there description to Telegram UI.
    """
    await dp.bot.set_my_commands(
        [BotCommand(command, description)
         for command, description in commands.items()]
    )
