from aiogram.types import Message
from utils.misc.path import settings_path, temp_path
import configparser


class Agreement:

    def __init__(self):
        self.path = temp_path + "agreement.txt"

    @property
    def message(self) -> str:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            with open(self.path, "w", encoding="utf-8") as f:
                return ""

    def edit_message(self, message: Message):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(message.text)

    @classmethod
    def turn_on(cls):
        config = configparser.ConfigParser()
        config.read(settings_path)
        config["settings"]["agreement"] = "true"
        with open(settings_path, "w") as f:
            config.write(f)

    @classmethod
    def turn_off(cls):
        config = configparser.ConfigParser()
        config.read(settings_path)
        config["settings"]["agreement"] = "false"
        with open(settings_path, "w") as f:
            config.write(f)


    def __bool__(self):
        config = configparser.ConfigParser()
        config.read(settings_path)
        agreement = config["settings"]["agreement"]
        return agreement == "true" and self.message != ""