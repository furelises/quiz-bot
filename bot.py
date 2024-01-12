import telebot
import info
from dotenv import dotenv_values
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

config = dotenv_values(".env")
token = config['token']
bot = telebot.TeleBot(token=token)


def create_menu(list: [info.Btn]) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for i in list:
        btn = types.InlineKeyboardButton(text=i.title, callback_data=i.id)
        markup.add(btn)
    return markup


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id,
                     'Привет,это бот_анкета, который поможет тебе определить свой цветотип. Я надеюсь, что вам понравится моя работа и вы прорекламируете меня друзьям!😁(Еще бот умеет отвечать на простые сообщения, типа - привет или пока)')
    bot.send_message(message.chat.id, "Это список команд, которые я умею выполнять:\n"
                                      "/start ; Приветствует пользователя и отправляет ему меню.\n"
                                      "/help ; Предоставляет пользователю инструкцию по использованию бота и отправляет ему меню.\n"
                                      "/play ; Начинает или продолжает прохождение анкеты.\n"
                                      "/restart ; Начинает прохождение анкеты заново.\n")
    bot.send_message(message.chat.id, info.project_to_str())


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, 'Инструкция пользования ботом_анкетой : ...')
    bot.send_message(message.chat.id, "Это меню команд, которые я умею выполнять:\n"
                                      "/start ; Приветствует пользователя и отправляет ему меню.\n"
                                      "/help ; Предоставляет пользователю инструкцию по использованию бота и отправляет ему меню.\n"
                                      "/play ; Начинает или продолжает прохождение анкеты.\n"
                                      "/restart ; Начинает прохождение анкеты заново.\n")


def next_question(user, chat_id):
    question = user.get_next_question()
    answer = user.get_answer()
    if question == None:
        bot.send_message(chat_id, "анкета завершена.")
        bot.send_photo(chat_id, open(answer['image'], 'rb'))
        bot.send_message(chat_id, answer['title'])
        return
    list = info.questions_list[question]["list"]
    title = info.questions_list[question]["title"]
    bot.send_message(chat_id, title, reply_markup=create_menu(list))


@bot.message_handler(commands=['play'])
def play_command(message):
    user_id = message.from_user.id
    user = info.User(user_id)
    next_question(user, message.chat.id)


@bot.message_handler(commands=['restart'])
def play_command(message):
    user_id = message.from_user.id
    user = info.User(user_id)
    user.restart()
    bot.send_message(message.chat.id, "Нажмите /play чтобы начать анкету заново.")


@bot.message_handler(content_types=['text'])
def hello_saying(message):
    if "привет" in message.text.lower():
        bot.send_message(message.chat.id, "Привет!")
    elif "пока" in message.text.lower():
        bot.send_message(message.chat.id, "Пока!")
    else:
        bot.send_message(message.chat.id, "Я подумаю об этом ... :)")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.from_user.id
    user = info.User(user_id)
    user.handler(call.data)
    next_question(user, call.message.chat.id)


@bot.message_handler(content_types=['text'])
def handle_start(message: Message):
    if message.text == 'pass':
        pass


bot.polling()
