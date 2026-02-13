from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import date

from keyboards import (
    main_admin_keyboard,
    main_keyboard,
    currency_keyboard
)
from .admin import id_check_admin
from services import CBRClient

#################################

Currency_Router = Router()

class Need_Currency(StatesGroup):
    user_input = State()

#################################

@Currency_Router.message(Command('currency'))
@Currency_Router.message(F.text == 'Курс валют(ЦБ РФ)🏛️')
async def currency_menu(message: Message) -> None:
    await message.answer(
        'Меню для изучения котировок валют.\n'
        '<b>Выберете команду.</b>',
        reply_markup=currency_keyboard,
        parse_mode="HTML"
    )

@Currency_Router.message(F.text == 'Основные валюты🚀')
async def world_currency(message: Message) -> None:
    async with CBRClient() as client:
        info_world_currency = await client.get_popular_currency()
        
    if info_world_currency is None:
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
            parse_mode="HTML"
        )
    await message.answer(
        'Курс основных валют по ЦБ РФ на дату: '
        f'<u>{date.today().strftime('%d.%m.%Y')}</u>',
        reply_markup=currency_keyboard,
        parse_mode="HTML"
    )

@Currency_Router.message(F.text == 'Поиск валюты 🔍')
async def search_currency(message: Message, state: FSMContext):
    await message.answer(
        'Введите валюту, которая Вас интересует.\n\n'
        'Можно указать:\n'
        '<i>Полное название</i>\n'
        '<i>Тикер валюты</i>\n'
        '<i>Номер</i>\n'
        '<u><b>Ввод не чувствителен к регистру</b></u>.',
        parse_mode="HTML"
    )
    await state.set_state(Need_Currency.user_input)

@Currency_Router.message(Need_Currency.user_input)
async def get_find_currency(message: Message, state: FSMContext):
    await state.update_data(user_input=message.text)
    async with CBRClient() as client:
        information = await client.find_currency(message.text)

    if information is None:
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
        await state.clear()
        return
    
    if len(information) == 0:
        await message.answer(
            'Не найдена информация по данной валюте.\n\n'
            '<b>Проверьте ВВОД!</b>',
            parse_mode='HTML',
            reply_markup=currency_keyboard
        )
        await state.clear()
        return
    
    сurrency_codename = information[1].upper()
    currency_nums = information[2]
    currency_name = information[3].capitalize()
    currency_value = information[4]
    
    await message.answer(
        f'💵{currency_nums} {сurrency_codename} '
        f'(<b>{currency_name}</b>) — <u><b>{currency_value}₽</b></u>',
        parse_mode="HTML"
    )
    await message.answer(
        f'Курс {currency_name} по ЦБ РФ на дату: '
        f'<u>{date.today().strftime('%d.%m.%Y')}</u>',
        reply_markup=currency_keyboard,
        parse_mode="HTML"
    )
    await state.clear()

    
