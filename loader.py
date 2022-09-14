# -*- coding: utf-8 -*-
from configparser import ConfigParser
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewares.updater import UserUpdater
from utils.entities.agreement import Agreement
from loguru import logger
from utils.misc.path import log_path

settings = ConfigParser()
settings.read("data/settings.ini")

admin_id = int(settings["settings"]["admin_id"])
bot_token = settings["settings"]["bot_token"]
update_username = settings["settings"]["update_username"].lower() in ["true", "yes", "+"]
update_activity = settings["settings"]["update_activity"].lower() in ["true", "yes", "+"]

with open(log_path, "w", encoding="utf-8") as f:
    f.write("")

logger.add(log_path)

bot = Bot(bot_token, parse_mode="html")
dp = Dispatcher(bot, storage=MemoryStorage())
dp.setup_middleware(UserUpdater())

agreement = Agreement()