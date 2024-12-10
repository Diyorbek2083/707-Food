from handler.users import router
from aiogram import Bot,Dispatcher
import asyncio
from data.sqliteClas import SQLiteBaza
from handler.reklama import reklama_router
from handler.states import Admin
from handler.addbuttons import button_router
from handler.addadmin import admin_router
from handler.seebutton import see_router
from handler.bot_malumot import malumot_router
from handler.comentlar import coment_router  


bot = Bot(token='8091829703:AAH-zsjNEPf6MCflrIZYb8gFggYRW-c_DFY')
dp = Dispatcher()
baza = SQLiteBaza("imtihon.db")

dp.include_router(router)
dp.include_router(reklama_router)
dp.include_router(button_router)
dp.include_router(admin_router)
dp.include_router(see_router)
dp.include_router(malumot_router)
dp.include_router(coment_router)

async def main():
   await dp.start_polling(bot)

# try:
asyncio.run(main())
# except:
#    print("tugadi")