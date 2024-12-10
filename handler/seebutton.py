from aiogram import Router, F
from handler.funksya import AdminAndUserButton, ProductUser, MaxsulotSoni, Karzinkalar
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from handler.states import Admin 
from aiogram.fsm.context import FSMContext
from handler.button import admin_button, contact, lacation
from data.sqliteClas import SQLiteBaza
from aiogram.fsm.state import State, StatesGroup



class Tekshirish(StatesGroup):
    comment = State()
    izoh_yuborish = State()
    tasdiqlash = State()
    ovqat_tanlash = State()
    maxsulot_soni = State()
    savat = State()
    cantakt = State()
    lacatsia = State()



reklama = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"Ha ✅", callback_data="ha"), InlineKeyboardButton(text="Yo'q ❌", callback_data="yoq")]
    ]
)

coments = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Izoh qoldirish 💬",callback_data="izoh_qoldirish"), InlineKeyboardButton(text="◀️ Orqaga",callback_data="orqaga")]
    ]
)

baza = SQLiteBaza("imtihon.db")
see_router = Router()

###### User start and Admin see
@see_router.callback_query(F.data,Admin.tek_button)
async def AdminTekshirish(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
        await call.message.answer(text="Siz adminsiz!", reply_markup=admin_button)
        await state.set_state(Admin.start)
    elif xabar=="boglanish":
        for i in baza.read("malumotlar","*"):
                if i[0]==1:
                    await call.message.answer(text=f"📞 Telefon raqam: {i[1]}\n✉️ Telegram: {i[2]}\n🔴 Instagram: {i[3]}\n👥 Bizning kanal: {i[4]}\n\nBot haqidagi fikringizni yozib qoldiring ✍️",reply_markup=coments)
        await state.set_state(Tekshirish.comment)

    elif xabar=="zakaz_berish":
        if call.from_user.id in [i[1] for i in baza.read("savat","*")]:
            savat = ""
            a = 1
            summasi = 0
            for i in baza.read("savat","*"):
                if i[1]==call.from_user.id:
                    savat += f"{a}.Nomi: {i[3]}\nNarxi: {i[4]} so'm\nSoni: {i[-1]} ta\nUmumiy: {i[4]*i[-1]} so'm,\n\n"
                    summasi += i[4]*i[-1]
                    a += 1
            await state.update_data(shop=savat)
            await state.update_data(summa=summasi)
            await call.message.answer(text=f"Savatdagi maxsulotlar:\n\n{savat}Umumiy narxi: {summasi} so'm",reply_markup=Karzinkalar(id=call.from_user.id))
            await state.set_state(Tekshirish.savat)
        else:
            await call.answer("savat hali bo'sh")
            await call.message.answer_photo(photo="AgACAgIAAxkBAAIK0GdVZSEERnHTSCRZLUtE6PRodCzLAAK05zEbn7KpSj6qe6XDtATbAQADAgADeAADNgQ", caption=f"Savatda hali hechnima yo'q",reply_markup=AdminAndUserButton(id=call.from_user.id))
            await state.set_state(Admin.tek_button)

    elif int(xabar.split("-")[-1]) in [i[0] for i in baza.read("categoriya",'*')]:
        await state.update_data(cat_id=int(xabar.split("-")[-1]))
        for i in baza.read("categoriya","*"):
            if int(xabar.split("-")[-1])==int(i[0]):
                await call.message.answer_photo(photo=f"{i[-1]}", reply_markup=ProductUser(int(i[0])))
        await state.set_state(Tekshirish.ovqat_tanlash)
    await call.message.delete() 

######  Savat funksiyasi
@see_router.callback_query(F.data, Tekshirish.savat)
async def SavatniTekshirish(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
        await call.message.answer_photo(photo="AgACAgIAAxkBAAIK0GdVZSEERnHTSCRZLUtE6PRodCzLAAK05zEbn7KpSj6qe6XDtATbAQADAgADeAADNgQ", caption=f"707 STREET FOOD dan buyurtma berishingiz mumkin",reply_markup=AdminAndUserButton(id=call.from_user.id))
        await state.set_state(Admin.tek_button)
    elif xabar=="✔️ Zakaz berish":
        await call.message.answer(text="Iltimos raqamingizni yuboring", reply_markup=contact)
        await state.set_state(Tekshirish.cantakt)
    elif xabar=="🛒 Savatni tozalash":
        baza.delete("savat", manzil_name=f"tg_id = {call.from_user.id}")
        await call.message.answer_photo(photo="AgACAgIAAxkBAAIK0GdVZSEERnHTSCRZLUtE6PRodCzLAAK05zEbn7KpSj6qe6XDtATbAQADAgADeAADNgQ", caption=f"Savatda maxsulot qolmadi",reply_markup=AdminAndUserButton(id=call.from_user.id))
        await state.set_state(Admin.tek_button)
    else:
        if int(xabar)!=1:
            baza.delete("savat",manzil_name=f"id = {int(xabar)}")
            if call.from_user.id in [i[1] for i in baza.read("savat","*")]:
                savat = ""
                a = 1
                summasi = 0
                for i in baza.read("savat","*"):
                    if i[1]==call.from_user.id and i[0]!=1:
                        savat += f"{a}.Nomi: {i[3]}\nNarxi: {i[4]} so'm\nSoni: {i[-1]} ta\nUmumiy: {i[4]*i[-1]} so'm,\n\n"
                        summasi += i[4]*i[-1]
                        a += 1
                await state.update_data(shop=savat)
                await state.update_data(summa=summasi)
                await call.message.answer(text=f"Savatdagi maxsulotlar:\n\n{savat}Umumiy narxi: {summasi} so'm",reply_markup=Karzinkalar(id=call.from_user.id))
                await state.set_state(Tekshirish.savat)
            else:
                await call.message.answer_photo(photo="AgACAgIAAxkBAAIK0GdVZSEERnHTSCRZLUtE6PRodCzLAAK05zEbn7KpSj6qe6XDtATbAQADAgADeAADNgQ", caption=f"Savatda maxsulot qolmadi",reply_markup=AdminAndUserButton(id=call.from_user.id))
                await state.set_state(Admin.tek_button)
        else:
            await call.message.answer(text="Bu maxsulotni o'chirib bo'lmaydi")
            if call.from_user.id in [i[1] for i in baza.read("savat","*")]:
                savat = ""
                a = 1
                summasi = 0
                for i in baza.read("savat","*"):
                    if i[1]==call.from_user.id and i[0]!=1:
                        savat += f"{a}.Nomi: {i[3]}\nNarxi: {i[4]} so'm\nSoni: {i[-1]} ta\nUmumiy: {i[4]*i[-1]} so'm,\n\n"
                        summasi += i[4]*i[-1]
                        a += 1
                await state.update_data(shop=savat)
                await state.update_data(summa=summasi)
                await call.message.answer(text=f"Savatdagi maxsulotlar:\n\n{savat}Umumiy narxi: {summasi} so'm",reply_markup=Karzinkalar(id=call.from_user.id))
                await state.set_state(Tekshirish.savat)
    await call.message.delete()

###### Zakaz berish
@see_router.message(F.contact,Tekshirish.cantakt)
async def ContactUlash(message:Message,state:FSMContext):
    xabar = message.contact.phone_number
    await state.update_data(can=xabar)
    await message.answer(text="Lactsiya yuboring", reply_markup=lacation)
    await state.set_state(Tekshirish.lacatsia)
    await message.delete()

@see_router.message(F.location, Tekshirish.lacatsia)
async def LacationUlashish(message:Message,state:FSMContext):
    la = message.location.latitude
    lo = message.location.longitude
    data = await state.get_data()
    await message.answer(text=f"Buyirtma qabul qilindi curier yo'lga chiqdi\nSizning chekingiz\n\n{data.get("shop")}Umumiy summa: {data.get("summa")} so'm")
    await message.answer_photo(photo="AgACAgIAAxkBAAIK0GdVZSEERnHTSCRZLUtE6PRodCzLAAK05zEbn7KpSj6qe6XDtATbAQADAgADeAADNgQ", caption=f"707 STREET FOOD dan buyurtma berishingiz mumkin",reply_markup=AdminAndUserButton(id=message.from_user.id))
    await state.set_state(Admin.tek_button)
    await message.bot.send_message(chat_id=6378609931, text=f"Sizga zakaz keldi: \n\nIsmi: {message.from_user.first_name}\nTel raqam: {data.get("can")}\nBuyirtmalari\n{data.get("shop")}Umumiy summasi: {data.get("summa")} so'm")
    await message.bot.send_location(chat_id=6378609931, latitude=la,longitude=lo)
    baza.delete("savat",manzil_name=f"tg_id = {message.from_user.id}")
    await message.delete()

###### Ovqat tanlash funksiyalari 
@see_router.callback_query(F.data, Tekshirish.ovqat_tanlash)
async def OvqatTanlash(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
        await call.message.answer_photo(photo="AgACAgIAAxkBAAIK0GdVZSEERnHTSCRZLUtE6PRodCzLAAK05zEbn7KpSj6qe6XDtATbAQADAgADeAADNgQ", caption="707 STREET FOOD dan buyurtma berishingiz mumkin", reply_markup=AdminAndUserButton(id=call.from_user.id))
        await state.set_state(Admin.tek_button)
    elif int(xabar.split("-")[-1]) in [i[0] for i in baza.read("product",'*')]:
        for i in baza.read("product","*"):
            if int(xabar.split('-')[-1])==i[0]:
                await state.update_data(name=i[1])
                await state.update_data(narxi=i[2])
                await call.message.answer_photo(photo=f"{i[3]}",caption=f"Malumotlar:\nNomi: {i[1]}\nNarxi: {i[2]} so'm\n\nNechat sotib olmoqchisiz?", reply_markup=MaxsulotSoni())
        await state.set_state(Tekshirish.maxsulot_soni)
    await call.message.delete()

@see_router.callback_query(F.data, Tekshirish.maxsulot_soni)
async def MaxsulotSoniBot(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar=="orqaga":
        for i in baza.read("categoriya","*"):
            if data.get("cat_id")==int(i[0]):
                await call.message.answer_photo(photo=f"{i[-1]}", reply_markup=ProductUser(int(i[0])))
        await state.set_state(Tekshirish.ovqat_tanlash)
    else:
        await call.message.answer_photo(photo="AgACAgIAAxkBAAIK0GdVZSEERnHTSCRZLUtE6PRodCzLAAK05zEbn7KpSj6qe6XDtATbAQADAgADeAADNgQ", caption="Maxsulot savatga saqlandi", reply_markup=AdminAndUserButton(id=call.from_user.id))
        await state.set_state(Admin.tek_button)
        if call.from_user.id in [i[1] for i in baza.read("savat","*")]:
            if data.get("name") in [i[3] for i in baza.read("savat","*") if i[1]==call.from_user.id]:
                a = int(xabar) + int([i[-1] for i in baza.read("savat","*") if i[3]==data.get("name")][0])
                baza.update("savat",yangi_name=f"soni = '{a}'", manzil_name=f"id = {[b[0] for b in baza.read("savat","*") if b[3]==data.get("name")][0]}")
            else:
                baza.insert("savat",tg_id=call.from_user.id,user=f"{call.from_user.first_name}",name=f"{data.get("name")}",narxi=f'{data.get("narxi")}', soni=int(xabar))
        else:
            baza.insert("savat",tg_id=call.from_user.id,user=f"{call.from_user.first_name}",name=f"{data.get("name")}",narxi=f'{data.get("narxi")}', soni=int(xabar))
    await call.message.delete()

######   Bog'lanish knopkasi
@see_router.callback_query(F.data,Tekshirish.comment)
async def CommentsBot(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
        await call.message.answer_photo(photo="AgACAgIAAxkBAAIK0GdVZSEERnHTSCRZLUtE6PRodCzLAAK05zEbn7KpSj6qe6XDtATbAQADAgADeAADNgQ", caption="707 STREET FOOD dan buyurtma berishingiz mumkin", reply_markup=AdminAndUserButton(id=call.from_user.id))
        await state.set_state(Admin.tek_button)   
    elif xabar=="izoh_qoldirish":
        await call.message.answer(text="O'z fikringizni yozib qoldirishingiz mumkin")
        await state.set_state(Tekshirish.izoh_yuborish)
    await call.message.delete()

@see_router.message(F.text, Tekshirish.izoh_yuborish)
async def IzohJonatish(message:Message,state:FSMContext):
    xabar = message.text
    await state.update_data(izoh=xabar)
    await message.answer(text=f"{xabar}\n\nRostan ham bu habarni yubormoqchimisiz?",reply_markup=reklama)
    await state.set_state(Tekshirish.tasdiqlash)
    await message.delete()

@see_router.callback_query(F.data,Tekshirish.tasdiqlash)
async def TasdiqlashButtons(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar=="ha":
        baza.insert("coment",tg_id=call.from_user.id, user=f"{call.from_user.first_name}",coment=f"{data.get("izoh")}")
        await call.message.answer(text="Sizning izohingiz yuborildi!!!")
        for i in baza.read("malumotlar","*"):
                if i[0]==1:
                    await call.message.answer(text=f"📞 Telefon raqam: {i[1]}\n✉️ Telegram: {i[2]}\n🔴 Instagram: {i[3]}\n👥 Bizning kanal: {i[4]}\n\nBot haqidagi fikringizni yozib qoldiring ✍️",reply_markup=coments)
        await state.set_state(Tekshirish.comment)
    elif xabar=='yoq':
        await call.message.answer(text="Izohingiz yuborilmadi")
        for i in baza.read("malumotlar","*"):
                if i[0]==1:
                    await call.message.answer(text=f"📞 Telefon raqam: {i[1]}\n✉️ Telegram: {i[2]}\n🔴 Instagram: {i[3]}\n👥 Bizning kanal: {i[4]}\n\nBot haqidagi fikringizni yozib qoldiring ✍️",reply_markup=coments)
        await state.set_state(Tekshirish.comment)
    await call.message.delete()
