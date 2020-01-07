from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, clear_mappers, sessionmaker
import datetime

base = declarative_base()
metadata = MetaData()
engine = create_engine('sqlite:///bot_dir/bot.sqlite3')


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
    


def create_table(tablename):
    tabl_obj = connect_to(tablename).__table__.create(bind=engine)
    print(f'Table {tablename} created')
    return tabl_obj


def connect_to(tablename):
    class RoomHistory(base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}
        message_id = Column(Integer, primary_key=True)
        user = Column(String)
        message = Column(String)
        date = Column(DateTime, nullable=False, default=datetime.datetime.now())

    print(f'Class to {tablename} was created as object')
    return RoomHistory
