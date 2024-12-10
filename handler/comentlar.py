from aiogram import Router, F
from handler.states import Admin
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from data.sqliteClas import SQLiteBaza
from handler.button import admin_button
from aiogram.fsm.state import State, StatesGroup

coment_router = Router()
baza = SQLiteBaza("imtihon.db")

class Izohlar(StatesGroup):
    javob_yozish = State()
    sorash = State()


@coment_router.callback_query(F.data,Admin.comentlar)
async def CommentlarRead(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if len(baza.read("coment","*"))>1:
        if xabar.split("-")[0]=="javob":
            await state.update_data(id=xabar.split('-')[1])
            await state.update_data(tgid=xabar.split("-")[-1])
            await call.message.answer(text="Izohga yozmoqchi bo'lgan fikringizni kirting!")
            await state.set_state(Izohlar.javob_yozish)
        elif xabar.split("-")[0]=="ochir":
            baza.delete("coment",manzil_name=f"id = {xabar.split("-")[1]}")
            await call.message.answer(text="Izoh o'chirildi!")
            await state.set_state(Admin.comentlar)
    else:
        await call.message.answer(text="Izoh qolmadi",reply_markup=admin_button)
        await state.set_state(Admin.start)
    await call.message.delete()

@coment_router.message(F.text, Izohlar.javob_yozish)
async def JavobYuborish(message:Message,state:FSMContext):
    xabar = message.text
    data = await state.get_data()
    await message.bot.send_message(chat_id=int(data.get("tgid")), text=f"Siz qoldirgan izohga kelgan javob:\n{xabar}")
    baza.delete("coment",manzil_name=f"id = {int(data.get("id"))}")
