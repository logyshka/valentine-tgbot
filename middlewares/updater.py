from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.entities.user import User
import loader

class UserUpdater(BaseMiddleware):
    async def on_pre_process_message(self, message, data):
        if message.text:
            if message.text == "/start":
                if User.is_new(message.from_user.id):
                    User.create(message.from_user.id, message.from_user.username)
        if message.from_user:
            if loader.update_username:
                User(message.from_user.id,  message.from_user.username)
            if loader.update_activity:
                User(message.from_user.id).be_active()