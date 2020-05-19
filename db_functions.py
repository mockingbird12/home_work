from db_driver import session
from db_driver import Users
from db_driver import User_State

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
    if session.query(User_State).filter(User_State.id == user_id).first():
        state = session.query(User_State).filter(User_State.id == user_id).first()
        return state.state
    else:
        return 'none'

def get_user_fio(user_id):
    if is_exsist(user_id):
        user = session.query(Users).filter(Users.id == int(user_id)).first()
        return user.first_name, user.second_name

def set_user_state(user_id, state):
    if session.query(User_State).filter(User_State.id == int(user_id)).first():
        user_state = session.query(User_State).filter(User_State.id == int(user_id)).first()
        user_state.state = state
    else:
        user_state = User_State(user_id, state)
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