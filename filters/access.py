from aiogram.dispatcher.filters import Filter
from aiogram.types import Message, CallbackQuery

from utils.entities.admin import Admin
from utils.entities.channel import Channel
from utils.entities.user import User
from loader import dp, admin_id, logger, agreement


class IsMember(Filter):
    async def check(self, obj) -> bool:
        user_id = obj.from_user.id
        if user_id == admin_id or user_id in Admin.admins():
            return False
        for channel_id in Channel.channels():
            try:
                user = await obj.bot.get_chat_member(chat_id=channel_id[0], user_id=user_id)
                if not user.is_chat_member() and not (user.is_chat_admin() or user.is_chat_creator()):
                    return True
            except: pass
        return False


class AcceptAgreement(Filter):
    async def check(self, obj) -> bool:
        if not bool(agreement):
            return False
        if isinstance(obj, Message) or isinstance(obj, CallbackQuery):
            if User(obj.from_user.id).agreement:
                return False
            return True
        return False