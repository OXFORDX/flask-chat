import telebot
from telebot import types
import random
from bot_dir.models import create_table, connect_to, engine
import re

bot = telebot.TeleBot('1035683242:AAG_atEniKoa39BNoH5lweHZ1S3vS5zz2Rs')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello', reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def message(message):
    if message.text == 'Generate room':
        rand_id = random.randint(1000, 10000)
        if f'room{rand_id}' not in engine.table_names():
            create_table(f'room{rand_id}')
            bot.send_message(message.chat.id, f'Room id: {rand_id}')
        else:
            message(message)


@bot.inline_handler(func=lambda query: query.query == 'connect')
def inline_connection(query):
    print(query.query)
    rooms = []
    table_names = sorted([int(i.replace('room', '')) for i in engine.table_names()])
    print(table_names)
    for i, name in enumerate(table_names):
        print(name)
        rooms.append(types.InlineQueryResultArticle(id=name, title=name,
                                                    input_message_content=types.InputTextMessageContent(
                                                        f'connecting to room{name}...', )))
    print(rooms)
    bot.answer_inline_query(query.id, rooms, cache_time=0)


@bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
def test_chosen(chosen_inline_result):
    table_obj = connect_to(f'room{chosen_inline_result.result_id}')
    bot.send_message(chosen_inline_result.from_user.id, 'Connected')


def keyboard():
    some = types.ReplyKeyboardMarkup()
    rand = types.KeyboardButton('Generate room')
    some.add(rand)
    return some


bot.polling()
