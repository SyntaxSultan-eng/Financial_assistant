from aiogram import types, Router,F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import LinkPreviewOptions

import app.keyboard as keyboards
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
        reply_markup=keyboards.main_keyboard
    )
@router.message(Command('currency'))
@router.message(F.text == 'Курс валют(ЦБ РФ)🏛️')
async def currency(message: types.Message):
    await message.answer("Выберите режим.", reply_markup=keyboards.setting_currency)

@router.message(Command('cancel'))
async def choose_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Нечего отменять💀", reply_markup=keyboards.main_keyboard)
        return
    
    await state.clear()
    await message.answer("Действие отменено⛔",reply_markup=keyboards.main_keyboard)

################# Курс валют(ЦБ РФ)🏛️############################

################### Конкретная валюта ###########################
@router.callback_query(F.data == 'True_info')
async def correction(callback: types.CallbackQuery, state: FSMContext):
    options_1 = LinkPreviewOptions(is_disabled=True)
    user_data = await state.get_data()

    #Блок кода, чтобы избежать проблему с командой cancel
    if len(user_data) == 0:
        await callback.message.delete()
        return

    await callback.message.delete()
    await callback.message.answer("Хммм... Значит ошибка в программной части. Напишите дебилу-разработчику @Senior_kartofan о вашей проблеме.🛠️")
    await callback.message.answer(f"Вот информация о вашей валюте в браузере: https://yandex.ru/search/?text={user_data['need_currency']}",
    reply_markup=keyboards.main_keyboard, link_preview_options=options_1)

    await state.clear()

@router.callback_query(F.data == 'False_info')
async def testing(callback: types.CallbackQuery, state:FSMContext):
    user_data = await state.get_data()

    #Блок кода, чтобы избежать проблему с командой cancel
    if len(user_data) == 0:
        await callback.message.delete()
        return
    
    await callback.message.delete()
    await callback.message.answer("Решили проверить работоспособность бота.🤓☝️ Похвально!",reply_markup=keyboards.main_keyboard)

    await state.clear()

@router.callback_query(F.data == 'Right_info')
async def good_end(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    #Блок кода, чтобы избежать проблему с командой cancel
    if len(user_data) == 0:
        await callback.message.delete()
        return
    
    await callback.message.delete()
    await callback.message.answer("Отлично!😎", reply_markup=keyboards.main_keyboard)

    await state.clear()

@router.callback_query(F.data == 'Lie_info')
async def bad_end(callback: types.CallbackQuery, state: FSMContext):
    options_1 = LinkPreviewOptions(is_disabled=True)
    user_data = await state.get_data()

    #Блок кода, чтобы избежать проблему с командой cancel
    if len(user_data) == 0:
        await callback.message.delete()
        return

    await callback.message.delete()
    await callback.message.answer(f"😎Тогда вот информация о вашей валюте в браузере: https://yandex.ru/search/?text={user_data['need_currency']}",
    reply_markup=keyboards.main_keyboard, link_preview_options=options_1)

    await state.clear()

@router.callback_query(F.data == 'need_currency')
async def find_currency(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Введите интересующую валюту.\n\n"\
    "Правило ввода: 1)❗ЖЕЛАТЕЛЬНО❗ вводить осознанно.\n\n"\
    "2)Пример правильного ввода👍: Австралийский доллар\n\n"\
    "Попробуйте!🔎")
    await state.set_state(Form.need_currency)

@router.message(Form.need_currency)
async def print_currency(message: types.Message, state: FSMContext):

    await state.update_data(need_currency=message.text)
    value = parc.get_currency(f"https://yandex.ru/search/?text=курс+{message.text}+к+рублю")

    if value == 'error':
        await message.answer("Что-то пошло не так.😱 Проверьте, Вы точно осознанно написали необходимую валюту?",reply_markup=keyboards.checkingNONE_inline_kb)
    else:
        await message.answer(value)
        await message.answer("Результат соответствует ожиданиям?",reply_markup=keyboards.checking_inline_kb)

#############################################

############## Мировые Валюты################# 

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
        reply_markup=keyboards.main_keyboard)

#################################################################
