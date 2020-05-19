import config
import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Sequence
from sqlalchemy import ForeignKey


user = config.db_user
passwd = config.db_passwd
host = config.db_host
dbname = config.db_name

Base = declarative_base()
engine = create_engine("postgresql://{0}:{1}@{2}/{3}".format(user, passwd, host, dbname))

class Users(Base):
    """
    Таблица с именами фамилиями пользователей
    """
    __tablename__ = 'users'
    id = Column(Integer, unique=True, primary_key=True)
    first_name = Column(Text)
    second_name = Column(Text)


    def __init__(self, user_id, first_name, second_name):
        self.first_name = first_name
        self.username = second_name
        self.id = user_id


class User_State(Base):
    """
    Таблица для отслеживания статуса пользователя
    """
    __tablename__ = 'user_state'
    id = Column(Integer, primary_key=True)
    state = Column(Text)

    def __init__(self, user_id, state):
        self.id = user_id
        self.state = state

class Users_tasks(Base):
    """
    Таблица с заданиями пользователей
    """
    __tablename__ = 'users_tasks'
    id = Column(Integer, Sequence('users_tasks_seq'), primary_key=True)
    user_id = Column(Integer)
    file_id = Column(Text)

    def __init__(self, user_id, file_id):
        self.user_id = user_id
        self.file_id = file_id


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()