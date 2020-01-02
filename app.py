from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
app = Flask(__name__)

# Database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# SocketIO
socketio = SocketIO(app)


class Room(db.Model):
    room_id = db.Column(db.Integer)


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    socketio.run(app)
