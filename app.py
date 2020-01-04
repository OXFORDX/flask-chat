from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import datetime

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
        id = db.Column(db.Integer, primary_key=True)
        user = db.Column(db.String)
        message = db.Column(db.String)
        date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    print(f'Class to {tablename} was created as object')
    return RoomHistory


o = create_table('room123456789')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    socketio.run(app)
