from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, clear_mappers, sessionmaker
import datetime

base = declarative_base()
metadata = MetaData()
engine = create_engine('sqlite:///bot.sqlite3')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class RoomHistory(base):
    __tablename__ = 'roomhistory'
    __table_args__ = {'extend_existing': True}
    message_id = Column(Integer, primary_key=True)
    user = Column(String)
    message = Column(String)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now())


class Users(base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    active_room = Column(Integer)
    rooms_quantity = Column(String)
    buffer_start = Column(Integer)
    buffer_end = Column(Integer)


def bot_create_table(tablename):
    tabl_obj = bot_connect_to(tablename).__table__.create(bind=engine)
    print(f'Table {tablename} created')
    return tabl_obj


def bot_connect_to(tablename):
    class RoomHistory(base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}
        message_id = Column(Integer, primary_key=True)
        user = Column(String)
        message = Column(String)
        date = Column(DateTime, nullable=False, default=datetime.datetime.now())

    print(f'Class to {tablename} was created as object')
    return RoomHistory
