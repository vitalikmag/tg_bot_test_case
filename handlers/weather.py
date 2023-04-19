import datetime

import requests
from aiogram import types

from config import OPEN_WEATHER_TOKEN


# Обработка приветствия и запрос города
async def start_weather(message: types.Message):
    await message.reply('Привет! В каком городе смотрим погоду?')


# Получаем погоду в городе
async def get_weather(message: types.Message):
    # Далаем словарь эмодзи для вывода
    code_to_icons = {
        'Clear': 'Ясно \U00002600',
        'Rain': 'Дождь \U00002614',
        'Clouds': 'Облачно \U00002601',
        'Drizzle': 'Дождь \U00002614',
        'Snow': 'Снег \U00002744',
        'Mist': 'Туман \U0001F32B',
        'Thunderstorm': 'Гроза \U0001F329',
    }
    # Получаем данные погоды
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={OPEN_WEATHER_TOKEN}&units=metric'
        )
        data = r.json()

        city = data['name']
        description = data['weather'][0]['main']

        # Условие на вывод эмодзи
        if description in code_to_icons:
            wd = code_to_icons[description]
        else:
            wd = 'Непонятно, посмотрите в окно!'

        # Выбираем нужные нам данные
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        feels_like = data['main']['feels_like']
        sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        # Выводим отформатированные данные
        await message.reply(f'*** {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")} ***\n'
                            f'Погода в городе: {city}\n'
                            f'{wd}\n'
                            f'Температура: {temp} °C\n'
                            f'Влажность: {humidity} %\n'
                            f'Ветер: {wind} м/c\n'
                            f'Ощущается как: {feels_like} °C\n'
                            f'Время рассвета: {sunrise_time.strftime("%d-%m-%Y %H:%M")}\n'
                            f'Время заката: {sunset_time.strftime("%d-%m-%Y %H:%M")}\n'
                            f'Продолжительность дня: {length_day}\n'
                            )
    # Обрабатываем некорректный ввод
    except:
        await message.reply('Проверьте название города!')
