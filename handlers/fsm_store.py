from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from db import db_main
from aiogram.types import ReplyKeyboardRemove
from config import staff


# from db import db_main


class FSM_Store(StatesGroup):
    name_products = State()
    category = State()
    size = State()
    price = State()
    article = State()
    photo_products = State()
    submit = State()


async def products_message(message: types.Message):
    if message.from_user.id == '1687464179':
      await start_fsm()
    else:
        await message.answer('Вы не админ')
async def start_fsm(message: types.Message):
    await message.answer('Укажите название или бренд товара: ', reply_markup=buttons.cancel_button)
    await FSM_Store.name_products.set()

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_products'] = message.text

    await message.answer('Введите информацию о товаре: ')
    await FSM_Store.next()

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await message.answer('Введите размер товара: ')
    await FSM_Store.next()


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer('Введите цену товара: ')
    await FSM_Store.next()



async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await message.answer('Введите артикул (он должен быть уникальным): ')
    await FSM_Store.next()


async def load_article(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['article'] = message.text

    await message.answer('Отправьте фото: ')
    await FSM_Store.next()


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await message.answer('Верные ли данные ?')
    await message.answer_photo(
        photo=data['photo'],
        caption=f'Название/Бренд товара: {data["name_products"]}\n'
                f'Категория товара: {data["category"]}\n'
                f'Размер товара: {data["size"]}\n'
                f'Цена товара: {data["price"]}\n'
                f'Артикул: {data["article"]}\n',
        reply_markup=buttons.submit_button)

    await FSM_Store.next()


async def submit(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()

    if message.text == 'Да':
        async with state.proxy() as data:
            await message.answer('Отлично, Данные в базе!', reply_markup=kb)
            await db_main.sql_insert_products(
                name_product=data['name_products'],
                category=data['category'],
                size=data['size'],
                price=data['price'],
                articul=data['article'],
                photo=data['photo']
            )


    elif message.text == 'Нет':
        await message.answer('Хорошо, заполнение анкеты завершено!', reply_markup=kb)
        await state.finish()

    else:
        await message.answer('Выберите "Да" или "Нет"')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=kb)


def register_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state="*")


    dp.register_message_handler(load_name, state=FSM_Store.name_products)
    dp.register_message_handler(load_category, state=FSM_Store.category)
    dp.register_message_handler(load_size, state=FSM_Store.size)
    dp.register_message_handler(load_price, state=FSM_Store.price)
    dp.register_message_handler(load_article, state=FSM_Store.article)
    dp.register_message_handler(load_photo, state=FSM_Store.photo_products, content_types=['photo'])
    dp.register_message_handler(submit, state=FSM_Store.submit)
