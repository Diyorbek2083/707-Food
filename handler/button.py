from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, WebhookInfo

##### Cantact so'rash
contact = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="☎️ Cantactni ulashish", request_contact=True)]
    ], resize_keyboard=True, one_time_keyboard=True
)

###### Lacatsia yuborish
lacation = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Lacatsiani yuborish", request_location=True)]
    ], resize_keyboard=True, one_time_keyboard=True
)

##### Bot malumotlarini ko'rish admin
malumotlar = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Tel raqam 📞",callback_data="tel_raqam"),InlineKeyboardButton(text="Bot 🤖",callback_data="bot_name")],
        [InlineKeyboardButton(text="Instagram 💌",callback_data="instagram"),InlineKeyboardButton(text="Kanal 👥",callback_data="kanal")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="orqaga")]

    ]
)

###### Admin qo'shish knopkasi
admin_add = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Admin ➕", callback_data="add_admin"),InlineKeyboardButton(text="Admin ➖",callback_data="remov_admin")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="orqaga")]
    ]
)

#@#### Admin Start Button
admin_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Knopka ➕➖🔄", callback_data="add_remov_replay_button"),InlineKeyboardButton(text="Admin ➕➖", callback_data="add_remov_replay_admin")],
        [InlineKeyboardButton(text="Knopkalarni tekshirish 👀", callback_data="see_button"),InlineKeyboardButton(text="Reklama ✈️", callback_data="send_reklama")],
        [InlineKeyboardButton(text="Bot malumotlari 🤖",callback_data="bot_malumot"),InlineKeyboardButton(text="Izohlar 💬",callback_data="izohlar")]
    ]
)

#### Admin knopka add remov replay
add_remov_replay = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Knopka ➕", callback_data="add_button"),InlineKeyboardButton(text="Knopka ➖",callback_data="remov_button"),InlineKeyboardButton(text="Knopka 🔄", callback_data="replay_button")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="orqaga")]
    ]
)