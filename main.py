from aiogram import Bot, executor, Dispatcher, types
from app import keyboards as kb
from app import database as db
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import os
from dotenv import load_dotenv

HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>начало работы с ботом</em>
<b>/description</b> - <em>описание бота</em>"""

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()


async def on_startup(_):
    try:
        await db.db_start()
    except db.db.Error as e:
        print(f'Connection failure: {e}')
    print('Bot successfully launched')


@dp.message_handler(commands=['help'])
async def help_reply(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=HELP_COMMAND, parse_mode='HTML')


@dp.message_handler(commands=['start'])
async def start_reply(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(text='Вы авторизовались как администратор', reply_markup=kb.main_admin)
        await message.delete()
    else:
        await message.answer(text='<em>Добро пожаловать в <b>наш</b> магазин</em>', parse_mode='HTML',
                             reply_markup=kb.main)
        await message.delete()


@dp.message_handler(text='Админ-панель')
async def admin_reply(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await bot.send_message(message.from_user.id, text='Добро пожаловать в админ-панель, она предназначена для '
                                                          'управления товаром', reply_markup=kb.admin_panel)
    else:
        await message.reply(text='Я тебя не понимаю(')


@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer(text='Выберите тип товара', reply_markup=kb.catalog_list)
    else:
        await message.reply(text='Я тебя не понимаю(')


@dp.callback_query_handler(state=NewOrder.type)
async def callback_type_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer(f'Напишите название товара', reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.name)
async def callback_type_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(f'Напишите описание товара', reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.desc)
async def callback_type_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer(f'Введите стоимость товара', reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.price)
async def callback_type_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer(f'Отправьте фотографию товара', reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def photo_check(message: types.message):
    await message.answer(text='Это не фотография')


@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer(text='Товар успешно создан', reply_markup=kb.admin_panel)
    await state.finish()


@dp.message_handler(text='Каталог')
async def catalog_reply(message: types.Message):
    await bot.send_message(message.from_user.id, text='Доступные к заказу товары', reply_markup=kb.catalog_list)


@dp.message_handler(text='Корзина')
async def cart_reply(message: types.Message):
    await bot.send_message(message.from_user.id, text='Корзина пуста')


@dp.message_handler(text='Контакты')
async def contacts_reply(message: types.Message):
    await bot.send_message(message.from_user.id, text='Контакты пусты')


@dp.message_handler(commands=['description'])
async def description_reply(message: types.Message):
    await message.answer(text='Здесь вы можете заказать футболку')
    await message.delete()


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 't-shirt':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите размер', reply_markup=kb.size_list)
    elif callback_query.data == 'something':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Тут скоро что то будет')
    if callback_query.data == 'S':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Товар добавлен в корзину')
    elif callback_query.data == 'M':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Товар добавлен в корзину')
    elif callback_query.data == 'L':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Товар добавлен в корзину')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
