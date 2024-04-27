import telebot
from telebot import types


class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=1)

    def start_buttons(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtn = types.KeyboardButton('✅написать историю✅')
        markup.add(itembtn)
        return markup