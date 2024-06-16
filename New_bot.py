import asyncio
from aiogram import Bot, Dispatcher,types
from decouple import config
import requests
from bs4 import BeautifulSoup

############################################

API_TOKEN = config('API_KEY',default = '')
bot = Bot(API_TOKEN)
dp = Dispatcher()

############################################

@dp.message()
async def echo(message: types.Message):
    await message.answer(text=message.text)


############################################

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())