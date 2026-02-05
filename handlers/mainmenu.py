from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart


from keyboards import *
from config import config


###################################

Mainmenu_Router = Router()


async def id_check_admin(message: Message, user_id: int, text: str) -> None:
    if config.bot.admin_id == user_id:
        await message.answer(
            text,
            reply_markup=main_admin_keyboard
        )

###################################

@Mainmenu_Router.message(CommandStart())
async def start_message(message: Message) -> None:
    """ Обработка команды /start"""
    await message.answer(
        f'Здравствуйте, <b>{message.from_user.first_name}</b>!\n'
        'Этот бот должен упростить мониторинг финансовых изменений на рынке валют и не только.\n'
        'Ориентируйтесь по кнопкам!',
        reply_markup=main_keyboard,
        parse_mode='HTML'
    )
    await id_check_admin(
        message=message,
        user_id=message.from_user.id,
        text='Вы вошли как администратор👑'
    )

@Mainmenu_Router.message(F.text == 'Информация📜')
async def get_information(message: Message):
    await message.answer(
        'Этот бот небольшой пет-проект. ' 
        'Хотелось сделать помощника по финансовому рынку и не только.\n\n'
        'github разработчика - <u>https://github.com/SyntaxSultan-eng</u> '
        '(Пока там ничего нет, но вдруг что-то изменится)', 
        reply_markup=Information_kb, 
        parse_mode='HTML',
    )

@Mainmenu_Router.message()
async def unkown_text(message: Message):
    await message.answer(
        'Неизвестная команда! Используйте кнопки.',
        reply_markup=main_keyboard
    )
    await id_check_admin(
        message=message,
        user_id=message.from_user.id,
        text='Вы вошли как администратор👑'
    )