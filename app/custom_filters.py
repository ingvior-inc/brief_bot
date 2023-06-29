from aiogram import filters, types


class ReplyFilterBot(filters.BoundFilter):
    async def check(self, message: types.Message):
        try:
            if message.reply_to_message.from_user.is_bot:
                return True
        except Exception:
            pass
