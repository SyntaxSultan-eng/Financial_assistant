from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart


from keyboards import (
    main_keyboard,
    Information_kb
)
from .admin import id_check_admin


###################################

Mainmenu_Router = Router()

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
async def get_information(message: Message) -> None:
    await message.answer(
        'Пока тут пусто.',
        reply_markup=Information_kb,
    )


@Mainmenu_Router.message(Command('menu'))
@Mainmenu_Router.message(F.text == 'Главное меню↩')
async def back_to_main(message: Message) -> None:
    await message.answer(
        'Возвращаю Вас на главное меню👨🏻‍💻',
        reply_markup=main_keyboard
    )
    await id_check_admin(
        message=message,
        user_id=message.from_user.id,
        text='Вы вошли как администратор👑'
    )


@Mainmenu_Router.message()
async def unkown_text(message: Message) -> None:
    await message.answer(
        'Неизвестная команда! Используйте кнопки.',
        reply_markup=main_keyboard
    )
    await id_check_admin(
        message=message,
        user_id=message.from_user.id,
        text='Вы вошли как администратор👑'
    )
