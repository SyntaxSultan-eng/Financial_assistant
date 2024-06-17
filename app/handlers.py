from aiogram import types, Router
from aiogram.filters import Command

#############################################

router = Router()

#############################################

@router.message(Command('start'))
async def start_menu(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.first_name}!\nЭтот бот должен упростить мониторинг финансовых изменений на рынке валют.\n Ориентируйтесь по кнопкам!')