import sqlite3
import telebot
import random
from telebot import types


f = open('D:\pythonBot\Long projects.txt', 'r', encoding='UTF-8')
Long_projects = f.read().split('\n')
f.close()

f = open('D:\pythonBot\Short projects.txt', 'r', encoding='UTF-8')
Short_projects = f.read().split('\n')
f.close()

name = ''
surname = ''
age = 0

bot = telebot.TeleBot("2132622817:AAERWPT4LOAx8-dg4NN4l462g1ViTQI4TSs")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Добро пожаловать!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == 'Привет':
        bot.reply_to(message, 'Если вы хотите найти себе волонтёрский проект, то напишите- да')
    elif message.text == 'hi':
        bot.reply_to(message, 'Hi again! The bot creator!')
    elif message.text == 'да':
        bot.send_message(message.from_user.id, "Отлично, давайте познакомимся! Как вас зовут?")
        bot.register_next_step_handler(message, reg_name)

def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Какая у вас фамилия?")
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Сколько вам лет?")
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    #age = message.text
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Вводите цифрами!")

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Вам ' + str(age) + ' лет? И вас зовут: ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Приятно познакомиться! "
                                               "Напишите - project, для поиска нужного проекта")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Попробуем еще раз!")
        bot.send_message(call.message.chat.id, "Привет! Давай познакомимся! Как тебя зовут?")
        bot.register_next_step_handler(call.message, reg_name, project)

@bot.message_handler(content_types=["project"])
def project(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Долгие проекты")
    item2 = types.KeyboardButton("Короткие проекты")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id, 'Нажми: \nДолгие проекты для получения информации о действующих проектах.'
						'\nКороткие проекты — для получения информации о действующих проекта',  reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
	if message.text.strip() == 'Долгий проект':
		answer = random.choice(Long_projects)
	elif message.text.strip() == 'Поговорка':
		answer = random.choice(Short_projects)
		bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True, interval=0)
