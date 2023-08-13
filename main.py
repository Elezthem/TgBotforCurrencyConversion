import telebot
import types
import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
import json
from telebot import types
import requests
import json
import sqlite3
from currency_converter import CurrencyConverter

bot = telebot.TeleBot('token')
#bot = Bot(config.BOT_TOKEN)
#dp = Dispatcher(bot)



# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await bot.send_invoice(message.chat.id, 'Покупка Nitro', 'Покупка Nitro Full ElezthemShop', 'invoce', config.PAYMENT_TOKEN, 'USD', [types.LabeledPrice('Покупка Nitro', 5 * 100)])

# @dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
# async def success(message: types.Message):
#     await message.answer(f'Success: {message.successful_payment.order_info}')

# @bot.message_handler()
# def info(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
#     elif message.text.lower() == 'id':
#         bot.reply_to(message, f'ID: {message.from_user.id}')

# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     markup = types.ReplyKeyboardMarkup()
#     markup.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://elezthem.github.io/MySiteforTeleBot/')))
#     await  message.answer('Привет, мой друг!', reply_markup=markup)



# @dp.message_handler(content_types=['web_app_data'])
# async def web_app(message: types.Message):
#     res = json.loads(message.web_app_data.data)
#     await message.answer(f'Name: {res["name"]}. Email: {res["email"]}. Phone: {res["phone"]}')

# @dp.message_handler(content_types=['photo']) #commands=['start']
# async def start(message: types.Message):
    #await bot.send_message(message.chat.id, 'Hello!')
    #await message.answer('Hello')
    # await message.reply('Hello User')
    #file = open('ludi.jpg', 'rb')
    #await message.answer_sticker(file)

# @dp.message_handler(commands=['inline'])
# async def info(message: types.Message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton('Site', url='https://discord.gg/vzaimnyi-vkhod-na-server-1067554815690952835m'))
#     markup.add(types.InlineKeyboardButton('Hello', callback_data='hello'))
#     await message.reply('Hello', reply_markup=markup)

# @dp.callback_query_handler()
# async def callback(call):
#     await call.message.answer(call.data)

# @dp.message_handler(commands=['reply'])
# async def reply(message: types.Message):
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#     markup.add(types.KeyboardButton('Instagram'))
#     markup.add(types.KeyboardButton('Discord'))
#     await message.answer('Hello', reply_markup=markup)


#@dp.message_handler(commands='start')
#async def start(message: types.Message):
#    markup = types.ReplyKeyboardMarkup()
#    markup.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://elezthem.com')))
#    await message.answer('Привет, я очень рада тебя видеть мой друг!', reply_markup=markup)

#@dp.message_handler(content_types=['photo']) #(commands=['start'])
#async def start(message: types.Message):
    #await bot.send_message(message.chat.id, 'Hello')
    #await message.answer('Hello')
    #await message.reply('Hello')
    #file = open('ludi.jpg', 'rb')
    #await message.answer_photo(file)


#@dp.message_handler(commands=['inline'])
#async def info(message: types.Message):
#    markup = types.InlineKeyboardMarkup()
#    markup.add(types.InlineKeyboardButton('Site', url='https://pornhub.com'))
#    markup.add(types.InlineKeyboardButton('Hello', callback_data='hello'))
#    await message.reply('Hello', reply_markup=markup)


#@dp.callback_query_handler()
#async def callback(call):
#    await call.message.answer(call.data)

#@dp.message_handler(commands=['reply'])
#async def reply(message: types.Message):
#    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#    markup.add(types.KeyboardButton('Site'))
#    markup.add(types.KeyboardButton('Website'))
#    await message.answer('Hello', reply_markup=markup)


#executor.start_polling(dp)

#bot = telebot.TeleBot('')
#API = ''
name = None
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат! Впишите сумму.')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больще за `0`! Впишите сумму.')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слэш')
        bot.register_next_step_handler(call.message, my_currency)



def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так. Впишите значение заново!')
        bot.register_next_step_handler(message, my_currency)


# @bot.message_handler(commands=['start'])
# def start(message):
#    mess = f'Привет, <b>{message.from_user.first_name} <v>{message.from_user.last_name}</u></b>'
#    bot.send_message(message.chat.id, mess, parse_mode='html')



# @bot.message_handler(content_types=['text'])
# def get_user_text(message):
#    if message.text == "Hello":
#       bot.send_message(message.chat.id, "И тебе приветик минетик!", parse_mode='html')
#  elif message.text == "id":
#     bot.send_message(message.chat.id, f"Твой ID: {message.from_user.id}", parse_mode="html")
#   elif message.text == "photo":
#       photo = open('tel.jpg', 'rb')
#       bot.send_photo(message.chat.id, photo)
#   else:
#       bot.send_message(message.chat.id, "Я тебя не понимаю ь-ь", parse_mode='html')


#@bot.message_handler(content_types=['photo'])
#def get_user_photo(message):
#    bot.send_message(message.chat.id, 'Вау крутая фотка!')


#@bot.message_handler(commands=['website'])
#def website(message):
#    markup = types.InlineKeyboardMarkup()
#    markup.add(types.InlineKeyboardButton("Посетить веб сайт", url="https://elezthem.com"))
#    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)


#@bot.message_handler(commands=['start'])
#def start(message):
#    conn = sqlite3.connect('elezthem.sql')
#    cur = conn.cursor()

#    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
#    conn.commit()
#    cur.close()
#    conn.close()

#    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегестрируем! Введите ваше имя')
#    bot.register_next_step_handler(message, user_name)


#@bot.message_handler(commands=['start'])
#def start(message):
#    bot.send_message(message.chat.id, "Привет! Рад тебя видеть, напиши название города")


#@bot.message_handler(content_types=['text'])
#def get_weather(message):
#    city = message.text.strip().lower()
#    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
#    if res.status_code == 200:
#        data = json.loads(res.text)
#        temp = data["main"]["temp"]
#        bot.reply_to(message, f'Сейчас погода: {temp}')

#        image = 'ludi.jpg' if temp > 5.0 else 'lox.jpg'
#        file = open('./' + image, 'rb')
#        bot.send_photo(message.chat.id, file)
#    else:
#        bot.reply_to(message, f"Город указан не верно!")

# @bot.message_handler(commands=['help'])
# def website(message):
#    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#    website = types.KeyboardButton('Веб сайт')
#    start = types.KeyboardButton('Start')
#    markup.add(website, start)
#    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)

#def user_name(message):
#    global name
#    name = message.text.strip()
#    bot.send_message(message.chat.id, 'Введите пароль')
#    bot.register_next_step_handler(message, user_pass)

#def user_pass(message):
#    password = message.text.strip()

#    conn = sqlite3.connect('elezthem.sql')
#    cur = conn.cursor()

#    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
#    conn.commit()
#    cur.close()
#    conn.close()

#    markup = telebot.types.InlineKeyboardMarkup()
#    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
#    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)

#@bot.callback_query_handler(func=lambda call: True)
#def callback(call):
#    conn = sqlite3.connect('elezthem.sql')
#    cur = conn.cursor()
#
#    cur.execute('SELECT * FROM users')
#    users = cur.fetchall()

 #   info = ''
#    for el in users:
#        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

#    cur.close()
#    conn.close()

#    bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)
