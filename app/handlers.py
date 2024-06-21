from aiogram import types, Router,F
from aiogram.filters import Command
from app.keyboard import main_keyboard,setting_currency
import app.parcer as parc


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
    await message.answer("Выберите режим.", reply_markup=setting_currency)

@router.callback_query(F.data == 'need_currency')
async def find_currency(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(parc.get_currency('https://yandex.ru/search/?text=доллар'),reply_markup=main_keyboard)

@router.callback_query(F.data == "world_currency")
async def world_currency(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Цифр.код\nБукв.код\nЕдиниц\nВалюта\nКурс')
    info_world_currency = parc.get_all_currency()
    for item in info_world_currency:
        '''
        структура info_world_currency
        [['840', 'USD', '1', 'Доллар США', '87,9595'],...]
        '''
        currency_code = item[0] 
        сurrency_codename = item[1]
        currency_nums = item[2]
        currency_name = item[3]
        currency_value = item[4]
        

        await callback.message.answer(f"💵({currency_code}) {currency_nums} {сurrency_codename} ({currency_name}) - {currency_value}₽")


