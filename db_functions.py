from db_driver import session
from db_driver import Users
from db_driver import User_State
from db_driver import Users_tasks
from db_driver import Marks
import random

def is_exsist(user_id):
    """
    Функция для провекри существования каких-либо сущностей
    (пользователей и т.д)
    :param kwargs:
    :return:
    """
    if session.query(Users).filter(Users.id == int(user_id)).first():
        return True
    else:
        return False

def get_user_state(user_id):
    state = session.query(User_State).filter(User_State.id == user_id).first()
    if state:
        return state.state
    else:
        return 'none'

def get_user_id_by_name(first_name, second_name):
    user = session.query(Users).filter(Users.first_name == first_name).filter(Users.second_name == second_name).first()
    if user:
        return user.id

def get_user_task(user_id):
    state = session.query(User_State).filter(User_State.id == user_id).first()
    if state:
        return state.task_id
    else:
        return 'none'

def get_all_user_task(user_id):
    users_tasks = session.query(Users_tasks).filter(Users_tasks.user_id == user_id).all()
    return users_tasks

def get_all_users():
    users = session.query(Users).all()
    return users

def get_user_fio(user_id):
    if is_exsist(user_id):
        user = session.query(Users).filter(Users.id == int(user_id)).first()
        return user.first_name, user.second_name

def set_user_state(user_id, state, task_id = None):
    if session.query(User_State).filter(User_State.id == int(user_id)).first():
        user_state = session.query(User_State).filter(User_State.id == int(user_id)).first()
        user_state.state = state

    else:
        user_state = User_State(user_id, state)
    if task_id: user_state.task_id = task_id
    session.add(user_state)
    session.commit()

def delete_user_state(user_id):
    if session.query(User_State).filter(User_State.id == int(user_id)).first():
        user_state = session.query(User_State).filter(User_State.id == int(user_id)).first()
        session.delete(user_state)
        session.commit()

def add_user(user_id, first_name, second_name):
    user = Users(user_id, first_name, second_name)
    session.add(user)
    session.commit()

def insert_file(user_id, file_id, file_name):
    if not session.query(Users_tasks).filter(Users_tasks.file_name == file_name).first():
        user_task = Users_tasks(user_id, file_id, file_name)
        user_task.is_checked = False
        session.add(user_task)
        session.commit()
    else:
        print('Error insert_file')

def get_random_task():
    tasks = session.query(Users_tasks).filter(Users_tasks.is_checked == False).all()
    if tasks:
        # length = tasks.count()
        if len(tasks) > 1:
            task = tasks[random.randint(0, len(tasks))]
            return task.id, task.file_id
        else:
            return tasks[0].id, tasks[0].file_id
    else:
        return None, None

def set_task_check(task_id, status):
    task = session.query(Users_tasks).filter(Users_tasks.id == task_id).first()
    if task:
        task.is_checked = status
        session.add(task)
        session.commit()

def set_task_mark(task_id, mark):
    mark = Marks(task_id, mark)
    session.add(mark)
    session.commit()

def set_task_comment(task_id, comment):
    mark = session.query(Marks).filter(Marks.task_id == task_id).first()
    mark.comment = comment
    session.add(mark)
    session.commit()

def get_mark(task_id):
    mark = session.query(Marks).filter(Marks.task_id == task_id).first()
    if mark:
        return mark

if __name__ == "__main__":
    get_random_task()