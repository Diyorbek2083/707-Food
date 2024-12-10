from aiogram import Router, F
from handler.button import admin_add, admin_button
from handler.states import Admin
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from handler.funksya import AdminReadButtons
from aiogram.fsm.state import State, StatesGroup
from data.sqliteClas import SQLiteBaza


class Add(StatesGroup):
    add = State()
    sorash = State()
    remov = State()


sorash_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"Ha ✅", callback_data="ha"), InlineKeyboardButton(text="Yo'q ❌", callback_data="yoq")]
    ]
)

baza = SQLiteBaza("imtihon.db")
admin_router = Router()

@admin_router.callback_query(F.data,Admin.add_admin)
async def AdminAddMenu(call:CallbackQuery, state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
        await call.message.answer(text="Siz adminsiz!", reply_markup=admin_button)
        await state.set_state(Admin.start)
    if xabar=="add_admin":
        await state.update_data(why=xabar)
        await call.message.answer(text="Qo'shmoqchi bo'lgan admining telegram raqamini yuboring")
        await state.set_state(Add.add)
    if xabar=="remov_admin":
        await state.update_data(why=xabar)
        await call.message.answer(text="Qaysi admini o'chirmoqchisiz?", reply_markup=AdminReadButtons())
        await state.set_state(Add.remov)
    await call.message.delete()

#### Botga admin qo'shish
@admin_router.message(F.contact,Add.add)
async def AdminQoshish(message:Message, state:FSMContext):
    xabar = message
    await state.update_data(id=message.contact.user_id)
    await state.update_data(nomi=message.contact.first_name)
    await state.update_data(raqam=message.contact.phone_number)
    await message.answer(text=f"Telegram raqam: {message.contact.phone_number}\nNomi: {message.contact.first_name}\nId: {message.contact.user_id}\n\nRostan ham bu teleramni admin qilmoqchimisiz?", reply_markup=sorash_button)
    await state.set_state(Add.sorash)


#### Botdan admin o'chirish
@admin_router.callback_query(F.data,Add.remov)
async def AdminRemov(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
        await call.message.answer(text="Nima qilmoqchisiz? 🤔", reply_markup=admin_add)
        await state.set_state(Admin.add_admin)
    else:
        for i in baza.read("admins","*"):
            if i[0]==int(xabar):
                if i[1]!=6378609931:
                    await state.update_data(id=i[0])
                    await call.message.answer(text=f"Telegram raqam: {i[-1]}\nNomi: {i[2]}\nId: {i[1]}\n\nRostan ham bu admin o'chirmoqchimisiz?", reply_markup=sorash_button)
                    await state.set_state(Add.sorash)
                else:
                    await call.message.answer(text="Bu adminni o'chirib bo'lmaydi‼️\nIltimos boshqatdan urining ko'ring", reply_markup=AdminReadButtons())
                    await state.set_state(Add.remov)
    await call.message.delete()


@admin_router.callback_query(F.data,Add.sorash)
async def QoshishniSorash(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if data.get("why")=="add_admin":
        baza.insert("admins",tg_id=int(data.get("id")),name=f"{data.get("nomi")}",number=f"{data.get("raqam")}")
        await call.message.answer(text="Admin bazaga qo'shildi!", reply_markup=admin_button)
        await state.set_state(Admin.start)
    if data.get("why")=="remov_admin":
        baza.delete("admins",f"id = {data.get("id")}")
        await call.message.answer(text="Admin o'chirildi",reply_markup=admin_button)
        await state.set_state(Admin.start)
    await call.message.delete()