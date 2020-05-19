from telebot import types


def main_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = [types.KeyboardButton('Проверить задание'), types.KeyboardButton('Сдать задание на проверку'),
             types.KeyboardButton('Узнать свои оценки')]
    for item in items:
        markup.add(item)
    return markup