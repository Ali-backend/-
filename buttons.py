from aiogram.types import KeyboardButton, ReplyKeyboardMarkup



start = ReplyKeyboardMarkup(resize_keyboard=True,
                            row_width=2)

start_button = KeyboardButton('/start')
info_button = KeyboardButton('/info')
product_button = KeyboardButton('/products')


start.add(start_button, info_button, product_button)


cancel_button = ReplyKeyboardMarkup(
    resize_keyboard=True
).add(KeyboardButton('Отмена'))


submit_buttons = ReplyKeyboardMarkup(
    resize_keyboard=True, row_width=2).add(
    KeyboardButton('Да'),
    KeyboardButton('Нет'))