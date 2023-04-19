import requests
from aiogram import types

from config import EXCHANGERATE_TOKEN
from create_bot import dp


# Получаем курсы из API
def get_exchange_rate(from_currency, to_currency):
    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGERATE_TOKEN}/latest/{from_currency}'
    response = requests.get(url)
    data = response.json()
    exchange_rate = data['conversion_rates'][to_currency]
    return exchange_rate


@dp.message_handler(commands=['exchange'])
async def process_exchange_command(message: types.Message):
    try:
        # Получаем валюты из команды
        currencies = message.get_args().upper().split()

        # Проверяем наличие двух валют
        if len(currencies) != 2:
            raise ValueError

        # Получаем значения валют
        from_currency, to_currency = currencies

        # Получаем курс валют
        exchange_rate = get_exchange_rate(from_currency, to_currency)

        # Отправляем результат пользователю
        await message.reply(f"1 {from_currency} = {exchange_rate} {to_currency}")
    except:
        # Обрабатываем возможные ошибки и информируем о вводе
        await message.reply('Для получения курса введите: /exchange FROM_CURRENCY TO_CURRENCY '
                            '(Например /exchange USD EUR)')
