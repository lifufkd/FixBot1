import os
import platform
from frontend import Bot_inline_btns
from config_parser import ConfigParser
from backend import TempUserData
import telebot
from telebot import types

# Токен вашего бота
config_name = 'secrets.json'


def delete_msg(user_id):
    try:
        bot.delete_message(user_id, temp_user_data.temp_data(user_id)[user_id][1])
    except:
        pass


def main():
    # Обработчик команды /start и вывод клавиатуры с кнопкой "Написать историю"
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        user_id = message.chat.id
        buttons = Bot_inline_btns()
        delete_msg(user_id)
        message_id = bot.send_message(message.chat.id, "Приветствуем тебя в канале MIRAGE! Мы рады, что ты решил присоединиться к нам "
                                          "и поделиться своей историей. Ждем с нетерпением твоих увлекательных повествований "
                                          "и вдохновляющих идей", reply_markup=buttons.start_buttons()).message_id
        temp_user_data.temp_data(user_id)[user_id][1] = message_id


    # Обработчик для кнопки "Написать историю"
    @bot.message_handler(content_types=['text', 'photo', 'video'])
    def txt_msg(message):
        user_id = message.chat.id
        user_input = message.text
        buttons = Bot_inline_btns()
        delete_msg(user_id)
        if user_input == '✅написать историю✅':
            bot.delete_message(user_id, message.id)
            message_id = bot.send_message(message.chat.id, "Пожалуйста, напишите свою историю:").message_id
            temp_user_data.temp_data(user_id)[user_id][1] = message_id
        else:
            bot.forward_message(config.get_config()['group_id'], user_id, message.id)
            bot.delete_message(user_id, message.id)
            message_id = bot.send_message(user_id, '✅история отправлена на проверку✅', reply_markup=buttons.start_buttons()).message_id
            temp_user_data.temp_data(user_id)[user_id][1] = message_id

    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()