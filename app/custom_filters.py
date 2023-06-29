from aiogram import filters, types

from app.settings import BOT


class ReplyFilterBot(filters.BoundFilter):
    async def check(self, message: types.Message):
        try:
            if message.reply_to_message.from_user.id == BOT.id:
                return True
        except Exception:
            pass
