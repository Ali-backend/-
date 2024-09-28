import logging
from aiogram.utils import executor
from handlers import (commands,  FSM_reg, fsm_store,send_products)
from config import dp, bot, staff
from db import db_main


async def on_startup(_):
    for admin in staff:
        await bot.send_message(chat_id=admin, text="Бот включен!")
        await db_main.sql_create()


async def on_shutdown(_):
    for admin in staff:
        await bot.send_message(chat_id=admin, text="Бот отключен!")


commands.register_commands(dp)
fsm_store.register_store(dp)
FSM_reg.register_fsm_reg(dp)
send_products.register_send_products_handler(dp)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, )
