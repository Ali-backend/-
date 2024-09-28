import sqlite3
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text



def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * FROM products p 
    """).fetchall()
    conn.close()
    return products


async def start_sending_products(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    show_all_products = InlineKeyboardButton(text='Показать все товары',
                                             callback_data='show_all')
    keyboard.add(show_all_products)

    await message.answer(text='Нажмите на кнопку, чтобы увидеть все товары',
                         reply_markup=keyboard)


async def send_all_products(callback_query: types.CallbackQuery):
    products = fetch_all_products()

    if products:
        for product in products:
            caption = (f'Название товара - {product["name_products"]}\n'
                       f'Категория - {product["category"]}\n'
                       f'Размер - {product["size"]}\n'
                       f'Цена - {product["price"]}\n'
                       f'Артикул - {product["article"]}\n')


            await callback_query.message.answer_photo(photo=product['photo'],
                                                      caption=caption)\

    else:
        await callback_query.message.answer(text='В базе товаров нет!')

async def send_products_staff(callback_query: types.CallbackQuery):
    products = fetch_all_products()

    button1 = types.InlineKeyboardButton("Получить информацию о продукте", callback_data='get_product_info')
    button2 = types.InlineKeyboardButton("Отправить сообщение сотрудникам", callback_data='send_to_staff')
    markup.add(button1, button2)


def register_send_products_handler(dp: Dispatcher):
    dp.register_message_handler(start_sending_products, commands=['products'])
    dp.register_callback_query_handler(send_all_products,
                                       Text(equals='show_all'))
