from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons

from aiogram.types import ReplyKeyboardRemove


class fsm_registration(StatesGroup):
    article = State()
    size = State()
    quantity = State()
    number_phone = State()
    photo = State()
    submit = State()
async def start_reg(message: types.Message):
    await message.answer('Привет!\n'
                         'Введи артикул товара: \n'
                         '!Введи размер товара,'
                         'Введи количество'
                         'Введи номер телефона\n '
                         'нажмите на "Отмена"!',
                         reply_markup=buttons.cancel_button)
    await fsm_registration.fullname.set()


async def load_article(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['article'] = message.text

    await message.answer('Введите размер товара: ')
    await fsm_registration.next()


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer('Укажите количество: ')

    await fsm_registration.next()


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text

    await message.answer('Введите номер телефона:')
    await fsm_registration.next()


async def load_number_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_phone'] = message.text
    await message.answer('Отправьте фото: ')
    await fsm_registration.next()

async def load_photo(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['photo'] = message.photo[-1].file_id

        await message.answer('Верные ли данные ?')
        await message.answer_photo(
        photo=data['photo'],
        caption=f'Артикуд: {data["article"]}\n'
        f'Размер: {data["size"]}\n'
        f'Количество: {data["quantity"]}\n'
        f'Номер телефона: {data["number_phone"]}\n',
        reply_markup=buttons.submit_buttons)

        await fsm_registration.next()

async def submit(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()

    if message.text == 'Да':
        await message.answer('Отлично, регистрация пройдена!',
                             reply_markup=kb)
        await state.finish()


    elif message.text == 'Нет':
        await message.answer('Хорошо, регистрация отменена!',
                             reply_markup=kb)
        await state.finish()
    else:
        await message.answer('Выберите "Да" или "Нет"')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!')


def register_fsm_reg(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(
        equals='Отмена',
        ignore_case=True),
                                state="*")

    dp.register_message_handler(start_reg, commands=['reg'])

    dp.register_message_handler(load_article,
                                state=fsm_registration.article)
    dp.register_message_handler(load_size,
                                state=fsm_registration.size)
    dp.register_message_handler(load_quantity,
                                state=fsm_registration.quantity)
    dp.register_message_handler(load_number_phone,
                                state=fsm_registration.number_phone)
    dp.register_message_handler(load_photo,
                                state=fsm_registration.photo,
                                content_types=['photo'])

    dp.register_message_handler(submit,
                                state=fsm_registration.submit)