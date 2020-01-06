import telebot
from telebot import types
import random
from app import db, create_table

bot = telebot.TeleBot('1035683242:AAG_atEniKoa39BNoH5lweHZ1S3vS5zz2Rs')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello', reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def message(message):
    if message.text == 'Generate room':
        print(message.chat.id)
        rand_id = random.randint(1000, 10000)
        if f'room{rand_id}' not in db.engine.table_names():
            create_table(f'room{rand_id}')
            bot.send_message(message.chat.id, f'Room id: {rand_id}')
        else:
            message(message)


def keyboard():
    some = types.ReplyKeyboardMarkup()
    rand = types.KeyboardButton('Generate room')
    some.add(rand)
    return some


bot.polling()
