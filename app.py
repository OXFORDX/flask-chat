from flask import Flask, render_template, redirect, url_for, session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import datetime
import json
import telebot


bot = telebot.TeleBot('1035683242:AAG_atEniKoa39BNoH5lweHZ1S3vS5zz2Rs')

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


@app.route('/room/<int:roomid>/')
def room(roomid):
    table_obj = connect_to(f'room{roomid}').query.all()
    return render_template('room.html', roomid=roomid, table=table_obj)


@socketio.on('message_send')
def handle_message(data):
    table_obj = connect_to(f'room{data["room_id"]}')
    username = data['username']
    message_obj = table_obj(user=username, message=data['message'])
    print(f'====\nUser: {message_obj.user}\n'
          f'Message: {message_obj.message}\n====')
    bot.send_message(370091393, f'*{message_obj.user}*\n{message_obj.message}', parse_mode="Markdown")
    db.session.add(message_obj)
    db.session.commit()


@socketio.on('room_connect')
def connection(message):
    room_id = message['room']
    if f'room{room_id}' in db.engine.table_names():
        table_obj = connect_to(f'room{room_id}')
        return socketio.emit('redirect', {'url': f'room/{room_id}', 'room_id': room_id})
    else:
        socketio.emit('RoomDoesNotExist')


if __name__ == '__main__':
    socketio.run(app)
