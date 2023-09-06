from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку').add('Назад')

catalog_list = InlineKeyboardMarkup(row_width=1)
size_list = InlineKeyboardMarkup(row_width=2)
size_list.add(InlineKeyboardButton('S', callback_data='S'), InlineKeyboardButton('M', callback_data='M'),
              InlineKeyboardButton('L', callback_data='L'))
catalog_list.add(InlineKeyboardButton('Футболка', callback_data='tshirt'),
                 InlineKeyboardButton('котики', callback_data='cats'))

items_list = ReplyKeyboardMarkup(resize_keyboard=True)
items_list.add('Букля').add('Викси')

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')
