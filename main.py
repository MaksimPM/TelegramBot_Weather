import datetime
import os

import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\n'
        'Напиши любой город, чтобы узнать погоду на текущий день'
    )


@dp.message()
async def get_weather(message: Message):
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}'
            f'&appid={os.getenv("open_weather_token")}&units=metric')
        data = r.json()

        city = data["name"]
        temp_weather = round(data["main"]["temp"])
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - \
                            datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        await message.answer(f'Погода в городе {city}:\n'
                             f'-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'
                             f'Температура: {temp_weather}°C\n'
                             f'-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'
                             f'Влажность: {humidity}%\n'
                             f'-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'
                             f'Давление: {pressure} мм.рт.ст\n'
                             f'-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'
                             f'Скорость ветра: {wind} м/с\n'
                             f'-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'
                             f'Восход солнца: {sunrise_timestamp}\n'
                             f'Закат солнца: {sunset_timestamp}\n'
                             f'-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'
                             f'Продолжительность дня: {length_of_the_day}'
                             f'_________________________________________')

    except Exception as ex:
        await message.answer('Неверное название города')


if __name__ == '__main__':
    dp.run_polling(bot)
