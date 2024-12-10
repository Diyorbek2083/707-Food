from aiogram.fsm.state import State, StatesGroup

class Admin(StatesGroup):
    obuna = State()
    start = State()
    knopka_turi = State()
    reklama = State()
    add_button = State()
    add_admin = State()
    tek_button = State()
    bot_malumotlar = State()
    bot_malumotlar_add = State()
    comment = State()
    comentlar = State()