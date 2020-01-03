from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import datetime

app = Flask(__name__)

# Database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# SocketIO
socketio = SocketIO(app)


class Room(db.Model):
    room_id = db.Column(db.Integer, primary_key=True)
    online_users = db.Column(db.String)


def uniq_table(tablename):
    class RoomHistory(db.Model):
        __tablename__ = tablename
        id = db.Column(db.Integer, primary_key=True)
        user = db.Column(db.String)
        message = db.Column(db.String)
        date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    RoomHistory.__table__.create(db.session.bind)
    return RoomHistory


def connect_to(tablename):
    class RoomHistory(db.Model):
        __tablename__ = tablename
        id = db.Column(db.Integer, primary_key=True)
        user = db.Column(db.String)
        message = db.Column(db.String)
        date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    return RoomHistory


o = connect_to('ROOM123')(user='ok', message='NONOE')
db.session.add(o)
db.session.commit()


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    socketio.run(app)
