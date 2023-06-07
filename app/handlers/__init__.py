from aiogram import Dispatcher

from . import analyser, historian, answerer


async def setup_all(dp: Dispatcher) -> None:
    """
    Init all setup-functions for registering in Dispatcher.
    """
    await analyser.setup(dp)
    await answerer.setup(dp)
    await historian.setup(dp)
