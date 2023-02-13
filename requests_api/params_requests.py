from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

dates = str(date.today()).split('-')

filters = {
    'sort_price': {"price": {
        "max": 500,
        "min": 10
    }}}

params_sort = ['PRICE_LOW_TO_HIGH ', 'DISTANCE']
commands = ['highprice', 'bestdeal', 'lowprice']
command = ''

headers_1 = {
    "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
    "X-RapidAPI-Host": os.getenv('RAPIDAPI_HOST')
}
headers_2 = headers_1
headers_2["content-type"] = "application/json"

payload_1 = {
    "currency": "USD",
    "eapid": 1,
    "locale": "ru_RU",
    "destination": {"regionId": ''},
    "checkInDate": {
        "day": int(dates[2]),
        "month": int(dates[1]),
        "year": int(dates[0])
    },
    "checkOutDate": {
        "day": int(dates[2]),
        "month": int(dates[1]),
        "year": int(dates[0])
    },
    "rooms": [
        {
            "adults": 1
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 10,
    "sort": "",
}
payload_2 = {
    "currency": "USD",
    "eapid": 1,
    "locale": "ru_Ru",
    "propertyId": ''
}

