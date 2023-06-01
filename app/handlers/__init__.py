from aiogram import Dispatcher

from . import analyser, historian


async def setup_all(dp: Dispatcher) -> None:
    """
    Init all setup-functions for registering in Dispatcher.
    """
    await analyser.setup(dp)
    await historian.setup(dp)
