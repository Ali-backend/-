import os
from buttons import start
from config import dp, bot
from aiogram import types, Dispatcher
from handlers.fsm_store import start_fsm



async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Hello!',
                           reply_markup=start)


async def info_handler(message: types.Message):
    await message.answer(text='Я создан для теста')

async def product_handler(message: types.Message):
    await start_fsm()


async def process_send_to_staff(callback_query: types.CallbackQuery):
    staff_ids = [1687464179, 3593583556]
    product_info = "Новое сообщение для сотрудников!"

def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(info_handler, commands=['info'])
    dp.register_message_handler(product_handler, commands=['product'])
    dp.register.callback_query(ats)