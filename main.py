from aiogram import Bot, executor, Dispatcher, types
from config import TOKEN_API
import pandas as pd
import random
import string

HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>начало работы с ботом</em>
<b>/give</b> - <em>кидает собаку</em>"""

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
count = 0


async def on_startup(_):
    print('Работаем девачки')


@dp.message_handler(commands=['help'])
async def help_reply(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=HELP_COMMAND, parse_mode='HTML')


@dp.message_handler(commands=['start'])
async def start_reply(message: types.Message):
    await message.answer(text='<em>Добро пожаловать в <b>наш</b> магазин</em>', parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['description'])
async def description_reply(message: types.Message):
    await message.answer(text='Здесь вы можете заказать футболку')
    await message.delete()


@dp.message_handler(commands=['count'])
async def count_reply(message: types.Message):
    global count
    await message.answer(text=f'Количество предыдущих вызовов: {count}')
    await message.delete()
    count += 1


@dp.message_handler(commands=['give'])
async def give_reply(message: types.Message):
    await message.answer(text='Смотри какой пэс крутой на тебя похож')
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEKNLlk84nhkBCmGe1YssiusPG5juyBVAACWQsAAoBjYUt4gLNAOvgwTzAE')


@dp.message_handler(commands=['image'])
async def image_reply(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://avatars.mds.yandex.net/i?id=2a0000018a574be0b8164509ae43c24fdf64-1075067-fast'
                               '-images&n=13')


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
