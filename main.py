import telebot
import config
import conversation
import state
from db_functions import is_exsist
from db_functions import set_user_state
from db_functions import get_user_state
from db_functions import add_user
from db_functions import delete_user_state
from db_functions import get_user_fio
from markups import main_menu

bot = telebot.TeleBot(config.token)

@bot.message_handler(func= lambda message: message.text == 'Проверить задание')
def check_someone(message):
    bot.send_message(message.chat.id, 'Проверить задание')

@bot.message_handler(func= lambda message: message.text == 'Сдать задание на проверку')
def take_job(message):
    bot.send_message(message.chat.id, 'Загрузите свое задание')
    set_user_state(message.from_user.id, state.take_the_job)

@bot.message_handler(func= lambda message: message.text == 'Узнать свои оценки')
def know_mark(message):
    bot.send_message(message.chat.id, 'Узнать свои оценки')

@bot.message_handler(content_types=['document'])
def upload_job(message):
    bot.send_message(message.chat.id, 'upload message')
    file = message.document.file_id
    delete_user_state(message.from_user.id)
    bot.send_message(message.chat.id, 'Вы загрузили свое задание, позже вы сможете увидеть свои оценки')
    bot.send_message(message.chat.id, conversation.hello_known.format(get_user_fio(message.from_user.id)[0]),
                     reply_markup=main_menu())


@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == state.enter_fio)
def get_fio(message):
    fio = message.text.split()
    if len(fio) == 2:
        if fio[0].isalnum() and fio[1].isalnum():
            add_user(message.from_user.id, fio[0], fio[1])
            delete_user_state(message.from_user.id)
            bot.send_message(message.chat.id, conversation.hello_known.format(get_user_fio(message.from_user.id)[0]),
                             reply_markup=main_menu())


@bot.message_handler(commands=['help','start'])
def main_start(message):
    print(message.from_user)
    if not is_exsist(user_id=message.from_user.id):
        set_user_state(message.from_user.id, state.enter_fio)
        bot.send_message(message.chat.id, conversation.hello_unknow )
    if is_exsist(user_id=message.from_user.id):
        print('User exsist')
        bot.send_message(message.chat.id, conversation.hello_known.format(get_user_fio(message.from_user.id)[0]),
                         reply_markup=main_menu())


if __name__ == '__main__':
    telebot.apihelper.proxy = {'https': 'socks5h://192.168.77.130:9100'}
    print('Start Bot')
    bot.polling()