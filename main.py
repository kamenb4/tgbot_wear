from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
import pandas as pd
import os
from dotenv import load_dotenv

HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>начало работы с ботом</em>
<b>/description</b> - <em>описание бота</em>"""

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку').add('Назад')


async def on_startup(_):
    print('Работаем девачки')


@dp.message_handler(commands=['help'])
async def help_reply(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=HELP_COMMAND, parse_mode='HTML')


@dp.message_handler(commands=['start'])
async def start_reply(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(text='Вы авторизовались как администратор', reply_markup=main_admin)
        await message.delete()
    else:
        await message.answer(text='<em>Добро пожаловать в <b>наш</b> магазин</em>', parse_mode='HTML',
                             reply_markup=main)
        await message.delete()


@dp.message_handler(text='Админ-панель')
async def start_reply(message: types.Message):
    await bot.send_message(message.from_user.id, text='Добро пожаловать в админ-панель, она предназначена для '
                                                      'управления товаром', reply_markup=admin_panel)


@dp.message_handler(text='Каталог')
async def start_reply(message: types.Message):
    await bot.send_message(message.from_user.id, text='Каталог пуст')


@dp.message_handler(text='Корзина')
async def start_reply(message: types.Message):
    await bot.send_message(message.from_user.id, text='Корзина пуста')


@dp.message_handler(text='Контакты')
async def start_reply(message: types.Message):
    await bot.send_message(message.from_user.id, text='Контакты пусты')


@dp.message_handler(commands=['description'])
async def description_reply(message: types.Message):
    await message.answer(text='Здесь вы можете заказать футболку')
    await message.delete()


@dp.message_handler(commands=['location'])
async def location_reply(message: types.Message):
    await bot.send_location(chat_id=message.from_user.id,
                            longitude=66,
                            latitude=74)


@dp.message_handler()
async def answer(message: types.Message):
    if '0' in message.text:
        await message.answer(text='YES')
    else:
        await message.answer(text='NO')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
