from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message

from keyboards import (
    economy_Rus,
    main_keyboard,
    main_admin_keyboard
)
from .admin import id_check_admin
from services.parcer import inflation, info_economy_rus

#################################

Economy_Router = Router()

#################################


@Economy_Router.message(F.text == "Экономика РФ")
async def main_menu_economy(message: Message) -> None:
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
    await message.answer(
        'Здесь Вы можете найти информацию '
        f'о состоянии <b>экономики РФ</b> на момент времени: {current_time} (По МСК)',
        reply_markup=economy_Rus,
        parse_mode="HTML"
    )


@Economy_Router.message(F.text == "Инфляция")
async def get_inflation(message: Message):
    data, next_meeting = inflation()

    if data == "error_status":
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

    await message.answer(
        f'Инфляция на момент времени {list(data['Инфляция'].keys())[1]} (ЦБ РФ)'
        f'равна - <u><b>{data["Инфляция"][list(data['Инфляция'].keys())[1]]}</b></u>',
        parse_mode='HTML'
    )
    await message.answer(
        'Цель по инфляции ЦБ РФ равна - '
        f'<u><b>{data["Инфляция"][list(data['Инфляция'].keys())[0]]}</b></u>',
        parse_mode='HTML'
    )
    await message.answer(
        'Значение ключевой ставки равно - '
        f'<u><b>{data['Ключевая ставка']}</b></u>',
        parse_mode='HTML'
    )
    await message.answer(
        f'{list(next_meeting.keys())[0]} - '
        f'<u><b>{next_meeting[list(next_meeting.keys())[0]]}</b></u>',
        parse_mode="HTML",
        reply_markup=economy_Rus
    )


@Economy_Router.message(F.text == "Безработица")
async def unemployment(message: Message):
    info_dict = info_economy_rus()

    if info_dict == 'error_status':
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

    keys_dict = list(info_dict.keys())

    await message.answer(
        f'{keys_dict[-2]} - <u><b>{info_dict[keys_dict[-2]][0] + info_dict[keys_dict[-2]][1]}</b></u>',
        parse_mode='HTML'
    )
    await message.answer(
        f'{keys_dict[0]} - равна '
        f'<u><b>{info_dict[keys_dict[0]][0] + " " + info_dict[keys_dict[0]][1]}</b></u>',
        parse_mode='HTML'
    )
    await message.answer(
        f'{keys_dict[-1]} равна - '
        f'<u><b>{info_dict[keys_dict[-1]][0] +' '+ info_dict[keys_dict[-1]][1]}</b></u>',
        parse_mode="HTML",
        reply_markup=economy_Rus
    )

@Economy_Router.message(F.text == "ВВП")
async def VVP(message: Message):
    info_dict = info_economy_rus()

    if info_dict == 'error_status':
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

    keys_dict = list(info_dict.keys())

    await message.answer(
        f"{keys_dict[1]} - <u><b>{info_dict[keys_dict[1]][0] +' '+ info_dict[keys_dict[1]][1]}</b></u>",
        parse_mode="HTML"
    )
    await message.answer(
        f"{keys_dict[2]} - <u><b>{info_dict[keys_dict[2]][0]+info_dict[keys_dict[2]][1]}</b></u>",
        parse_mode="HTML",
        reply_markup=economy_Rus
    )

@Economy_Router.message(F.text == "Индекс промышленного производства")
async def index_production(message: Message):
    info_dict = info_economy_rus()

    if info_dict == 'error_status':
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
    
    keys_dict = list(info_dict.keys())

    await message.answer(
        f"{keys_dict[3]} - <u><b>{info_dict[keys_dict[3]][0]+info_dict[keys_dict[3]][1]}</b></u>",
        parse_mode="HTML",
        reply_markup=economy_Rus
    )

@Economy_Router.message(F.text == "Индекс потребительских цен")
async def index_price(message: Message):
    info_dict = info_economy_rus()

    if info_dict == 'error_status':
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
    
    keys_dict = list(info_dict.keys())
    await message.answer(
        f"{keys_dict[4]} - <u><b>{info_dict[keys_dict[4]][0]+info_dict[keys_dict[4]][1]}</b></u>",
        parse_mode="HTML",
        reply_markup=economy_Rus,
    )
