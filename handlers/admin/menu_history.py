import keyboards.inline.admin as kb
from utils.entities.sending import Sending
from utils.entities.user import User
from loader import dp, admin_id, logger, log_path
from aiogram.types import CallbackQuery
from filters import IsAdmin, CallEqual
from utils.entities.statistic import Statistic

@dp.callback_query_handler(CallEqual("menu_history"), IsAdmin())
async def menu_history(call: CallbackQuery):
    await call.message.edit_text(f"<b>🆔 Ваш id: <code>{call.from_user.id}</code></b>\n\n"
                                 "<b>🗃 Вы админ, вы можете выгружать полную информацию о проекте</b>",
                                 reply_markup=kb.menu_history())

@dp.callback_query_handler(CallEqual("menu_history_users"), IsAdmin())
async def menu_history_users(call: CallbackQuery):
    await call.message.answer(f"<b>✅ Началась выгрузка данных из БД</b>\n\n"
                              f"<i>⚠ Необходимо выгрузить<code> {len(User.users())} строк</code>, это может занять много времени!</i>")
    await call.message.answer_document(document=User.collect_data((await call.bot.me).username),
                                       caption="<b>✅ Данные о пользователях успешно выгружены из БД!</b>")

@dp.callback_query_handler(CallEqual("menu_history_sendings"), IsAdmin())
async def menu_history_users(call: CallbackQuery):
    await call.message.answer(f"<b>✅ Началась выгрузка данных из БД</b>\n\n"
                              f"<i>⚠ Необходимо выгрузить<code> {len(Sending.sendings())} строк</code>, это может занять много времени!</i>")
    await call.message.answer_document(document=Sending.collect_data((await call.bot.me).username),
                                       caption="<b>✅ Данные о пользователях успешно выгружены из БД!</b>")


@dp.callback_query_handler(CallEqual("menu_history_general"), IsAdmin())
async def menu_history_users(call: CallbackQuery):
    await call.message.answer(f"<b>✅ Началась выгрузка статистики из БД</b>\n\n"
                              f"<i>⚠ Сбор полной статистики может занять много времени!</i>")
    await call.message.answer_document(document=Statistic.collect_general(),
                                       caption="<b>✅ Статистика успешно выгружена из БД!</b>")

@dp.callback_query_handler(CallEqual("menu_history_income"), IsAdmin())
async def menu_history_users(call: CallbackQuery):
    await call.message.answer(f"<b>✅ Началась выгрузка данных из БД</b>\n\n"
                              f"<i>⚠ Это может занять много времени!</i>")
    await call.message.answer_document(document=Statistic.collect_income(),
                                       caption="<b>✅ Данные о приходе новых пользователей успешно выгружены из БД!</b>")

@dp.callback_query_handler(CallEqual("menu_history_log"), IsAdmin())
async def menu_history_users(call: CallbackQuery):
    await call.message.answer(f"<b>✅ Началась выгрузка данных из БД</b>\n\n"
                              f"<i>⚠ Это может занять много времени!</i>")
    with open(log_path, "rb") as log_file:
        await call.message.answer_document(document=log_file,
                                           caption="<b>✅ Данные о приходе новых пользователей успешно выгружены из БД!</b>")