from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from filters import IsAdmin, IsMember, CallEqual, CallStart
from loader import dp, admin_id, logger
import keyboards.inline.admin as kb
from utils.entities.channel import Channel, ChannelLimitError, ChannelExistsError, BotAdminError
import states.admin as st


@dp.callback_query_handler(CallEqual("menu_channels"), IsAdmin())
async def menu_channels(call: CallbackQuery):
    await call.message.edit_text(f"<b>🆔 Ваш id: {call.from_user.id}</b>\n\n"
                                 f"<b>◾ Вы админ, вы можете добавлять/удалять каналы вашего проекта</b>\n\n"
                                 f"<b>◾ Лимит каналов в проекте<code> 5 </code></b>")
    await call.message.edit_reply_markup(kb.menu_channels([[i[0], "locked"] for i in Channel.channels()]))


@dp.callback_query_handler(CallEqual("add_channel"), IsAdmin())
async def add_channel(call: CallbackQuery):
    await call.answer("◾ Введите id канала, которого хотите добавить", show_alert=True)
    await st.Channel.add.set()


@dp.message_handler(IsAdmin(), state=st.Channel.add)
async def add_channel(message: Message, state: FSMContext):
    try:
        channel_id = int(message.text)
        await Channel.add(channel_id=channel_id, bot=dp.bot)
        await message.answer(f"<b>✅ Канал успешно добавлен!</b>\n\n"
                             f"<b>📢 Название канала<code>{(await dp.bot.get_chat(channel_id)).full_name}</code></b>")
        logger.success(f"{message.from_user.id}: channel {channel_id} has been added")
    except ChannelExistsError:
        await message.answer("<b>⚠ Канал не был добавлен!</b>\n\n"
                             "<i>🤷‍♂ Причина:</i><code> канал уже в списке добавленных</code>")
    except ChannelLimitError:
        await message.answer("<b>⚠ Канал не был добавлен!</b>\n\n"
                             "<i>🤷‍♂ Причина:</i><code> вы достигли лимита 5/5</code>")
    except BotAdminError:
        await message.answer("<b>⚠ Канал не был добавлен!</b>\n\n"
                             "<i>🤷‍♂ Причина:</i><code> бот не является админом канала</code>")
    except Exception:
        await message.answer("<b>⚠ Канал не был добавлен!</b>\n\n"
                             "<i>🤷‍♂ Причина:</i><code> некорректный id канала</code>")
    finally:
        await state.finish()
        await message.delete()


@dp.callback_query_handler(CallEqual("refresh_channel"), IsAdmin())
async def refresh_channel(call: CallbackQuery):
    try:
        await call.message.edit_reply_markup(kb.menu_channels([[i[0], "locked"] for i in Channel.channels()]))
    except Exception:
        await call.answer("⚠ Ничего не изменилось!")


@dp.callback_query_handler(CallStart("unlock_delete_channel_"), IsAdmin())
async def unlock_delete_channel(call: CallbackQuery):
    channels = []
    for i in Channel.channels():
        if i[0] == int(call.data.replace("unlock_delete_channel_", "")):
            channels.append([i[0], "unlocked"])
        else:
            channels.append([i[0], "locked"])
    await call.message.edit_reply_markup(kb.menu_channels(channels))


@dp.callback_query_handler(CallEqual("channel_locked"), IsAdmin())
async def channel_locked(call: CallbackQuery):
    await call.answer("Не доступно!")


@dp.callback_query_handler(CallStart("delete_channel_"), IsAdmin())
async def delete_channel(call: CallbackQuery):
    channel_id = int(call.data.replace("delete_channel_", ""))
    Channel.delete(channel_id)
    await call.message.edit_reply_markup(kb.menu_channels([[i, "locked"] for i in Channel.channels()]))
    logger.success(f"{call.from_user.id}: channel {channel_id} has been deleted")


@dp.message_handler(IsMember())
async def is_not_member(message: Message):
    await message.answer("<b>⚠ Для работы с ботом вы должны быть подписаны на каналы ниже</b>\n\n"
                         "<b>⌨ После подписки нажмите на кнопку проверки</b>",
                         reply_markup=kb.subscribe_channels(Channel.channels()))


@dp.callback_query_handler(IsMember())
async def is_not_member(call: CallbackQuery):
    if call.data == "accept_subscription":
        await call.answer("⚠ Не пытайся меня обмануть!")
    else:
        await call.message.answer("<b>⚠ Для работы с ботом вы должны быть подписаны на каналы ниже</b>\n\n"
                                  "<b>⌨ После подписки нажмите на кнопку проверки</b>",
                                  reply_markup=kb.subscribe_channels(Channel.channels()))


@dp.callback_query_handler(CallEqual("accept_subscription"))
async def accept_subscription(call: CallbackQuery):
    await call.message.answer("<b>✅ Вы успешно подписались на необходимые каналы!</b>\n\n"
                              "<b>⌨ Для использования бота введите /start</b>")
    await call.message.delete()
