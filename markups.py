from telebot import types
from db_functions import get_all_users


def main_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = [types.KeyboardButton('Проверить задание'), types.KeyboardButton('Сдать задание на проверку'),
             types.KeyboardButton('Узнать свои оценки')]
    for item in items:
        markup.add(item)
    return markup

def marks_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = [types.KeyboardButton('1'), types.KeyboardButton('2'), types.KeyboardButton('3'), types.KeyboardButton('4'),
             types.KeyboardButton('5')]
    for item in items:
        markup.add(item)
    return markup

def students_tasks():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    users = get_all_users()
    items = []
    for user in users:
        items.append(types.KeyboardButton(' '.join([user.first_name,user.second_name])))
    for item in items:
        markup.add(item)
    return markup
