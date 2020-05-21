import telebot
import config
import conversation
import state
from telebot.types import ReplyKeyboardRemove
from db_functions import is_exsist
from db_functions import set_user_state
from db_functions import get_user_state
from db_functions import add_user
from db_functions import delete_user_state
from db_functions import get_user_fio
from db_functions import insert_file
from db_functions import get_random_task
from db_functions import set_task_check
from db_functions import get_user_task
from db_functions import set_task_mark
from db_functions import get_all_user_task
from db_functions import get_mark
from db_functions import get_all_users
from db_functions import get_user_id_by_name
from db_functions import set_task_comment
from markups import main_menu, marks_markup, students_tasks

bot = telebot.TeleBot(config.token)

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == state.add_comment)
def add_comment(message):
    print('add_comment')
    comment = message.text
    task_id = get_user_task(message.from_user.id)
    set_task_comment(task_id, comment)
    delete_user_state(message.from_user.id)
    bot.send_message(message.chat.id, conversation.thanks_comment, reply_markup=ReplyKeyboardRemove)


@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == state.check_the_job)
def set_the_mark(message):
    print('set_the_mark')
    mark = message.text
    task_id = get_user_task(message.from_user.id)
    set_task_check(task_id, True)
    set_task_mark(task_id, mark)
    # delete_user_state(message.from_user.id)
    set_user_state(message.from_user.id, state.add_comment, task_id=task_id)
    bot.send_message(message.chat.id, conversation.thanks, reply_markup=main_menu())

@bot.message_handler(func= lambda message: message.text == 'Проверить задание')
def check_someone(message):
    print('check_someone')
    bot.send_message(message.chat.id, 'Проверить задание')
    task_id, file_id = get_random_task()
    if task_id:
        set_user_state(message.chat.id, state.check_the_job, task_id=task_id)
        set_task_check(task_id, True)
        bot.send_document(message.chat.id,file_id, reply_markup=marks_markup())
    else:
        bot.send_message(message.chat.id, conversation.no_tasks, reply_markup=main_menu())

@bot.message_handler(func= lambda message: message.text == 'Сдать задание на проверку')
def take_job(message):
    print('take_job')
    bot.send_message(message.chat.id, 'Загрузите свое задание')
    set_user_state(message.from_user.id, state.take_the_job)

@bot.message_handler(func= lambda message: message.text == 'Узнать свои оценки')
def know_mark(message):
    bot.send_message(message.chat.id, 'Узнать свои оценки')
    user_tasks = get_all_user_task(message.from_user.id)
    delete_user_state(message.from_user.id)
    for one_task in user_tasks:
        bot.send_message(message.chat.id, '{0} - {1}'.format(one_task.file_name, get_mark(one_task.id).mark))

@bot.message_handler(content_types=['document'])
def upload_job(message):
    bot.send_message(message.chat.id, 'upload message')
    file = message.document.file_id
    file_name = message.document.file_name
    insert_file(message.chat.id, file, file_name)
    delete_user_state(message.from_user.id)
    bot.send_message(message.chat.id, conversation.success_upload.format(get_user_fio(message.from_user.id)[0]),
                     reply_markup=main_menu())

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == state.admin_task)
def get_student_tasks(message):
    first_name = message.text.split()[0]
    second_name = message.text.split()[1]
    delete_user_state(message.from_user.id)
    user_id = get_user_id_by_name(first_name, second_name)
    tasks = get_all_user_task(user_id)
    if tasks:
        for task in tasks:
            bot.send_document(message.chat.id, task.file_id)
    else:
        bot.send_message(message.chat.id, conversation.no_tasks)

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == state.enter_fio)
def get_fio(message):
    fio = message.text.split()
    if len(fio) == 2:
        if fio[0].isalnum() and fio[1].isalnum():
            add_user(message.from_user.id, fio[0], fio[1])
            delete_user_state(message.from_user.id)
            bot.send_message(message.chat.id, conversation.hello_known.format(get_user_fio(message.from_user.id)[0]),
                             reply_markup=main_menu())

@bot.message_handler(commands=['admin_table'])
def admin_info(message):
    users = get_all_users()
    res = ''
    for user in users:
        tasks = get_all_user_task(user.id)
        for task in tasks:
            mark = get_mark(task.id)
            res += '\t\t'.join([str(user.first_name),str(user.second_name),str(task.file_name),str(mark.mark),
                             str(mark.comment)])+'\n'
    bot.send_message(message.chat.id, res)

@bot.message_handler(commands=['admin_tasks'])
def admin_tasks(message):
    set_user_state(message.from_user.id, state.admin_task)
    bot.send_message(message.chat.id, 'Работы', reply_markup=students_tasks())

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
    bot.polling(none_stop=True,timeout=123)