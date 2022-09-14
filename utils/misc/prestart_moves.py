from aiogram.types import BotCommand
from loader import admin_id, logger, update_activity, update_username

async def prestart_moves(dp):
    await dp.bot.send_message(chat_id=admin_id,
                              text="<b>✅ Бот успешно запущен!</b>\n\n"
                                   "<i>⚠️ Это сообщение получили только вы!</i>")
    await dp.bot.set_my_commands([
        BotCommand("/start", "▶️ Запустить бота"),
        BotCommand("/support", "📨 Написать в тех. поддержку")
    ])
    logger.success(f"{(await dp.bot.get_me()).username} has been started")
    logger.info(f"User id{admin_id} was authorized as MAIN ADMIN")
    logger.info(f"Updating usernames is turn {'ON' if update_username else 'OFF'}")
    logger.info(f"Updating activity is turn {'ON' if update_activity else 'OFF'}")