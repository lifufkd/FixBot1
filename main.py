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
        code = temp_user_data.temp_data(user_id)[user_id][0]
        delete_msg(user_id)
        if user_input == '✅написать историю✅':
            bot.delete_message(user_id, message.id)
            temp_user_data.temp_data(user_id)[user_id][0] = 0
            message_id = bot.send_message(message.chat.id, "Пожалуйста, напишите свою историю:").message_id
            temp_user_data.temp_data(user_id)[user_id][1] = message_id
        elif code == 0:
            temp_user_data.temp_data(user_id)[user_id][0] = None
            bot.delete_message(user_id, message.id)
            if message.text:
                bot.send_message(config.get_config()['group_id'], message.text)
            # Если сообщение содержит фотографию, отправляем её
            if message.photo:
                # Получаем информацию о фотографии
                photo = message.photo[-1]
                # Отправляем фотографию в ваш чат
                bot.send_photo(config.get_config()['group_id'], photo.file_id)
            # Если сообщение содержит видео, отправляем его
            if message.video:
                # Получаем информацию о видео
                video = message.video
                # Отправляем видео в ваш чат
                bot.send_video(config.get_config()['group_id'], video.file_id)
            message_id = bot.send_message(user_id, '✅история отправлена на проверку✅').message_id
            temp_user_data.temp_data(user_id)[user_id][1] = message_id

    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()