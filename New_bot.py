import asyncio
from aiogram import Bot, Dispatcher,types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters.command import Command

from decouple import config
import requests
from bs4 import BeautifulSoup

############################################

API_TOKEN = config('API_KEY',default = '')
bot = Bot(API_TOKEN)
dp = Dispatcher()

############################################

async def on_startup():
    print("Bot has started working🚀", end = '\n\n')


@dp.message(Command('start'))
async def start_menu(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.first_name}!\nЭтот бот должен упростить мониторинг финансовых изменений на рынке валют.\n Ориентируйтесь по кнопкам!')


############################################

async def main() -> None:
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot has stopped working❌')