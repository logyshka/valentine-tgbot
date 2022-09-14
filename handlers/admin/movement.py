from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from loader import dp, admin_id, logger
from filters import AdminCommand, IsAdmin, CallEqual
import keyboards.inline.admin as kb

@dp.message_handler(AdminCommand(), IsAdmin())
async def open_menu(message: Message):
    status = "владелец" if message.from_user.id == admin_id else "админ"
    await message.answer(f"<b>👋🏻 Приветствую тебя, <u>{message.from_user.full_name}</u></b>\n\n"
                         f"<b>◾ Ваш статус: <code>{status}</code></b>\n\n"
                         "<i>🖥 Пользуйтесь админ-панелью с удовольствием</i>\n\n"
                         "<i>♻ Admin-panel by @KamaaPyla</i>",
                         reply_markup=kb.menu())
    await message.delete()

@dp.callback_query_handler(CallEqual("to_menu"), IsAdmin())
async def to_menu(call: CallbackQuery):
    status = "владелец" if call.from_user.id == admin_id else "админ"
    await call.message.edit_text(f"<b>👋🏻 Приветствую тебя, <u>{call.from_user.full_name}</u></b>\n\n"
                                 f"<b>◾ Ваш статус: <code>{status}</code></b>\n\n"
                                 "<i>🖥 Пользуйтесь админ-панелью с удовольствием</i>\n\n"
                                 "<i>♻ Admin-panel by @KamaaPyla</i>",
                                 reply_markup=kb.menu())

@dp.callback_query_handler(CallEqual("close"), state="*")
async def close(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()