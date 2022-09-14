import datetime
import data
from prettytable import PrettyTable
from utils.misc.path import temp_path
from aiogram.types import InputFile
from utils.entities.smart_time import Time


class User:

    def __init__(self, user_id, username=None):
        self.id = int(user_id)

        if username:
            self.update_username(username)

    @classmethod
    def is_new(cls, user_id):
        if len(data.db_users.get("*", user_id=user_id)) == 0:
            return True
        return False

    @classmethod
    def create(cls, user_id, username):
        data.db_users.insert(
            user_id=user_id,
            username=username,
            reg_date=datetime.date.today(),
            banned_for=datetime.datetime(1, 1, 1, 1, 1, 1),
            last_activity=datetime.datetime.now(),
            agreement=0
        )

    @property
    def reg_date(self):
        return datetime.date.fromisoformat(data.db_users.get("reg_date", user_id=self.id)[0][0])

    @property
    def agreement(self):
        return data.db_users.get("agreement", user_id=self.id)[0][0] == 1

    @property
    def banned_for(self):
        return datetime.datetime.fromisoformat(data.db_users.get("banned_for", user_id=self.id)[0][0]).replace(microsecond=0)

    @property
    def last_activity(self):
        return datetime.datetime.fromisoformat(data.db_users.get("last_activity", user_id=self.id)[0][0]).replace(microsecond=0)

    @property
    def username(self):
        return "@" + data.db_users.get("username", user_id=self.id)[0][0]

    @property
    def online(self):
        if (datetime.datetime.now() - self.last_activity).total_seconds() > 300:
            return True
        return False

    def be_active(self):
        data.db_users.set("last_activity", datetime.datetime.now(), user_id=self.id)

    def get_ban(self, hours):
        data.db_users.set("banned_for", datetime.datetime.now() + datetime.timedelta(hours=int(hours)), user_id=self.id)

    def get_unban(self):
        data.db_users.set("banned_for", datetime.datetime(1, 1, 1, 1, 1, 1), user_id=self.id)

    def update_username(self, username):
        data.db_users.set("username", username, user_id=self.id)

    def accept_agreement(self):
        data.db_users.set("agreement", 1, user_id=self.id)

    @classmethod
    def count(cls):
        return len(data.db_users.get_all())

    @classmethod
    def is_banned(cls, user_id):
        return User(user_id).banned_for > datetime.datetime.now()

    @classmethod
    def collect_data(cls, proj_name):
        table = PrettyTable(["№", "ID", "Nickname", "Дата регистрации", "Последняя активность", "Забанен до"])
        table.title = f"Данные о пользователях проекта @{proj_name}"
        table.set_style(15)
        table.encoding = "utf-8"
        i = 0
        for user in data.db_users:
            i += 1
            table.add_row([
                i, user[0], user[1], user[2],
                "был в сети " + str(Time(datetime.datetime.fromisoformat(user[4]))) + " назад",
                user[3] if datetime.datetime.fromisoformat(user[3]) > datetime.datetime.now() else "не забанен"
            ])
        _path = temp_path + "users_info.txt"
        with open(_path, "w", encoding = "utf-8") as f:
            f.write(str(table))
        return InputFile(_path)

    @classmethod
    def users(cls):
        return data.db_users.get_all()