import telebot
from telebot.types import *
from currency_converter import *

bot = telebot.TeleBot(token)
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start', 'convert'])
def convert(message):
    global amount
    conv = ReplyKeyboardMarkup(resize_keyboard=True)
    converter = KeyboardButton(text='/convert')
    conv.add(converter)
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Please enter amount to convert.', reply_markup=conv)
        bot.register_next_step_handler(message, convert)
        return

    if amount > 0:
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton(text='USD/EUR', callback_data='usd/eur')
        btn2 = InlineKeyboardButton(text='EUR/USD', callback_data='eur/usd')
        btn3 = InlineKeyboardButton(text='USD/GBP', callback_data='usd/gbp')
        btn4 = InlineKeyboardButton(text='GBP/USD', callback_data='gbp/usd')
        btn5 = InlineKeyboardButton(text='Another currency', callback_data='else')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4, btn5)
        bot.send_message(message.chat.id, 'Hi, to convert please click button', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Amount should be greater than 0.')
        bot.register_next_step_handler(message, convert)

#Main converter
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Result: {round(res, 2)}, you can enter amount again')
        bot.register_next_step_handler(call.message, convert)
    else:
        bot.send_message(call.message.chat.id, 'Enter 2 currencies by using /(like usd/jpy).')
        bot.register_next_step_handler(call.message, my_currency)

#Convert currencies that user would enter
def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Result: {round(res, 2)}, you can enter amount again')
        bot.register_next_step_handler(message, convert)
    except Exception:
        bot.send_message(message.chat.id, 'Something went wrong. Please try again')
        bot.register_next_step_handler(message, my_currency)

bot.polling(non_stop=True)
