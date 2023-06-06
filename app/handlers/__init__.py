from aiogram import Dispatcher

from . import chat_analyser, historian, answerer


async def setup_all(dp: Dispatcher) -> None:
    """
    Init all setup-functions for registering in Dispatcher.
    """
    await chat_analyser.setup(dp)
    await answerer.setup(dp)
    await historian.setup(dp)
