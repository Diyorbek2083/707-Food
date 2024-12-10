from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from handler.states import Admin
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.db_bot import UsersId, AdminsId
from handler.button import admin_button


reklama_router = Router()


class Reklama(StatesGroup):
    tag_xabar = State()
    sorash = State()

reklama = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"Ha ✅", callback_data="ha"), InlineKeyboardButton(text="Yo'q ❌", callback_data="yoq")]
    ]
)

@reklama_router.message(Admin.reklama)
async def ReklamaBot(message:Message,state:FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data({"photo":photo})
    await message.answer_photo(photo=photo, caption="Reklama")
    await message.answer(text="Tagiga qo'yiladigan malumotlarni kirting!")
    await state.set_state(Reklama.tag_xabar)
    await message.delete()

@reklama_router.message(Reklama.tag_xabar)
async def TagXabar(message:Message,state:FSMContext):
    xabar = message.text
    await state.update_data({"matn":xabar})
    data = await state.get_data()
    await message.answer_photo(photo=f"{data.get("photo")}", caption=xabar)
    await message.answer(text="Rostan ham bu reklamani yuborishni hohlaysizmi?", reply_markup=reklama)
    await state.set_state(Reklama.sorash)
    await message.delete()
@reklama_router.callback_query(Reklama.sorash)
async def ReklamaSorash(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar=="ha":
        for i in UsersId():
            await call.bot.send_photo(chat_id=i, photo=f"{data.get("photo")}", caption=f"{data.get("matn")}")
            await call.message.answer(text="Reklama yuborildi!", reply_markup=admin_button)
            await state.set_state(Admin.start)
    elif xabar=="yoq":
        await call.message.answer(text="Reklama yuborish bekor qilindi", reply_markup=admin_button)
        await state.set_state(Admin.start)
    await call.message.delete()