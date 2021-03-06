import telebot
from telebot import types
import random
from bot_dir.models import bot_create_table, bot_connect_to, engine, Users, base, session
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from app import create_table

bot = telebot.TeleBot('1035683242:AAG_atEniKoa39BNoH5lweHZ1S3vS5zz2Rs')


@bot.message_handler(commands=['start'])
def start(message):
    user = Users(username=message.chat.id)
    session.add(user)
    try:
        session.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Hello', reply_markup=keyboard_start())


@bot.message_handler(content_types=['text'])
def message(message):
    if 'connecting to room' in message.text:
        return
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    user_obj = session.query(Users).filter_by(username=message.chat.id).one()
    if user_obj.active_room:
        if message.text == 'Disconnect':
            room = user_obj.active_room
            user_obj.active_room = None
            if user_obj.buffer_start:
                for i in range(user_obj.buffer_start, user_obj.buffer_end + 1):
                    print(i)
                    bot.delete_message(message.chat.id, i)
            user_obj.buffer_start, user_obj.buffer_end = None, None
            bot.send_message(message.chat.id, f'Disconnected from room{room}', reply_markup=keyboard_start())
        else:
            if not user_obj.buffer_start:
                user_obj.buffer_start = message.message_id
            user_obj.buffer_end = message.message_id
            room_obj = bot_connect_to(
                f'room{user_obj.active_room}')
            x = room_obj(user=message.chat.username, message=message.text)
            session.add(x)

    if message.text == 'Generate room':
        rand_id = random.randint(1000, 10000)
        if f'room{rand_id}' not in engine.table_names():
            bot_create_table(f'room{rand_id}')
            create_table(f'room{rand_id}')
            bot.send_message(message.chat.id, f'Room id: {rand_id}')
        else:
            message(message)

    session.commit()


@bot.inline_handler(func=lambda query: query.query == 'connect')
def inline_connection(query):
    rooms = []
    table_names = sorted([i.replace('room', '') for i in engine.table_names() if 'room' in i])
    for i, name in enumerate(table_names):
        rooms.append(types.InlineQueryResultArticle(id=name, title=name,
                                                    input_message_content=types.InputTextMessageContent(
                                                        f'connecting to room{name}...')))
    bot.answer_inline_query(query.id, rooms, cache_time=0)


@bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
def test_chosen(chosen_inline_result):
    print(chosen_inline_result)
    username = chosen_inline_result.from_user.username
    user_obj = session.query(Users).filter_by(username=username)
    if user_obj.active_room:
        bot.send_message(chosen_inline_result.from_user.id, f'Disconnected from {user_obj.active_room}')
    user_obj.active_room = chosen_inline_result.result_id
    bot.send_message(chosen_inline_result.from_user.id, f'Connected to {user_obj.active_room}',
                     reply_markup=room_keyboard())
    session.commit()


def keyboard_start():
    some = types.ReplyKeyboardMarkup(resize_keyboard=True)
    generate = types.KeyboardButton('Generate room')
    some.add(generate)
    return some


def room_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    disconnect = types.KeyboardButton('Disconnect')
    markup.add(disconnect)
    return markup


bot.polling()
