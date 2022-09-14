from data.database import Table, INT, TEXT, DATE, TIME
from utils.misc.path import db_path

db_channels = Table(name="channels",
                    db_path=db_path + "channels.db").create(
        channel_id=INT,
        invite_link=TEXT)

db_admins = Table(name="admins",
                  db_path=db_path + "admins.db").create(admin_id=INT)

db_users = Table(name="users", db_path=db_path + "users.db").create(
        user_id=INT,
        username=TEXT,
        reg_date=DATE,
        banned_for=TIME,
        last_activity=TIME,
        agreement=INT)

db_sending = Table(name="sending",
                   db_path=db_path + "sending.db").create(
        start_time=TIME,
        end_time=TIME,
        during=TIME,
        success=INT,
        failure=INT)

db_support_message = Table(name="support",
                           db_path=db_path + "support_message.db").create(
        from_id=INT,
        from_username=TEXT,
        sending_date=TIME,
        text=TEXT,
        unique_id=INT)