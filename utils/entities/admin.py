from data import db_admins
from utils.exceptions.admin import AdminExistsError, AdminLimitError
from loader import dp, admin_id, logger


class Admin:

    @classmethod
    def count(cls):
        return len(db_admins)

    @classmethod
    def is_new(cls, user_id):
        if db_admins.get("*", admin_id=int(user_id)):
            return False
        return True

    @classmethod
    def add(cls, user_id):
        if not cls.is_new(admin_id=user_id):
            raise AdminExistsError
        if cls.count() >= 5:
            raise AdminLimitError
        db_admins.insert(admin_id=int(user_id))

    @classmethod
    def delete(cls, user_id):
        if cls.is_new(user_id):
            raise AdminExistsError
        db_admins.delete(admin_id=int(user_id))

    @classmethod
    def admins(cls):
        admins = [i[0] for i in db_admins.get_all()]
        admins.append(admin_id)
        return admins