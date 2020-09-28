import telebot, time
from random import choice
from telebot import types
import config
from data_base import User

bot = telebot.TeleBot(config.TOKEN)

db = User("data.db")

undone_time = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))

bad_advice_list = db.copy_bad_advice()
choice_advice_list = db.copy_choice_advice()
rest_list = db.copy_rest()
helper_list = db.copy_helper()

@bot.message_handler(commands=['start'])
def menu(message):
    bot.send_message(message.chat.id, text='Вот что я умею: ', reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def message_handler(message):
    user_id = message.from_user.id
    stat = undone_time(message.date)
    if (not db.get_all_id(user_id)):
        db.add_id_to_db(user_id)
    if (not db.get_stat(user_id)):
        db.add_stat(user_id, stat)
    if message.text:
        db.update_stat(stat, user_id)

    if message.text == 'Вредные советы':
        global bad_advice_list
        bad_choice = choice(bad_advice_list)
        index = bad_advice_list.index(bad_choice)
        bad_message = bad_advice_list.pop(index)
        bot.reply_to(message, bad_message)
        if len(bad_advice_list) == 0:
            bad_advice_list = db.copy_bad_advice().copy()

    if message.text == 'Советы по выбору':
        global choice_advice_list
        advice_choice = choice(choice_advice_list)
        index = choice_advice_list.index(advice_choice)
        advice_message = choice_advice_list.pop(index)
        bot.reply_to(message, advice_message)
        if len(choice_advice_list) == 0:
            choice_advice_list = db.choice_advice().copy()

    if message.text == 'Как отдыхать?':
        global rest_list
        rest_choice = choice(rest_list)
        index = rest_list.index(rest_choice)
        rest_message = rest_list.pop(index)
        if rest_choice[1] == '0':
            bot.reply_to(message, rest_message)
        else:
            bot.reply_to(message, f'{rest_message[0]} {rest_choice[1]}')
        if len(rest_list) == 0:
            rest_list = db.copy_rest().copy()


    if message.text == 'Поддержка':
        global helper_list
        help_choice = choice(helper_list)
        index = helper_list.index(help_choice)
        help_message = helper_list.pop(index)
        bot.reply_to(message, help_message)
        if len(helper_list) == 0:
            helper_list = db.copy_helper().copy()

    if message.text == 'Досье научруков':
        bot.send_message(message.chat.id, text='Выберите ваше научного руководителя: ', reply_markup=inline_keyboard())


def inline_keyboard():
    markup_inline = types.InlineKeyboardMarkup()
    item_1 = types.InlineKeyboardButton(text='Логинов Никита Иванович', callback_data='Логинов')
    item_2 = types.InlineKeyboardButton(text='Бангура Мариам', callback_data='Бангура')
    markup_inline.add(item_1, item_2)
    return markup_inline


def start_keyboard():
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton('Старт')
    start_markup.add(start_button)
    return start_markup


def keyboard():
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    bad_advice = types.KeyboardButton('Вредные советы')
    choice_advice = types.KeyboardButton('Советы по выбору')
    resume = types.KeyboardButton('Досье научруков')
    rest = types.KeyboardButton('Как отдыхать?')
    helper = types.KeyboardButton('Поддержка')
    markup_menu.add(bad_advice, choice_advice, resume, rest, helper)
    return markup_menu


@bot.callback_query_handler(func=lambda call: True)
def resumes(call):
    result = db.get_resumes()
    if call.data == 'Логинов':
        bot.send_photo(call.message.chat.id, 'https://imbt.ga/HVkXc7eBcz', caption=result[0])
    if call.data == 'Бангура':
        bot.send_photo(call.message.chat.id, 'https://imbt.ga/KrQP5E7VUy', caption=result[1])


if __name__ == '__main__':
    bot.polling(none_stop=True)
