import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove, KeyboardButton


TOKEN = '7062809223:AAHoRKMaFGUq--eqZ6VnEOzuAToBF9FKwPs'
bot = telebot.TeleBot(TOKEN)
new_human = []
eho_flag = False
podbor_flag = False

letters = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя-'


class Human:
    def __init__(self, name='Стас', car=None, money=None):
        self.name = name
        self.car = car
        self.money = money


@bot.message_handler(commands=['start'])
def start(message):
    global eho_flag, podbor_flag, new_human
    new_human = []
    eho_flag = False
    podbor_flag = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Эхо-бот")
    item2 = types.KeyboardButton("Подбор машины")
    markup.add(item1, item2)
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}! Я бот, созданный Borisovgang, работающий '
                     f'как Эхо-бот и помощник для подбора машины.',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def process_messages(message):
    global eho_flag, podbor_flag

    if eho_flag is True:
        bot.send_message(message.chat.id, message.text)
    elif message.text == 'Эхо-бот':
        eho_flag = True
        podbor_flag = False
        bot.send_message(message.chat.id, f'Эхо-бот включен', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Подбор машины':
        eho_flag = False
        podbor_flag = True
        bot.send_message(message.chat.id,
                         f'{message.from_user.first_name}, подбор машины работает!')
        message = bot.reply_to(message, 'Пожалуйста введите свой никнейм из паспорта(личный ник, и ник родаков',
                               reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_name_step)

    elif message.text == 'Исправить':
        message = bot.reply_to(message, 'Пожалуйста введите свой никнейм из паспорта(личный ник, и ник родаков',
                               reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_name_step)

    elif message.text == 'Отправить заявку':
        link = get_link(new_human[-1].car)

        bot.send_message(message.chat.id, f'{link}')
        bot.send_message(chat_id=-4251956203, text=f'Никнейм из паспорта:{new_human[-1].name}\n'
                                                   f'Марка машины:{new_human[-1].car}\nЦена за которую '
                                                   f'хотели бы купить машину:{new_human[-1].money}')
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, данные отправлены',
                         reply_markup=types.ReplyKeyboardRemove())


def process_name_step(_message):
    try:

        name = _message.text

        if not isinstance(name, str):
            _message = bot.reply_to(_message, 'Никнейм из цифр, ты что на por..hube регаешься?')
            bot.register_next_step_handler(_message, process_name_step)
            return
        temp_name = name.lower()
        temp_name = temp_name.split()
        if len(temp_name) < 2:
            _message = bot.reply_to(_message, 'Ник твой и Ник родаков - это 2 слова')
            bot.register_next_step_handler(_message, process_name_step)
            return

        for s in temp_name:
            if len(s.strip(letters)) != 0:
                _message = bot.reply_to(_message, 'В такими символами в нике только в дотку на 500MMR играть!')
                bot.register_next_step_handler(_message, process_name_step)
                return

        user = Human(name)
        new_human.append(user)
        _message = bot.reply_to(_message, 'Если ты хочешь приобрести Жигули, напиши "жигули" или '
                                          f'"zhiguli", и я отправлю тебе прекрасный вариант этого автомобиля. '
                                          f'Можешь также написать марку '
                                          f'другой машины и получишь ссылку на сайт.')
        bot.register_next_step_handler(_message, process_car_step)
    except Exception:
        bot.reply_to(_message, 'Пардон, ты умудрился наи..ть систему проверки, но работать так ботяра не будет!')


def process_car_step(message):
    try:
        car = message.text

        if not isinstance(car, str):
            message = bot.reply_to(message, 'Что это за марка тачилы из цифр?? А ну повтори!')
            bot.register_next_step_handler(message, process_car_step)
            return
        temp_car = car.lower()

        for s in temp_car:
            if len(s.strip(letters)) != 0:
                message = bot.reply_to(message, 'Что за левые символы в марке тачилы? Повторяй')
                bot.register_next_step_handler(message, process_car_step)
                return

        new_human[-1].car = car
        message = bot.reply_to(message, 'Сколько у Вас денег для покупки?')
        bot.register_next_step_handler(message, process_money_step)  # Пошаговый запрос
    except Exception:
        bot.reply_to(message, 'Пардон, ты умудрился наи..ть систему проверки, но работать так ботяра не будет!')


def process_money_step(message):
    try:

        money = message.text
        if not money.isdigit() or int(money) < 0:
            message = bot.reply_to(message,
                                   'Т.е у тебя походу уже есть потраченный кредит, а ты еще и машину купить'
                                   ' хочешь. Силен!')
            bot.register_next_step_handler(message, process_money_step)
            return

        new_human[-1].money = money

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Отправить заявку")
        item2 = types.KeyboardButton("Исправить")
        markup.add(item1, item2)

        bot.send_message(message.chat.id,
                         text=f'Никнейм из паспорта:{new_human[-1].name}\nМарка машины:{new_human[-1].car}\nЦена за которую '
                              f'хотели бы купить машину:{new_human[-1].money}. Все верно?',
                         reply_markup=markup)

    except Exception:
        bot.reply_to(message, 'Пардон, ты умудрился наи..ть систему проверки, но работать так ботяра не будет!')


def get_link(message):
    model = message.lower()
    if model == 'жигули' or model == 'zhiguli':
        link = "https://cars.av.by/lada-vaz/2106/100771444"
    else:
        link = "https://cars.av.by"
    return link


bot.polling(none_stop=True, interval=0)
