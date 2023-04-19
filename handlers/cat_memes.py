import requests
from aiogram import types

from create_bot import bot


# Получаем картинку котиков из API
async def send_cat_mem(message: types.Message):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    cat_url = response.json()[0]['url']
    await bot.send_photo(chat_id=message.chat.id, photo=cat_url)
