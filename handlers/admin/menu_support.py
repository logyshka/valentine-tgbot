from aiogram.dispatcher import FSMContext
import keyboards.inline.admin as kb
from utils.entities.admin import Admin
from loader import dp, admin_id, logger
from aiogram.types import CallbackQuery, Message, ContentTypes
from filters import IsAdmin, CallEqual, CallStart
import states.admin as st
from utils.entities.support_message import SupportMessage


@dp.callback_query_handler(CallEqual("menu_support"), IsAdmin())
async def menu_support(call: CallbackQuery):
    await call.message.edit_text(f"<b>🆔 Ваш id: <code>{call.from_user.id}</code></b>\n\n"
                                 f"<b>👨🏼‍💻 Здесь вы можете просматривать сообщения отправленные в тех. поддержку от пользователей и отвечать на них</b>",
                                 reply_markup=kb.menu_support(len(SupportMessage.messages())))


@dp.callback_query_handler(CallEqual("refresh_support_messages"), IsAdmin())
async def refresh_support_messages(call: CallbackQuery):
    try:
        await call.message.edit_text(f"<b>🆔 Ваш id: <code>{call.from_user.id}</code></b>\n\n"
                                     f"<b>👨🏼‍💻 Здесь вы можете просматривать сообщения отправленные в тех. поддержку от пользователей и отвечать на них</b>",
                                     reply_markup=kb.menu_support(len(SupportMessage.messages())))
    except:
        await call.answer("⚠ Всё осталось не изменно!")


@dp.message_handler(commands=["support"])
async def support(message: Message):
    await message.answer("<b>◾ Отправьте боту сообщение для тех. поддержки</b>\n\n"
                         "<i>⚠ Можно отправить только текстовое сообщение!</i>\n\n"
                         "<i>⚠ Флуд, спам, оскорбления и реклама в тех. поддержку = бан в проекте!</i>\n\n")
    await st.Support.send_to.set()


@dp.message_handler(state=st.Support.send_to)
async def support(message: Message, state: FSMContext):
    if message.text:
        message1 = SupportMessage.create(message.from_user, message.text)
        message2 = await message.bot.send_message(chat_id=admin_id,
                                                  text=f"<b>👤 Автор: <code>@{message.from_user.username}</code></b>\n\n"
                                                       f"<b><a href='https://t.me/{message.from_user.username}'>👤 Автор: id{message.from_user.id}</a></b>\n\n"
                                                       f"<b>◾ Текст сообщения: </b>"
                                                       f"<i>{message.text}</i>",
                                                  reply_markup=kb.message_menu(message1.id, message1.from_user.id),
                                                  disable_web_page_preview=True)
        for moder_id in Admin.admins():
            try:
                await message2.copy_to(moder_id)
            except:
                pass
        await message.answer("<b>✅ Тех. поддержка получила ваше сообщение, ожидайте ответа!</b>")
        logger.info(f"user id{admin_id} has sent message to support")
    await state.finish()


@dp.callback_query_handler(CallStart("delete_support_message_"), IsAdmin())
async def delete_support_message(call: CallbackQuery):
    await call.message.edit_reply_markup(None)
    try:
        message = SupportMessage(call.data.replace("delete_support_message_", ""))
        message1 = await call.bot.send_message(chat_id=message.from_user.id,
                                               text=f"<b>📆 Ваше сообщение <code>{message.sending_date}</code></b>\n\n"
                                                    f"<b>◾ Его текст: </b>"
                                                    f"<i>{message.text}</i>")
        await message1.reply("<b>😩 Тех. поддержка прочитала ваше сообщение, но ничего не ответила!</b>")
        SupportMessage.delete(message.id)
    except:
        await call.message.delete()


@dp.callback_query_handler(CallStart("answer_support_message_"), IsAdmin())
async def answer_support_message_(call: CallbackQuery):
    try:
        await call.message.answer("<b>◾ Для отправки вашего ответа, просто ответьте на это сообщение</b>")
        await st.Support.send_from.set()
    except:
        await call.message.delete()


@dp.message_handler(state=st.Support.send_from)
async def send_from(message: Message):
    if message.reply_to_message and message.text:
        chat_id = None
        message_id = None
        for row in message.reply_to_message.reply_markup.inline_keyboard:
            for button in row:
                if button.text == "🗣 Ответить":
                    chat_id = button.callback_data.replace("answer_support_message_", "")
                if button.text == "✅ Прочитано":
                    message_id = button.callback_data.replace("delete_support_message_", "")
        if chat_id:
            message1 = SupportMessage(message_id)
            message2 = await message.bot.send_message(chat_id=chat_id,
                                                      text=f"<b>📆 Ваше сообщение <code>{message1.sending_date}</code></b>\n\n"
                                                           f"<b>◾ Его текст: </b>"
                                                           f"<i>{message1.text}</i>")
            await message2.reply(text="<b>👤 Ответ от тех. поддержки:</b>"
                                      f"<i>{message.text}</i>")
            logger.success(f"{message.from_user.id}: message has been successfully sent to id{message1.from_user.id}")
            SupportMessage.delete(message1.id)
        else:
            await message.answer(
                "<b>◾ Для отправки вашего ответа, просто ответьте на сообщение, на которое необходимо ответить</b>")
    else:
        await message.answer(
            "<b>◾ Для отправки вашего ответа, просто ответьте на сообщение, на которое необходимо ответить</b>")


@dp.callback_query_handler(CallEqual("unlock_support_messages"), IsAdmin())
async def unlock_support_messages(call: CallbackQuery):
    await call.message.edit_reply_markup(kb.menu_support(len(SupportMessage.messages()), locked=False))


@dp.callback_query_handler(CallEqual("lock_support_messages"), IsAdmin())
async def lock_support_messages(call: CallbackQuery):
    await call.message.edit_reply_markup(kb.menu_support(len(SupportMessage.messages())))


@dp.callback_query_handler(CallEqual("locked"), IsAdmin())
async def locked(call: CallbackQuery):
    await call.answer("⚠ Недоступно!")


@dp.callback_query_handler(CallEqual("clean_menu_support"), IsAdmin())
async def clean_menu_support(call: CallbackQuery):
    await call.answer("🕐 Очистка сообщений началась, ожидайте...")
    SupportMessage.clean()
    await call.answer("✅ Очистка успешно завершена!", show_alert=True)
    await call.message.edit_reply_markup(kb.menu_support(len(SupportMessage.messages())))


@dp.callback_query_handler(CallEqual("get_support_messages"), IsAdmin())
async def get_support_messages(call: CallbackQuery):
    await call.message.edit_text(
        "<b>◾ Вот все полученные сообщение, которые не прочитаны, либо оставлены без ответа</b>",
        reply_markup=kb.support_messages(SupportMessage.messages()))


@dp.callback_query_handler(CallStart("open_support_message_"), IsAdmin())
async def get_support_messages(call: CallbackQuery):
    try:
        message = SupportMessage(call.data.replace("open_support_message_", ""))
        await call.message.answer(text=f"<b>👤 Автор: <code>@{message.from_user.username}</code></b>\n\n"
                                       f"<b><a href='https://t.me/{message.from_user.username}'>👤 Автор: id{message.from_user.id}</a></b>\n\n"
                                       f"<b>◾ Текст сообщения: </b>"
                                       f"<i>{message.text}</i>",
                                  reply_markup=kb.message_menu(message.id, message.from_user.id),
                                  disable_web_page_preview=True)
    except:
        try:
            await call.message.edit_reply_markup(reply_markup=kb.support_messages(SupportMessage.messages()))
        except:
            await call.answer("⚠ Что-то пошло не так!")


@dp.callback_query_handler(CallStart("send_message_from_support"), IsAdmin())
async def send_message_from_support(call: CallbackQuery):
    await call.message.answer("<b>◾ Отправьте боту<code> id </code>того, кому хотите отправить сообщение</b>")
    await st.Support.get_aim.set()


@dp.message_handler(state=st.Support.get_aim)
async def send_from(message: Message, state: FSMContext):
    try:
        await message.bot.get_chat(message.text)
        async with state.proxy() as data:
            data["user_id"] = int(message.text)
        await message.answer(f"<b>◾ Введите сообщение для пользователя <code> id{message.text}</code></b>\n\n")
        await st.Support.send_message.set()
    except:
        await message.answer("<b>⚠ Некорректный<code> id </code>пользователя!</b>")
        await state.finish()


@dp.message_handler(state=st.Support.send_message, content_types=ContentTypes.ANY)
async def send_from(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            user_id = data["user_id"]
            message1 = await message.copy_to(chat_id=user_id)
            await message.bot.send_message(chat_id=user_id,
                                           reply_to_message_id=message1.message_id,
                                           text=f"<b>◾ Сообщение от тех. поддержки бота @{(await message.bot.get_me()).username}</b>\n\n"
                                                f"<i>⚠ Для обращение в тех. поддержку бота используйте команду <code>/support</code></i>")
            await message.reply(f"<b>✅ Сообщение успешно отправлено пользователю <code> id{user_id}</code>!</b>")
            logger.success(f"{message.from_user.id}: message has been successfully sent to id{user_id}")
    except:
        await message.answer("<b>⚠ Что-то пошло не так!</b>")
    finally:
        await state.finish()
