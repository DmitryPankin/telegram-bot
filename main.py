import os
import telebot
from requests_api import base_functions, bestdeal, highprice, lowprice, history
from dotenv import load_dotenv
from telebot import types
from database.CRUD import Interface
from database import models
from database.models import db, History

load_dotenv()
result = dict()

models.db_create()
write_history = Interface.create()
reade_history = Interface.retrieve()


def get_commands(message) -> None:
    """Изменение параметров запроса к API в зависимости от полученной команды.
       Если команда history - вывод истории запросов
    """
    command = message.text
    if message.text not in ['/lowprice', '/bestdeal', '/highprice', '/history']:
        bot.send_message(message.from_user.id, "Надо нажать на кнопку!!!", reply_markup=None)

    if command == '/lowprice':
        lowprice.change_params()
        get_city(message)
    elif command == '/history':
        user_id = str(message.from_user.id)
        response_database = reade_history(db, History, History.created_request, History.user_id, History.request)
        result_out = history.out_history(response_database, user_id)

        for result_next in result_out:
            bot.send_message(message.from_user.id, f"Ваша история: \n{result_next}", reply_markup=None)
        bot.send_message(message.from_user.id, "Хочешь ещё? Выбери и нажми кнопку!' ", reply_markup=None)

    elif command == '/highprice':
        highprice.change_params_commands_high()
        get_city(message)
    elif command == '/bestdeal':
        bestdeal.change_params_commands_best()
        get_city(message)


def get_city(message) -> None:
    """Запрос города"""
    city_in = bot.send_message(message.from_user.id, 'Какой город интересует?', reply_markup=None)
    bot.register_next_step_handler(city_in, get_hotels)


def get_hotels(message) -> None:
    """Запрос количества отелей"""
    hotels_numbers = bot.send_message(message.from_user.id, 'Сколько отелей выбрать?', reply_markup=None)
    result[message.from_user.id] = [message.text.capitalize()]
    bot.register_next_step_handler(hotels_numbers, get_photos)


def get_photos(message) -> None:
    """Запрос необходимости вывода фото"""
    if message.text.isdigit() and int(message.text) < 10:
        result[message.from_user.id].append(message.text + ' hotels')
        photos = bot.send_message(message.from_user.id, 'Фото показать? ДА/нет', reply_markup=None)
        bot.register_next_step_handler(photos, get_numbers_photos)
    else:
        bot.send_message(message.from_user.id, 'Это не цифра...\nНачнём заново?!)))..Цифра не > 9', reply_markup=None)
        get_city(message)


def get_numbers_photos(message) -> None:
    """Запрос количества фото"""
    if message.text.lower() == 'да':
        photos_numbers = bot.send_message(message.from_user.id, 'Сколько фото показать?', reply_markup=None)
        bot.register_next_step_handler(photos_numbers, digit_to_5)
    else:
        out_res(message)


def digit_to_5(message) -> None:
    """ Проверка количества фото (не более 5)"""
    if int(message.text) > 5:
        digit = bot.send_message(message.from_user.id, ' не > 5...повторите ввод', reply_markup=None)
        bot.register_next_step_handler(digit, digit_to_5)
    else:
        out_res(message)


def out_res(message) -> None:
    """Поиск информации и вывод результата пользователю"""
    if message.text.isdigit() and int(message.text) <= 5:
        message.text = f'{message.text} фото'
    else:
        message.text = 'без фото'
    result[message.from_user.id].append(message.text)
    if result:
        bot.send_message(message.from_user.id, "Итак, ищем: ")
        bot.send_message(message.from_user.id, f'{result[message.from_user.id][0]},  '
                                               f'{result[message.from_user.id][1]},  '
                                               f'{result[message.from_user.id][2]} ')
        city = result[message.from_user.id][0].lower()
        number = int(result[message.from_user.id][1][:1])
        bot.send_message(message.from_user.id, "Поиск.... 10-15 сек")
        if result[message.from_user.id][2] == 'без фото':
            out_total = base_functions.get_city_hotels_photo(city, number)
        else:
            photos = int(result[message.from_user.id][2][:1])
            out_total = base_functions.get_city_hotels_photo(city, number, photos)

        for out_next in out_total.split(']')[:-1]:
            bot.send_message(message.from_user.id, f'{out_next}')
        write_history(
            db, History, [
                {'user_id': str(message.from_user.id), 'request': out_total}
            ])
        bot.send_message(message.from_user.id, "Хочешь ещё? Выбери и нажми кнопку!' ", reply_markup=None)
        get_commands(message)
    else:
        bot.send_message(message.from_user.id, "Мало информации!")


if __name__ == '__main__':

    bot = telebot.TeleBot(os.getenv('MY_TOKEN'))


    @bot.message_handler(content_types=['text'], reply_markup=None)
    def get_text_messages(message):
        if message.text.lower() == "привет":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('/lowprice')
            item2 = types.KeyboardButton('/bestdeal')
            item3 = types.KeyboardButton('/highprice')
            item4 = types.KeyboardButton('/history')
            markup.add(item1, item2, item3, item4)

            response = bot.send_message(message.from_user.id, 'Привет! Я бот,который ищет отели.\n'
                                                              ' Умею выполнять команды:\n  '
                                                              '/lowprice - дешёвые отели\n  '
                                                              '/highprice - дорогие отели\n  '
                                                              '/bestdeal - отели в центре города\n  '
                                                              '/history - история поиска\n'
                                                              'Bыбери что поискать и нажми кнопку:',
                                        reply_markup=markup)
            bot.register_next_step_handler(response, get_commands)

        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Если нужна помощь,напиши привет!", reply_markup=None)
        elif message.text in ['/lowprice', '/bestdeal', '/highprice', '/history']:
            get_commands(message)
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.", reply_markup=None)


    bot.polling(none_stop=True, interval=0)
