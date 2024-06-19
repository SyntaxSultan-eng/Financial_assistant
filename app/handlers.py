from aiogram import types, Router,F
from aiogram.filters import Command
from app.keyboard import main_keyboard

#############################################

router = Router()

#############################################

@router.message(Command('start'))
async def start_menu(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.first_name}!\n'
        f'Этот бот должен упростить мониторинг финансовых изменений на рынке валют.\nОриентируйтесь по кнопкам!',
        reply_markup=main_keyboard
    )

@router.message(F.text == 'Курс валют(ЦБ РФ)🏛️')
async def currency(message: types.Message):
    pass