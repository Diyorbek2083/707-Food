from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from handler.states import Admin
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from handler.button import admin_button, add_remov_replay
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from data.sqliteClas import SQLiteBaza
from handler.funksya import CategoryaButtons, ProductButtons

baza = SQLiteBaza("imtihon.db")
button_router = Router()

button_turi = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Categorya",callback_data="categorya"),InlineKeyboardButton(text="Product",callback_data="product")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="orqaga")]
    ]
)
sorash = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"Ha ✅", callback_data="ha"), InlineKeyboardButton(text="Yo'q ❌", callback_data="yoq")]
    ]
)
categorya_butns = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Nomi", callback_data="Nomi"),InlineKeyboardButton(text="Rasmi",callback_data="Rasmi")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="orqaga")]
    ]
)
product_butns = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Nomi",callback_data="Nomi"),InlineKeyboardButton(text="Narxi",callback_data="Narxi")],
        [InlineKeyboardButton(text="Rasmi",callback_data="Rasmi"),InlineKeyboardButton(text="◀️ Orqaga",callback_data="orqaga")]
    ]
)

class Buttons(StatesGroup):
    buttons_turi = State()
    categorya_name = State()
    categorya_photo = State()
    categorya_id = State()
    categorya_remov = State()
    categorya_remov_id = State()
    categorya_reply = State()
    nomi_photo_reply = State()
    new_categorya = State()
    product_name = State()
    product_remov_name = State()
    product_count = State()
    product_photo = State()
    product_reply = State()
    name_photo_count_reply = State()
    new_product = State()
    new_product_tasdiqlash = State()
    remov_button = State()
    replay_button = State()
    sorash = State()


@button_router.callback_query(F.data,Admin.add_button)
async def ButtonBot(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
        await call.message.answer(text="Siz adminsiz!", reply_markup=admin_button)
        await state.set_state(Admin.start)
    elif xabar=="add_button":
        await state.update_data({"turi":xabar})
        await call.message.answer(text="Qayerga knopka qo'shmoqchisiz?", reply_markup=button_turi)
        await state.set_state(Buttons.buttons_turi)
    elif xabar=="remov_button":
        await state.update_data({"turi":xabar})
        await call.message.answer(text="Qayerdan knopka o'chirmoqchisiz?", reply_markup=button_turi)
        await state.set_state(Buttons.buttons_turi)
    elif xabar=="replay_button":
        await state.update_data({"turi":xabar})
        await call.message.answer(text="Qayerdagi knopkani yangilamoqchisiz?", reply_markup=button_turi)
        await state.set_state(Buttons.buttons_turi)
    await call.message.delete()

@button_router.callback_query(F.data,Buttons.buttons_turi)
async def ButtonsTuri(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar=="categorya":
        await state.update_data({"qayerga":xabar})
        if data.get("turi")=="add_button":
            await call.message.answer(text="Qo'shmoqchi bo'lgan categoriya nomini yozing!")
            await state.set_state(Buttons.categorya_name)
        elif data.get("turi")=="remov_button":
            await call.message.answer(text="Qaysi categoriyani o'chirmoqchisiz?", reply_markup=CategoryaButtons())
            await state.set_state(Buttons.categorya_remov)
        elif data.get("turi")=="replay_button":
            await call.message.answer(text="Qaysi categoriya malumotlarini o'zgartirmoqchisiz?", reply_markup=CategoryaButtons())
            await state.set_state(Buttons.categorya_reply)
    if xabar=="product":
        await state.update_data({"qayerga":xabar})
        if data.get("turi")=="add_button":
            await call.message.answer("Qaysi categoriyaga qo'shmoqchisiz?", reply_markup=CategoryaButtons())
            await state.set_state(Buttons.categorya_id)
        if data.get("turi")=="remov_button":
            await call.message.answer(text="Qaysi categoriyadagi productani o'chirmoqchisiz?", reply_markup=CategoryaButtons())
            await state.set_state(Buttons.categorya_remov_id)
        if data.get("turi")=="replay_button":
            await call.message.answer(text="Qaysi qategoriyadagi productani o'zgartirmoqchisiz?", reply_markup=CategoryaButtons())
            await state.set_state(Buttons.product_reply)
    if xabar=="orqaga":
        await call.message.answer(text="Nima qilmoqchisiz?", reply_markup=add_remov_replay)
        await state.set_state(Admin.add_button)
    await call.message.delete()


@button_router.callback_query(F.data,Buttons.sorash)
async def ButtonSorash(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar=="ha":
        if data.get("qayerga")=="categorya":
            if data.get("turi")=="add_button":
                baza.insert("categoriya",name=f"{data.get("nomi")}",rasmi=f"{data.get("photo")}")
                await call.message.answer(text="Malumotlar qo'shildi", reply_markup=admin_button)
            if data.get("turi")=="remov_button":
                baza.delete("categoriya",f"id = {data.get("c_id")}")
                baza.delete("product", f"c_id = {data.get("c_id")}")
                await call.message.answer(text="Categorya o'chirildi", reply_markup=admin_button)
            if data.get("turi")=="replay_button":
                if data.get("cat")=="Nomi":
                    baza.update("categoriya",yangi_name=f"name = '{data.get("c_new_name")}'",manzil_name=f"id = {data.get("cat_id")}")
                if data.get("cat")=="Rasmi":
                    baza.update("categoriya",yangi_name=f"rasmi = '{data.get("c_new_photo")}'",manzil_name=f"id = {data.get("cat_id")}")
                await call.message.answer(text="Categoriya mlumoti yangilandi", reply_markup=admin_button)
        if data.get("qayerga")=="product":
            if data.get("turi")=="add_button":
                baza.insert("product", name=f"{data.get("p_name")}", narxi=f"{data.get("count")}", rasm=f"{data.get("p_photo")}", c_id=int(data.get("c_id")))
                await call.message.answer("malumot qo'shildi", reply_markup=admin_button)  
            elif data.get("turi")=="remov_button":
                baza.delete("product", f"id = {data.get("p_id")}")
                await call.message.answer(text="Producta o'chirildi", reply_markup=admin_button)
            elif data.get("turi")=="replay_button":
                if data.get("p_turi")=="Nomi":
                    baza.update("product",yangi_name=f"name = '{data.get("qayerga1")}'",manzil_name=f"id = {data.get("c_id")}")
                    await call.message.answer(text="Producta nomi yangiladni", reply_markup=admin_button)
                if data.get("p_turi")=="Narxi":
                    baza.update("product",yangi_name=f"narxi = '{data.get("qayerga1")}'",manzil_name=f"id = {data.get("c_id")}")
                    await call.message.answer(text="Producta narxi yangiladni", reply_markup=admin_button)
                if data.get("p_turi")=="Rasmi":
                    baza.update("product",yangi_name=f"rasm = '{data.get("qayerga1")}'",manzil_name=f"id = {data.get("c_id")}")
                    await call.message.answer(text="Producta rasmi yangiladni", reply_markup=admin_button)
        await state.set_state(Admin.start)
        await call.message.delete()
    if xabar=="yoq":
        await call.message.answer(text="Nima qilmoqchisiz?", reply_markup=add_remov_replay)
        await state.set_state(Admin.add_button)
    await call.message.delete()


#####  Producta malumotlarini replay qilish
@button_router.callback_query(F.data,Buttons.product_reply)
async def ProductaReplyCategorya(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
        await call.message.answer(text="Qayerdagi knopkani yangilamoqchisiz?", reply_markup=button_turi)
        await state.set_state(Buttons.buttons_turi)
    else:
        a = 0
        for i in baza.read("product","*"):
            if int(xabar.split("-")[-1])==int(i[-1]):
                a+=1
        if a>0:
            await state.update_data(c_id=xabar.split("-")[-1])
            await state.update_data(c_name=xabar.split("-")[0])
            await call.message.answer(text=f"Qaysi productani malumotlarini o'zgartirmoqchisiz?", reply_markup=ProductButtons(xabar.split("-")[-1]))
            await state.set_state(Buttons.name_photo_count_reply)
        else:
            await call.message.answer(text="Bu categoryada hali maxsulot yo'q iltimos oldin maxsulot qo'shing", reply_markup=CategoryaButtons())
            await state.set_state(Buttons.product_reply)
    await call.message.delete()

@button_router.callback_query(F.data,Buttons.name_photo_count_reply)
async def ProductaMalumotlari(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar=="orqaga":
        await call.message.answer(text="Qaysi qategoriyadagi productani o'zgartirmoqchisiz?", reply_markup=CategoryaButtons())
        await state.set_state(Buttons.product_reply)
    else:
        for i in baza.read("product","*"):
            if i[0]==int(xabar.split("-")[-1]):
                await state.update_data(p_nomi=i[1])
                await state.update_data(p_count=i[2])
                await state.update_data(p_rasm=i[3])
                await call.message.answer_photo(photo=f"{i[3]}",caption=f"Categorya: {data.get("c_name")}\nNomi: {i[1]}\nNarxi: {i[2]}so'm")
                await call.message.answer(text="Productaning qaysi malumotini o'zgartirmoqchisiz?", reply_markup=product_butns)
                await state.set_state(Buttons.new_product)
    await call.message.delete()


@button_router.callback_query(F.data,Buttons.new_product)
async def NewProduct(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    if xabar=="orqaga":
        await call.message.answer(text=f"Qaysi productani malumotlarini o'zgartirmoqchisiz?", reply_markup=ProductButtons(data.get("c_id")))
        await state.set_state(Buttons.name_photo_count_reply)
    elif xabar=="Nomi":
        await state.update_data(p_turi = xabar)
        await call.message.answer(text="Productaning yanig nomini kirting")
        await state.set_state(Buttons.new_product_tasdiqlash)
    elif xabar=="Narxi":
        await state.update_data(p_turi = xabar)
        await call.message.answer(text="Productaning yangi narxini kirting")
        await state.set_state(Buttons.new_product_tasdiqlash)
    elif xabar=="Rasmi":
        await state.update_data(p_turi = xabar)
        await call.message.answer(text="Productaning yangi rasmini yuboring")
        await state.set_state(Buttons.new_product_tasdiqlash)
    await call.message.delete()

@button_router.message(Buttons.new_product_tasdiqlash)
async def NewProductTasdiqlash(messsage:Message,state:FSMContext):
    xabar = messsage.text
    data = await state.get_data()
    if data.get("p_turi")=="Nomi":
        await state.update_data(qayerga1=xabar)
        await messsage.answer(text=f"Eski nomi: {data.get("p_nomi")}\nYangi nomi: {xabar}\nYangi nomini tasdiqlaysizm?", reply_markup=sorash)
        await state.set_state(Buttons.sorash)
    elif data.get("p_turi")=="Narxi":
        if xabar.isdigit():
            await state.update_data(qayerga1=xabar)
            await messsage.answer(text=f"Eski narxi: {data.get("p_count")}so'm\nYangi narxi: {xabar}so'm\nYangi narxni tasdiqlaysizmi?",reply_markup=sorash)
            await state.set_state(Buttons.sorash)
        else:
            await messsage.answer(text=f"Iltimos raqam kirting\nMisol: 10000")
            await state.set_state(Buttons.new_product_tasdiqlash)
    elif data.get("p_turi")=="Rasmi":
        if messsage.photo[-1].file_id:
            await state.update_data(qayerga1=messsage.photo[-1].file_id)
            await messsage.answer_photo(photo=messsage.photo[-1].file_id, caption=f"Productaning yangi rasmi\nYangi rasimni tasdiqlaysizmi?",reply_markup=sorash)
            await state.set_state(Buttons.sorash)
        else:
            await messsage.answer(text="Iltimos rasim yuboring")
            await state.set_state(Buttons.new_product_tasdiqlash)


######  Categorya malumotlarini o'zgartirish
@button_router.callback_query(F.data, Buttons.categorya_reply)
async def CategoryaReplay(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
        await call.message.answer(text="Qayerdagi knopkani yangilamoqchisiz?", reply_markup=button_turi)
        await state.set_state(Buttons.buttons_turi)
    else:
        for i in baza.read("categoriya"):
            if int(xabar.split("-")[-1])==i[0]:
                await state.update_data(cat_name=xabar.split("-")[0])
                await state.update_data(cat_id=int(xabar.split("-")[-1]))
                await call.message.answer_photo(photo=i[2], caption=f"Nomi: {i[1]}")
                await call.message.answer(text="Categoriyaning qaysi malumotini o'zgartirmoqchisiz?", reply_markup=categorya_butns)
                await state.set_state(Buttons.nomi_photo_reply)
    await call.message.delete()

@button_router.callback_query(F.data,Buttons.nomi_photo_reply)
async def CategoryaNameReply(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    print(xabar)
    if xabar=="orqaga":
        await call.message.answer(text="Qaysi categoriya malumotlarini o'zgartirmoqchisiz?", reply_markup=CategoryaButtons())
        await state.set_state(Buttons.categorya_reply)
    elif xabar=="Nomi":
        await state.update_data(cat=xabar)
        await call.message.answer(text="Categoryaning yangi nomini kirting")
        await state.set_state(Buttons.new_categorya)
    elif xabar=="Rasmi":
        await state.update_data(cat=xabar)
        await call.message.answer(text="Categoriyaning rangi rasmini yuboring")
        await state.set_state(Buttons.new_categorya)
    await call.message.delete()

@button_router.message(Buttons.new_categorya)
async def NewCategorya(message:Message,state:FSMContext):
    xabar = message.text
    data = await state.get_data()
    if data.get("cat")=="Nomi":
        await state.update_data(c_new_name=xabar)
        await message.answer(text=f"Eski nomi: {data.get("cat_name")}\nYangi nomi: {xabar}\nYangi nomini tasdiqlaysizmi?", reply_markup=sorash)
    elif data.get("cat")=="Rasmi":
        await state.update_data(c_new_photo=message.photo[-1].file_id)
        await message.answer_photo(photo=message.photo[-1].file_id, caption=f"Categoriyaning yangi rasmi")
        await message.answer(text="Bu rasimni tasdiqlaysizmi?",reply_markup=sorash)
    await state.set_state(Buttons.sorash)


##### Product remov button
@button_router.callback_query(F.data,Buttons.categorya_remov_id)
async def CategoryaRemovId(call:CallbackQuery,state:FSMContext):
    xaba = call.data
    if xaba=="orqaga":
        await call.message.answer(text="Qayerdan knopka o'chirmoqchisiz?", reply_markup=button_turi)
        await state.set_state(Buttons.buttons_turi)
    else:
        a=0
        for i in baza.read("product","*"):
            if int(xaba.split("-")[-1])==int(i[-1]):
                a+=1
        if a>0:
            await state.update_data({"c_id":xaba.split("-")[-1]})
            await state.update_data({"c_name":xaba.split("-")[0]})
            await call.message.answer(text="Qaysi productani o'chirmoqchisiz?", reply_markup=ProductButtons(xaba.split("-")[-1]))
            await state.set_state(Buttons.product_remov_name)
        else:
            await call.message.answer(text="Bu categoriyada hali maxsulot yo'q iltimos oldin maxsulot qo'shing", reply_markup=CategoryaButtons())
            await state.set_state(Buttons.categorya_remov_id)
    await call.message.delete()

@button_router.callback_query(F.data,Buttons.product_remov_name)
async def ProductRemovName(call:CallbackQuery,state:FSMContext):
    xaba = call.data
    data = await state.get_data()
    print(xaba)
    if xaba=="orqaga":
        await call.message.answer(text="Qayerdan knopka o'chirmoqchisiz?", reply_markup=CategoryaButtons())
        await state.set_state(Buttons.categorya_remov_id)
    else:
        for i in baza.read("product","*"):
            if int(xaba.split("-")[-1])==i[0]:
                await state.update_data({"p_id":int(xaba.split("-")[-1])})
                await call.message.answer_photo(photo=f"{i[3]}", caption=f"Categorya: {data.get("c_name")}\nNomi: {i[1]}\nNarxi: {i[2]}")
                await call.message.answer(text="Rostan ham bu productani o'chirmoqchimisiz?", reply_markup=sorash)
                await state.set_state(Buttons.sorash)
    await call.message.delete()


##### Categorya o'chirish
@button_router.callback_query(F.data,Buttons.categorya_remov)
async def RemovCategorya(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
            await call.message.answer(text="Qayerdan knopka o'chirmoqchisiz?", reply_markup=button_turi)
            await state.set_state(Buttons.buttons_turi)
    else:
        for i in baza.read("categoriya","*"):
            if i[0]==int(xabar.split("-")[-1]):
                await state.update_data({"c_id":xabar.split("-")[-1]})
                await call.message.answer_photo(photo=f"{i[2]}", caption=f"{i[1]}")
                await call.message.answer(text="Rostan ham bu categoryani o'chirmoqchimisiz?", reply_markup=sorash)
                await state.set_state(Buttons.sorash)
    await call.message.delete()


##### Product qoshish
@button_router.callback_query(F.data, Buttons.categorya_id)
async def CtegoryaIdAdd(call:CallbackQuery,state:FSMContext):
    xabar = call.data
    if xabar=="orqaga":
        await call.message.answer(text="Qayerga knopka qo'shmoqchisiz?", reply_markup=button_turi)
        await state.set_state(Buttons.buttons_turi)
    else:
        await state.update_data({"c_id":xabar.split('-')[-1]})
        await state.update_data({"c_name":xabar.split("-")[0]})
        await call.message.answer(text=f"Qo'shmoqchi bo'lgan producta nomini yozing")
        await state.set_state(Buttons.product_name)
    await call.message.delete()

@button_router.message(F.text,Buttons.product_name)
async def ProductNameAdd(message:Message,state:FSMContext):
    xabar = message.text
    await state.update_data({"p_name":xabar})
    await message.answer(text="Producta narxini kirting")
    await state.set_state(Buttons.product_count)

@button_router.message(F.text,Buttons.product_count)
async def ProductCountAdd(message:Message,state:FSMContext):
    xabar = message.text
    if xabar.isdigit():
        await state.update_data({"count":xabar})
        await message.answer(text="Producta rasmini yuboring")
        await state.set_state(Buttons.product_photo)
    else:
        await message.answer(text=f"Iltimos raqam kirting\nMasaln: 10000")
        await state.set_state(Buttons.product_count)

@button_router.message(F.photo,Buttons.product_photo)
async def ProductPhotoAdd(message:Message,state:FSMContext):
    if message.photo[-1].file_id:
        xabar = message.photo[-1].file_id
        data = await state.get_data()
        await state.update_data({"p_photo":xabar})
        await message.answer_photo(photo=xabar, caption=f"Categorya: {data.get("c_name")}\nNomi: {data.get("p_name")}\nNarxi: {data.get("count")}so'm")
        await message.answer(text="Malumotlar to'g'rimi?", reply_markup=sorash)
        await state.set_state(Buttons.sorash)
        await message.delete()
    else:
        await message.answer(text="Iltimos rasim yuboring")
        await state.set_state(Buttons.product_photo)

#### Categoriya add
@button_router.message(F.text,Buttons.categorya_name)
async def CategoryaAdd(message:Message,state:FSMContext):
    xabar = message.text
    await state.update_data({"nomi":xabar})
    await message.answer(text="Qo'shmoqchi bo'lgan categoryangizni rasmini yuboring.")
    await state.set_state(Buttons.categorya_photo)
    await message.delete()
    
@button_router.message(F.photo,Buttons.categorya_photo)
async def CategoryaPhotoAdd(message:Message,state:FSMContext):
    xabar = message.photo[-1].file_id
    data = await state.get_data()
    await state.update_data({"photo":xabar})
    await message.answer_photo(photo=xabar,caption=f"{data.get("nomi")}")
    await message.answer(text="Rostan ham bu categoryani qo'shmoqchimisiz?", reply_markup=sorash)
    await state.set_state(Buttons.sorash)
    await message.delete()