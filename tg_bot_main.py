from aiogram import executor, types

from create_bot import dp
from handlers import cat_memes, currency, polls_creator, weather

# Создаем клавиатуру с кнопками
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton('Погода')
btn2 = types.KeyboardButton('Курсы валют')
btn3 = types.KeyboardButton('Мемы с котами')
btn4 = types.KeyboardButton('Создать опрос')
keyboard.add(btn1, btn2, btn3, btn4)


# Обрабатываем приветствие через хэндлер /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет! Я бот, который может помочь тебе узнать курсы валют, погоду, отправить'
                        ' мемы с котами или создать опрос. Выбери нужный пункт из меню ниже:', reply_markup=keyboard)

# Создаем хэндлеры для команд клавиатуры и обработки погоды
dp.register_message_handler(currency.process_exchange_command, lambda message: message.text == 'Курсы валют')
dp.register_message_handler(cat_memes.send_cat_mem, lambda message: message.text == 'Мемы с котами')
dp.register_message_handler(weather.start_weather, lambda message: message.text == 'Погода')
dp.register_message_handler(polls_creator.create_poll_handler, lambda message: message.text == 'Создать опрос')
dp.register_message_handler(weather.get_weather)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
