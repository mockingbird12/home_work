import config
import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
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
    username = Column(Text)


    def __init__(self, first_name, username, user_id):
        self.first_name = first_name
        self.username = username
        self.user_id = user_id


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


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()