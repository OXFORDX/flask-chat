from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import datetime
import json
import telebot

app = Flask(__name__)

# Database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SocketIO
socketio = SocketIO(app)


class Rooms(db.Model):
    room_id = db.Column(db.Integer, primary_key=True)
    online_users = db.Column(db.String)


def create_table(tablename):
    tabl_obj = connect_to(tablename).__table__.create(db.session.bind)
    print(f'Table {tablename} created')
    return tabl_obj


def connect_to(tablename):
    class RoomHistory(db.Model):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}
        message_id = db.Column(db.Integer, primary_key=True)
        user = db.Column(db.String)
        message = db.Column(db.String)
        date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    print(f'Class to {tablename} was created as object')
    return RoomHistory


@app.route('/')
def hello_world():
    return render_template('room_selector.html')


@app.route('/room')
def room():
    return render_template('room.html')


@socketio.on('json')
def handle_message(message):
    print(message)


@socketio.on('room_connect')
def connection(message):
    username = message['username']
    room_id = message['room']
    if f'room{room_id}' in db.engine.table_names():
        table_obj = connect_to(f'room{room_id}')
        return socketio.emit('redirect', {'url': url_for('room')})
    else:
        socketio.emit('RoomDoesNotExist')


if __name__ == '__main__':
    socketio.run(app)
