from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import stocks_keyboard

####################################

Stocks_Router = Router()

####################################

@Stocks_Router.message(Command('stocks'))
@Stocks_Router.message(F.text == 'Рынок акций🌐')
async def Market_stocks(message: Message):
    await message.answer(
        'Что вы хотите узнать из мира инвестиций?✍',
        reply_markup=stocks_keyboard
    )