from aiogram import types, Router,F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.keyboard import main_keyboard,setting_currency
import app.parcer as parc


#############################################

router = Router()

class Form(StatesGroup):
    need_currency = State()


#############################################

@router.message(Command('start'))
async def start_menu(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.first_name}!\n'
        f'Этот бот должен упростить мониторинг финансовых изменений на рынке валют.\nОриентируйтесь по кнопкам!',
        reply_markup=main_keyboard
    )

@router.message(F.text == 'Курс валют(ЦБ РФ)🏛️')
async def currency(message: types.Message):
    await message.answer("Выберите режим.", reply_markup=setting_currency)

#############################################

@router.callback_query(F.data == 'need_currency')
async def find_currency(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Введите интересующую валюту.\n\n"\
    "Правило ввода: 1)❗ЖЕЛАТЕЛЬНО❗ вводить осознанно.\n\n"\
    "2)Пример правильного ввода👍: Австралийский доллар\n\n"\
    "Попробуйте это просто!")
    await state.set_state(Form.need_currency)

@router.message(Form.need_currency)
async def print_currency(message: types.Message, state: FSMContext):

    await message.answer(parc.get_currency(f"https://yandex.ru/search/?text=курс+{message.text}+к+рублю"),reply_markup=main_keyboard)
    await state.clear()

#############################################

@router.callback_query(F.data == "world_currency")
async def world_currency(callback: types.CallbackQuery):
    await callback.message.delete()
    info_world_currency = parc.get_all_currency()
    for item in info_world_currency:
        '''
        структура info_world_currency
        [['840', 'USD', '1', 'Доллар США', '87,9595'],...]
        '''
        сurrency_codename = item[1]
        currency_nums = item[2]
        currency_name = item[3]
        currency_value = item[4]
        

        await callback.message.answer(f"💵{currency_nums} {сurrency_codename} ({currency_name}) - {currency_value}₽",
        reply_markup=main_keyboard)


