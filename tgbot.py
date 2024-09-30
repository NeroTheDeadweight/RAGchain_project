import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Chat_History, create_tables
from chatGPT_For_tgbot import gpt
from telebot import types
from dotenv import load_dotenv
import os
from sqldb_int import get_chat_history, save_todb

create_tables()
def tgbot():
    load_dotenv()
    key = os.getenv('TELEBOT_KEY')
    bot = telebot.TeleBot(key)

    list_of_bot_commands = ('/start', '/history', '/help', '/chatgpt', '/photo')



    @bot.message_handler(commands=['start', 'help'])
    def help_list(message):
        bot.send_message(message.chat.id, "Список команд:" + '\n' + "/start, /help, /chatgpt, /photo")
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEIqKxm7uBan7yMW1D3ap2pfG7BLvJroQAC1k0AApMnKEkhdxhnWZvD3zYE")

    @bot.message_handler(commands=['history'])
    def get_history_command(message):
        try:
            for p in get_chat_history():
                p = str(p)
                bot.send_message(message.chat.id, p)
        except:
            print("История - это ложь")

    @bot.message_handler(commands=['photo'])
    def get_photo(message):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://google.com'))
        markup.add(types.InlineKeyboardButton('Удалить фото', callback_data='delete'))
        markup.add(types.InlineKeyboardButton('Изменить текст', callback_data='edit'))
        bot.reply_to(message, 'Найс фото!', reply_markup=markup)

    @bot.message_handler(commands=['start'])
    def main(message):
        bot.send_message(message.chat.id, "Дарова, бандит. Это чат-бот на основе модели gpt 3.5🔥\nПриступим!")

    @bot.message_handler(commands=['chatgpt'])
    def get_question(message):
        bot.send_message(message.chat.id, "Ведите вопрос для нейросети:")
        bot.register_next_step_handler(message, ai_message(message))

    def ai_message(message):
        answer = gpt(message.text)
        bot.send_message(message.chat.id, answer)
        save_todb(answer)

    @bot.message_handler()
    def writing_todb(message):
        if message.text not in list_of_bot_commands:
            save_todb(message.text)
        get_chat_history()

    bot.polling(none_stop=True)


if __name__ == '__main__':
    tgbot()
