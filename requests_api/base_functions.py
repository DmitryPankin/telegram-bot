from typing import List, Dict
import requests
import requests_api.params_requests
from .params_requests import headers_1, headers_2, payload_1, payload_2


def result_hotel_price_sort(hotels: Dict, prices: Dict) -> List:
    """
    Функция сортирует отели по цене
    :param hotels: словарь найденных отелей
    :param prices: отсортированный словарь цен
    :return: отсортированный список отелей по цене
    """
    result_out = []
    for price in prices:
        result_out.append({price: hotels[price]})
    return result_out


def out_from_user(prices: Dict, hotels: Dict, photos: Dict, number_hotels: int,
                  number_photos: int, address: Dict, distance: Dict) -> str:
    """
    Функция выводит результат запроса пользователя
    :param prices: полученный из API отсортированный словарь цен
    :param hotels: полученный из API словарь отелей
    :param photos: полученный из API словарь фото
    :param number_hotels: количество отелей для вывода
    :param number_photos: количество фото для вывода
    :param address: полученный из API словарь адресов
    :param distance: полученный из API словарь расстояний до центра города
    :return: текстовый результат запроса
    """
    out = ''
    result = result_hotel_price_sort(hotels, prices)
    if len(result) > number_hotels:
        result = result[:number_hotels]
    for element in result:
        for key, value in element.items():
            if hotels:
                out += f'**{value},\n адрес: {address[key]}\n' \
                       f' {distance[key]} км до центра\n {photos[key][:number_photos]}\n'
            else:
                out += f'**{value},\n адрес не найден\n {photos[key][:number_photos]}\n'
    return out


def get_city_hotels_photo(city_in: str, number_in: int, photos_in=0) -> str:
    """
    Функция производящая запросы к API
    :param city_in: запрашиваемый город
    :param number_in: запрашиваемое количество отелей
    :param photos_in: количество фото для вывода
    :return: текстовый результат запроса
    """
    result = {}
    result_price = {}
    result_address = {}
    result_photos = {}
    result_distance = {}
    url_city = "https://hotels4.p.rapidapi.com/locations/v3/search"
    url_hotels = "https://hotels4.p.rapidapi.com/properties/v2/list"
    url_photos = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    querystring_1 = {"q": str(city_in), "locale": "ru_RU"}

    response_city = requests.request("GET", url_city, headers=headers_1, params=querystring_1, timeout=15)
    res_city = response_city.json()
    if 'gaiaId' not in res_city['sr'][0]:
        return f'Ошибка запроса...\n ' \
               f'Похоже, такого города не существует...\n ' \
               f'Попробуйте ещё раз!'

    region_id = res_city['sr'][0]['gaiaId']
    payload_1['destination']['regionId'] = region_id

    response_hotels = requests.request("POST", url_hotels, json=payload_1, headers=headers_2, timeout=30)
    res_hotels = response_hotels.json()
    if 'errors' in res_hotels:
        return f'Похоже, по городу нет данных...\n ' \
               f'Попробуйте ещё раз!'

    for number in res_hotels['data']['propertySearch']['properties']:
        result[number['id']] = number['name'] + '**\n цена: ' + number['price']['lead']['formatted'] + ' за ночь'
        result_price[number['id']] = int(number['price']['lead']['formatted'][1:])
        payload_2['propertyId'] = number['id']
        response_photo = requests.request("POST", url_photos, headers=headers_2, json=payload_2, timeout=30)
        res_photo = response_photo.json()
        result_photos[number['id']] = []
        result_distance[number['id']] = round(number['destinationInfo']['distanceFromDestination']['value'] * 1.61, 2)

        for number_image in res_photo['data']['propertyInfo']['propertyGallery']['images']:
            result_photos[number['id']].append(number_image['image']['url'])
            result_address[number['id']] = \
                res_photo['data']['propertyInfo']['summary']['location']['address']['addressLine']

    command = requests_api.params_requests.command
    if command == 'lowprice':
        result_price = dict(sorted(result_price.items(), key=lambda item: item[1]))

    elif command == 'highprice':
        result_price = dict(sorted(result_price.items(), key=lambda item: item[1], reverse=True))

    if result:
        result_out = out_from_user(result_price, result, result_photos, number_in, photos_in,
                                   result_address, result_distance)
    else:
        return f'Ничего не найдено('
    return result_out
