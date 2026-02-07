from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import (
    main_admin_keyboard,
    main_keyboard
)
from .admin import id_check_admin
import services.parcer as parc

#################################

Currency_Router = Router()

#################################

@Currency_Router.message(Command('currency'))
@Currency_Router.message(F.text == 'Курс валют(ЦБ РФ)🏛️')
async def world_currency(message: Message) -> None:
    info_world_currency = parc.get_all_currency()
    if info_world_currency == 'error_status':
        await message.answer(
            'Извините, но данная функция на ремонте🔧',
            reply_markup=main_keyboard
        )
        await id_check_admin(
            message=message,
            user_id=message.from_user.id,
            text='Необходим ремонт🛠️',
            keyboard_name=main_admin_keyboard
        )
        return
    
    #Отправка курса валют
    for item in info_world_currency:
        # ['840', 'USD', '1', 'Доллар США', '87,9595']
        сurrency_codename = item[1]
        currency_nums = item[2]
        currency_name = item[3]
        currency_value = item[4]
        
        await message.answer(
            f'💵{currency_nums} {сurrency_codename} '
            f'(<b>{currency_name}</b>) — <u><b>{currency_value}₽</b></u>',
            reply_markup=main_keyboard,parse_mode="HTML"
        )
    await id_check_admin(
        message=message,
        user_id=message.from_user.id,
        text='Вы вошли как администратор👑',
        keyboard_name=main_admin_keyboard
    )