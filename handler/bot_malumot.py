from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from handler.states import Admin
from handler.button import admin_button, malumotlar
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from data.sqliteClas import SQLiteBaza
import re

malumot_router = Router()
baza = SQLiteBaza("imtihon.db")


class Bot(StatesGroup):
    bot_name = State()
    insta_name = State()
    kanal_name = State()
    sorash = State()
    malumot_add = State()



sorash = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"Ha ✅", callback_data="ha"), InlineKeyboardButton(text="Yo'q ❌", callback_data="yoq")]
    ]
)



#### Bot malumotlarini yangilash 
@malumot_router.callback_query(F.data,Admin.bot_malumotlar)
async def BotMalumotlarReplay(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    await state.update_data(bot=2)
    data = await state.get_data()
    await state.update_data(nomer=data.get("nomer"))
    await state.update_data(tg1=data.get("tg"))
    await state.update_data(insta1=data.get("insta"))
    await state.update_data(kanal1=data.get("kanal"))
    if xabar=="orqaga":
        await call.message.answer(text="Siz adminsiz",reply_markup=admin_button)
        await state.set_state(Admin.start)
    elif xabar=="tel_raqam":
        await state.update_data(qaysi=xabar)
        await call.message.answer(text="Iltimos yangi raqamni yuboring\nMasalan: +998907002083")
        await state.set_state(Bot.malumot_add)
    elif xabar=="bot_name":
        await state.update_data(qaysi=xabar)
        await call.message.answer(text="Yangi telegram name yuboring\nMasalan: @but_name")
        await state.set_state(Bot.malumot_add)
    elif xabar=="instagram":
        await state.update_data(qaysi=xabar)
        await call.message.answer(text="Yangi instagram name kirting\nMasalan: @bun_insta")
        await state.set_state(Bot.malumot_add)
    elif xabar=="kanal":
        await state.update_data(qaysi=xabar)
        await call.message.answer(text="Yangi kanalning user nameni kirting\nMasalan: @kanal_name")
        await state.set_state(Bot.malumot_add)
    await call.message.delete()

@malumot_router.message(F.text,Bot.malumot_add)
async def MalumotQoshish(message:Message,state:FSMContext):
    xabar = message.text
    data = await state.get_data()
    if data.get("qaysi")=="tel_raqam":
        andoza1 = "(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"
        if re.match(andoza1, xabar):
            await state.update_data(nima=xabar)
            await message.answer(text=f"Eski raqam: {data.get("nomer")}\nYangi raqam: {xabar}\nRostan ham bu malumotga o'zgartirmoqchmisiz?", reply_markup=sorash)
            await state.set_state(Bot.sorash)
        else:
            await message.answer(text="Siz yuborgan raqam to'g'ri kelmadi iltimos boshqatdan kirting\nMasalan: +998907002083")
            await state.set_state(Bot.malumot_add)
    elif data.get("qaysi")=="bot_name":
        if xabar.startswith('@'):
            await state.update_data(nima=xabar)
            await message.answer(text=f"Eski bot name: {data.get("tg1")}\nYangi bot name: {xabar}\nRostan ham bu malumotga o'zgartirmoqchmisiz?",reply_markup=sorash)
            await state.set_state(Bot.sorash)
        else:
            await message.answer(text="Siz yuborgan user name to'g'ri kelmadi iltimos boshqatdan yozing\nMasalan: @bot_name")
            await state.set_state(Bot.malumot_add)
    elif data.get("qaysi")=="instagram":
        if xabar.startswith("@"):
            await state.update_data(nima=xabar)
            await message.answer(text=f"Eski instagram name: {data.get("insta1")}\nYangi instagram name: {xabar}\nRostan ham bu malumotga o'zgartirmoqchimisiz?", reply_markup=sorash)
            await state.set_state(Bot.sorash)
        else:
            await message.answer(text="Siz yuborgan instagram name to'g'ri kelmadi iltimos boshqatdan yozing\nMasalan: @insta_bot")
            await state.set_state(Bot.malumot_add) 
    elif data.get("qaysi")=="kanal":
        if xabar.startswith('@'):
            await state.update_data(nima=xabar)
            await message.answer(text=f"Eski kanal name: {data.get("kanal1")}\nYangi kanal name: {xabar}\nRostan ham bu malumotga o'zgartirmoqchimisiz?", reply_markup=sorash)
            await state.set_state(Bot.sorash)
        else:
            await message.answer(text="Siz yuborgan instagram name to'g'ri kelmadi iltimos boshqatdan yozing\nMasalan: @kanal_name")
            await state.set_state(Bot.malumot_add)  
    await message.delete()


##### Botga malumot qo'shish va malumot yangilash
@malumot_router.callback_query(F.data,Bot.sorash)
async def RuxsatSorash(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar=="ha":
        if int(data.get("bot"))==1:
            baza.insert("malumotlar", tel=f"{data.get('raqam')}", tg=f"{data.get("bot_name")}",insta=f"{data.get("insta")}",kanal=f"{data.get("kanal")}")
        elif int(data.get("bot"))==2:
            print(1)
            if data.get("qaysi")=="tel_raqam":
                baza.update("malumotlar",yangi_name=f"tel = '{data.get("nima")}'", manzil_name=f"id = {1}")
            elif data.get("qaysi")=="bot_name":
                print(data.get("nima"))
                baza.update("malumotlar",yangi_name=f"tg = '{data.get("nima")}'", manzil_name=f"id = {1}")
            elif data.get("qaysi")=="instagram":
                print(1)
                print(type(data.get("nima")))
                baza.update("malumotlar",yangi_name=f"insta = '{data.get("nima")}'", manzil_name=f"id = {1}")
            elif data.get("qaysi")=="kanal":
                baza.update("malumotlar",yangi_name=f"kanal = '{data.get("nima")}'", manzil_name=f"id = {1}")
            await call.message.answer(text="Malumot yangilandi", reply_markup=admin_button)
            await state.set_state(Admin.start)
    if xabar=="yoq":
        await call.message.answer(text="Siz adminsiz", reply_markup=admin_button)
        await state.set_state(Admin.start)
    await call.message.delete()
    

###### Bootga malumot qo'shish
@malumot_router.message(F.text,Admin.bot_malumotlar_add)
async def BotgaMalumotYuklash(messag:Message,state:FSMContext):
    raqam = messag.text
    await state.update_data(bot=1)
    andoza1 = "(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"
    if re.match(andoza1, raqam):
        await state.update_data(raqam=messag.text)
        await messag.answer(text="Bot manzilini kirting\nBunga o'xshash: @bot_name")
        await state.set_state(Bot.bot_name)
    else:
        await messag.answer(text="Iltimos uzb raqam kirting\nBung o'xshash: +998907002083")
        await state.set_state(Admin.bot_malumotlar_add)

@malumot_router.message(F.text,Bot.bot_name)
async def BotNamenAdd(message:Message,state:FSMContext):
    xabar = message.text
    if xabar.startswith("@") and xabar.isalpha() or "_" in xabar:
        await state.update_data(bot_name=message.text)
        await message.answer(text="Bot instagram nameni yuboring\nBunga o'xshash bo'lsin: @insta_name")
        await state.set_state(Bot.insta_name)
    else:
        await message.answer(text="Yuborgan bot user nomi xato\nIltimos bung o'xshash qilbi yuboring: @bot_name")
        await state.set_state(Bot.bot_name)

@malumot_router.message(F.text,Bot.insta_name)
async def InstaNameAdd(message:Message,state:FSMContext):
    xabar = message.text
    if xabar.startswith("@"):
        await state.update_data(insta=xabar)
        await message.answer(text="Bot ulangan kanal nameni yuboring\nBunga o'xshash bo'lsin: @kanal_name")
        await state.set_state(Bot.kanal_name)
    else:
        await message.answer(text="Siz yuborgan instagram name xato iltimos boshqatdan yuboring\nBunga o'xshash bo'lsin: @insta_name")
        await state.set_state(Bot.insta_name)
    
@malumot_router.message(F.text,Bot.kanal_name)
async def KanalNameAdd(message:Message,state:FSMContext):
    xabar = message.text
    if xabar.startswith("@"):
        data = await state.get_data()
        await state.update_data(kanal=xabar)
        await message.answer(text=f"Tel raqam: {data.get('raqam')}\nBot name: {data.get("bot_name")}\nInstagram: {data.get("insta")}\nBizning kanal: {xabar}\n\nRostan ham bu malumotlarni qo'shmoqchmisiz?",reply_markup=sorash)
        await state.set_state(Bot.sorash)
    else:
        await message.answer(text="Siz yuborgan kanal nomi xato iltimos boshqatdan yuboring\nBunga o'xshash bo'lsin: @kanal_name")
        await state.set_state(Bot.kanal_name)
        