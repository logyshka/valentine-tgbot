from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


skip_nickname = ReplyKeyboardMarkup(one_time_keyboard=True,
                                    resize_keyboard=True,
                                    row_width=1).add(
    "▶ Пропустить"
)

skip_nickname2 = ReplyKeyboardRemove()

def accept(user_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("✉ Отправить", callback_data=f"send_message_{user_id}"),
        InlineKeyboardButton("♻ Заново", callback_data=f"rewrite_message_{user_id}")
    )

def send_again(user_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("✉ Отправить ещё", callback_data=f"rewrite_message_{user_id}")
    )