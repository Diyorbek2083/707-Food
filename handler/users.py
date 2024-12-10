from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from data.sqliteClas import SQLiteBaza
from handler.states import Admin
from handler.button import admin_button, add_remov_replay, admin_add,malumotlar
from data.db_bot import UsersId, users, admins, AdminsId
from handler.funksya import AdminAndUserButton, JavobYozish
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
baza = SQLiteBaza("imtihon.db")


@router.message(CommandStart())
async def StartBot(message:Message,state:FSMContext):
    xabar = message.text
    if message.from_user.id in [i[1] for i in baza.read("admins","*")]:
        await message.answer(text=f"Assalomu aleykum {message.from_user.first_name}\nSiz adminsiz!", reply_markup=admin_button)
        await state.set_state(Admin.start)
    else:
        await message.answer_photo(photo="AgACAgIAAxkBAAIK0GdVZSEERnHTSCRZLUtE6PRodCzLAAK05zEbn7KpSj6qe6XDtATbAQADAgADeAADNgQ", caption=f"Assalomu aleykum {message.from_user.first_name}",reply_markup=AdminAndUserButton(id=message.from_user.id))
        if message.from_user.id not in AdminsId() and message.from_user.id not in UsersId():
            baza.insert("users", tg_id=message.from_user.id, user=message.from_user.full_name)    
        await state.set_state(Admin.tek_button)
    await message.delete()

@router.callback_query(F.data, Admin.start)
async def StartAdmin(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="send_reklama":
        await call.message.answer(text="Reklamaning rasmini yuboring")
        await state.set_state(Admin.reklama)
    if xabar=="add_remov_replay_button":
        await call.message.answer(text="Nima qilmoqchisiz? 🤔", reply_markup=add_remov_replay)
        await state.set_state(Admin.add_button)
    if xabar=="add_remov_replay_admin":
        await call.message.answer(text="Nima qilmoqchisiz? 🤔", reply_markup=admin_add)
        await state.set_state(Admin.add_admin)
    if xabar=="see_button":
        await call.message.answer_photo(photo="AgACAgIAAxkBAAIK0GdVZSEERnHTSCRZLUtE6PRodCzLAAK05zEbn7KpSj6qe6XDtATbAQADAgADeAADNgQ", caption="Siz adminsiz‼️\nQaysi knopkani tekshirmoqchsiz⁉️", reply_markup=AdminAndUserButton(id=call.from_user.id))
        await state.set_state(Admin.tek_button)
    if xabar=="izohlar":
        if len(baza.read("coment","*"))>1:
            for i in baza.read("coment","*"):
                await call.answer()
    if xabar=="izohlar":
        if len(baza.read("coment","*"))>1:
            buton = InlineKeyboardBuilder()
            for i in baza.read('coment',"*"):
                if i[0]!=4:
                    await call.message.answer(text=f"{i[2]}ning izohi:\n{i[-1]}\n\nJavob yozasizmi yoki o'chirib tashlaysizmi?",reply_markup=JavobYozish(id=i[0],tg_id=i[1]))
            await state.set_state(Admin.comentlar)
        else:
            await call.answer("Hozircha izohlar yo'q")
            await call.message.answer(text="Siz adminsiz!", reply_markup=admin_button)
            await state.set_state(Admin.start)
    if xabar=="bot_malumot":
        a=0
        for i in baza.read("malumotlar","*"):
            a+=1
        if a>0:
            for i in baza.read("malumotlar","*"):
                if i[0]==1:
                    await state.update_data(nomer=i[1])
                    await state.update_data(tg=i[2])
                    await state.update_data(insta=i[3])
                    await state.update_data(kanal=i[4])
                    await call.message.answer(text=f"Telefon raqam: {i[1]}\nTelegram: {i[2]}\nInstagram: {i[3]}\nBizning kanal: {i[4]}\n\nQaysi malumotlarni o'zgartirmoqchisiz?",reply_markup=malumotlar)
            await state.set_state(Admin.bot_malumotlar)
        else:
            await call.message.answer(text="Bot malumotlari hali qo'shilmagan iltimos oldin malumot qo'shing\n\nTelefon raqam kiriting\nBunga o'xshash: +998 01 234 56 78")   
            await state.set_state(Admin.bot_malumotlar_add)
    await call.message.delete()
