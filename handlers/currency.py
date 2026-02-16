from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import date, datetime

from keyboards import (
    main_admin_keyboard,
    main_keyboard,
    currency_keyboard,
    show_all_currency,
    select_date
)
from .admin import id_check_admin
from services import CBRClient
from config import config

#################################

Currency_Router = Router()

class Need_Currency(StatesGroup):
    user_input = State()
    user_date = State()

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

#################################

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

#################################

@Currency_Router.message(F.text == 'Поиск валюты 🔍')
async def search_currency(message: Message):
    await message.answer(
        'Введите валюту, которая Вас интересует.\n\n'
        'Можно указать:\n'
        '<i>Полное название</i>\n'
        '<i>Тикер валюты</i>\n'
        '<i>Номер</i>\n'
        '<u><b>Ввод не чувствителен к регистру</b></u>.'
        'Также возможно выбрать курс валюты на заданную дату.\n'
        f'Крайняя дата: 01.07.1992 - {date.today().strftime('%d.%m.%Y')}\n',
        parse_mode="HTML"
    )
    await message.answer(
        'На какую дату вывести информацию.\n'
        '↓↓↓',
        reply_markup=select_date
    )


@Currency_Router.callback_query(F.data == 'today')
async def today_date(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        'Можете вывести данные о всех валютах в pdf файле '
        '(Название, тикер, код)',
        reply_markup=show_all_currency
    )

@Currency_Router.callback_query(F.data == 'another_date')
async def get_another_date(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        'Введите дату. Правильный формат (день.месяц.год)\n'
        'Пример: 02.07.2022'
    )
    await state.set_state(Need_Currency.user_date)

@Currency_Router.message(Need_Currency.user_date)
async def set_user_date(message: Message, state: FSMContext):
    try:
        right_format = datetime.strptime(message.text,'%d.%m.%Y').strftime("%d/%m/%Y")
        await state.update_data(user_date=right_format)

        await message.answer(
            'Можете вывести данные о всех валютах в pdf файле '
            '(Название, тикер, код)',
            reply_markup=show_all_currency
        )

    except Exception:
        await state.clear()
        await message.answer(
            '<b>Дата в неправильном формате.</b>',
            parse_mode="HTML",
            reply_markup=currency_keyboard
        )

@Currency_Router.callback_query(F.data == 'get_all_currency')
async def get_pdf_currency(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    file_path = config.cbr.pdf_file_url
    pdf_file = FSInputFile(file_path)

    await callback.message.answer_document(
        document=pdf_file,
        caption="Валюта (ЦБ РФ)"
    )
    
    await callback.message.answer(
        "Вы можете продолжить ввод названия.↓"
    )
    await state.set_state(Need_Currency.user_input)


@Currency_Router.callback_query(F.data == 'skip')
async def skip_all_currency(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "Вы можете продолжить ввод названия.↓"
    )
    await state.set_state(Need_Currency.user_input)

@Currency_Router.message(Need_Currency.user_input)
async def get_find_currency(message: Message, state: FSMContext):
    await state.update_data(user_input=message.text)
    data = await state.get_data()
    user_date = data['user_date'] if 'user_date' in data else date.today().strftime("%d/%m/%Y")

    async with CBRClient() as client:
        information = await client.find_currency(
            message.text,
            user_date
        )

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
    
    сurrency_codename = information[1]
    currency_nums = information[2]
    currency_name = information[3]
    currency_value = information[4]
    
    await message.answer(
        f'💵{currency_nums} {сurrency_codename} '
        f'(<b>{currency_name}</b>) — <u><b>{currency_value}₽</b></u>',
        parse_mode="HTML"
    )
    await message.answer(
        f'Курс {currency_name} по ЦБ РФ на дату: '
        f'<u>{user_date}</u>',
        reply_markup=currency_keyboard,
        parse_mode="HTML"
    )
    await state.clear()

#################################   
