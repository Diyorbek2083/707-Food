from data.sqliteClas import SQLiteBaza
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.db_bot import AdminsId, UsersId
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

baza = SQLiteBaza("imtihon.db")

###### Comentga javob yozish
def JavobYozish(id,tg_id):
    javob = InlineKeyboardBuilder()
    for i in baza.read("coment","*"):
        if i[0]==id:
            javob.button(text="Javob yozish ✍️",callback_data=f"javob-{id}-{tg_id}")
            javob.button(text="O'chirib tashlash ❌", callback_data=f"ochir-{id}-{tg_id}")
    javob.adjust(2)
    return javob.as_markup()


###### Savat ichidagi ovqat o'chirish knopkalari
def Karzinkalar(id):
    karzinka = InlineKeyboardBuilder()
    a = 1
    for i in baza.read("savat","*"):
        if i[1]==id:
            karzinka.button(text=f"🗑{a}",callback_data=f"{i[0]}")
            a += 1
    karzinka.add(InlineKeyboardButton(text="✔️ Zakaz berish", callback_data="✔️ Zakaz berish"))
    karzinka.add(InlineKeyboardButton(text="🛒 Savatni tozalash",callback_data='🛒 Savatni tozalash'))
    karzinka.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data="orqaga"))
    karzinka.adjust(3)
    return karzinka.as_markup()

##### Maxsulotlar soni funksiyasi
def MaxsulotSoni():
    buton = InlineKeyboardBuilder()
    for i in range(1, 11):
        buton.button(text=f"{i}",callback_data=f"{i}")
    buton.button(text="◀️ Orqaga", callback_data="orqaga")
    buton.adjust(5)
    return buton.as_markup()

##### Productani chiqaradigan funksiya
def ProductUser(id):
    buton = InlineKeyboardBuilder()
    for i in baza.read("product","*"):
        if id==int(i[-1]):
            buton.button(text=f"{i[1]}-{i[2]}so'm", callback_data=f"{i[1]}-{i[2]}-{i[0]}")
    buton.button(text="◀️ Orqaga", callback_data="orqaga")
    buton.adjust(2)
    return buton.as_markup()

##### Admin tekshirish knopkasi
def AdminAndUserButton(id):
    button = InlineKeyboardBuilder()
    for i in baza.read("categoriya","*"):
        button.button(text=f"{i[1]}",callback_data=f"{i[1]}-{i[0]}")
    if id in AdminsId():
        button.button(text="Bog'lanish 📞",callback_data="boglanish")
        button.button(text="Zakaz berish 🛒", callback_data="zakaz_berish")
        button.button(text="◀️ Orqaga", callback_data="orqaga")
    else:
        button.button(text="Bog'lanish 📞",callback_data="boglanish")
        button.button(text="Zakaz berish 🛒", callback_data="zakaz_berish")
    button.adjust(2)
    return button.as_markup()

#######  Admin buttons
def AdminReadButtons():
    button = InlineKeyboardBuilder()
    for i in baza.read("admins","*"):
        button.button(text=f"{i[2]}({i[1]})", callback_data=f"{i[0]}")
    button.button(text="◀️ Orqaga", callback_data="orqaga")
    button.adjust(2)
    return button.as_markup()

#### Product Buttos
def ProductButtons(id):
    botton = InlineKeyboardBuilder()
    for i in baza.read("product","*"):
        if i[-1]==id:
            botton.button(text=f"{i[1]} - {i[2]} so'm",callback_data=f"{i[1]}-{i[2]}-{i[0]}")
    botton.button(text="◀️ Orqaga", callback_data="orqaga")
    botton.adjust(2)
    return botton.as_markup()

#### Categroya buttons
def CategoryaButtons():
    button = InlineKeyboardBuilder()
    for i in baza.read("categoriya","*"):
        button.button(text=f"{i[1]}", callback_data=f"{i[1]}-{i[0]}")
    button.button(text="◀️ Orqaga", callback_data="orqaga")
    button.adjust(3)
    return button.as_markup()