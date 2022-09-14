import re
from loader import dp
from aiogram.types import Message, CallbackQuery
import states.send_message as states
import keyboards.main as keyboard

from aiogram.dispatcher import FSMContext

send_to = {}

@dp.message_handler(lambda message: message.text == "/start")
async def SEND_VALENTINE(message: Message):
    await message.answer(text="<i>👋🏻 Приветствую тебя</i>\n\n"
                              "<i>👾 Для того, чтобы получать валентинки используй свою персональную ссылку:</i>\n\n"
                              f"<b>https://t.me/{(await dp.bot.get_me()).username}?start={message.from_user.id}</b>\n\n"
                              f"<i>👾 После перехода по ней каждый сможет отправить вам валентинку!</i>",
                         disable_web_page_preview=True)

@dp.message_handler(regexp="/start \d+")
async def SEND_VALENTINE(message: Message):
    user_id = int(re.findall(r"/start (\d+)", message.text)[0])
    try:
        await dp.bot.get_chat(user_id)
        if message.from_user.id != user_id:
            await states.SendMessage.nickname.set()
            send_to[message.from_user.id] = user_id
            await message.answer(text="<i>✒ Введите свой псевдоним</i>\n\n"
                                      "<b>⚠ Если не хочешь, то жми на кнопку снизу, чтобы пропустить</b>",
                                 reply_markup=keyboard.skip_nickname)
        else:
            await message.answer(text=f"<i>⚠ Вы не можете отправить признание самому себе!</i>")

    except:
        bot = (await dp.bot.get_me()).username
        await message.answer(text=f"<i>⚠ Такого пользователя не существует в @{bot}!</i>")
    finally:
        await message.delete()

@dp.message_handler(state=states.SendMessage.nickname)
async def GET_NICKNAME(message: Message, state: FSMContext):
    if message.text != "▶ Пропустить":
        async with state.proxy() as data:
            data["nickname"] = message.text
    await states.SendMessage.next()
    await message.answer(text=f"<i>✒ Введите сообщение для пользователя @{(await dp.bot.get_chat(send_to[message.from_user.id])).username}</i>")

@dp.message_handler(state=states.SendMessage.message)
async def GET_MESSAGE(message: Message, state: FSMContext):
    if len(message.text) < 2000:
        async with state.proxy() as data:
            nickname = data.get("nickname")
            data["message"] = message.text
            if nickname:
                text = "<i>🤨 Вы уверены, что хотите отправить сообщение с текстом:</i>\n\n" + message.text + "\n\n" + \
                        f"🥷🏼 Ваш псевдоним: {nickname}"
            else:
                text = "<i>🤨 Вы уверены, что хотите отправить сообщение с текстом:</i>\n\n" + message.text
            await message.answer(text, reply_markup=keyboard.accept(send_to.get(message.from_user.id)))
    else:
        await message.answer(text=f"<i>⚠ Сообщение может быь длиной до 2000 символов! Попробуйте ещё раз!</i>")

@dp.callback_query_handler(lambda call: "send_message_" in call.data, state=states.SendMessage.message)
async def SEND_MESSAGE(call: CallbackQuery, state: FSMContext):
    user_id = int(call.data.replace("send_message_", ""))
    await call.message.answer(f"<i>✅ Сообщение успешно отправлено пользователю @{(await dp.bot.get_chat(user_id)).username}</i>", reply_markup=keyboard.send_again(user_id))
    async with state.proxy() as data:
        nickname = data.get("nickname")
        message = data.get("message")
    if nickname:
        text = f"""
<i>✅ Вы получили сообщение от человека с псевдонимом <u>{nickname}</u>!</i>\n
<i>◾ Текст сообщения:</i>\n
<b>{message}</b>
        """
    else:
        text = f"""
<i>✅ Вы получили новое сообщение!</i>\n
<i>◾ Текст сообщения:</i>\n
<b>{message}</b>
                """
    await dp.bot.send_message(chat_id=user_id, text=text)
    await state.finish()
    await call.message.delete()

@dp.callback_query_handler(lambda call: "rewrite_message_" in call.data)
async def SEND_MESSAGE(call: CallbackQuery):
    user_id = int(call.data.replace("rewrite_message_", ""))
    await states.SendMessage.nickname.set()
    send_to[call.from_user.id] = user_id
    await call.message.answer(text="<i>✒ Введите свой псевдоним</i>\n\n"
                                   "<b>⚠ Если не хочешь, то жми на кнопку снизу, чтобы пропустить</b>",
                              reply_markup=keyboard.skip_nickname)
    await call.message.delete()