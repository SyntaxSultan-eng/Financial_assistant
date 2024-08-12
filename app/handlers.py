from aiogram import types, Router,F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import LinkPreviewOptions

import app.keyboard as keyboards
import app.parcer as parc
import datetime

#############################################

router = Router()

class Form(StatesGroup):
    need_currency = State()


##################### Главные команды ########################

@router.message(Command('start'))
async def start_menu(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.first_name}!\n'
        f'Этот бот должен упростить мониторинг финансовых изменений на рынке валют.\nОриентируйтесь по кнопкам!',
        reply_markup=keyboards.main_keyboard
    )

@router.message(Command("stocks"))
@router.message(F.text == 'Рынок акций🌐')
async def Market_stocks(message: types.Message):
    await message.answer("Что вы хотите узнать из мира инвестиций?✍",reply_markup=keyboards.stocks_keyboard)

@router.message(Command("menu"))
@router.message(F.text == "Главное меню↩")
async def return_menu(message: types.Message):
    await message.answer("Возвращаю Вас на главное меню👨🏻‍💻", reply_markup=keyboards.main_keyboard)

@router.message(Command('cancel'))
async def choose_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Нечего отменять💀", reply_markup=keyboards.main_keyboard)
        return
    
    await state.clear()
    await message.answer("Действие отменено⛔",reply_markup=keyboards.main_keyboard)

################# Курс валют(ЦБ РФ)🏛️############################

############## Мировые Валюты################# 

@router.message(Command('currency'))
@router.message(F.text == 'Курс валют(ЦБ РФ)🏛️')
async def world_currency(message: types.Message):
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
        

        await message.answer(f"💵{currency_nums} {сurrency_codename} (<b>{currency_name}</b>) — <u><b>{currency_value}₽</b></u>",
        reply_markup=keyboards.main_keyboard,parse_mode="HTML")


#################################################################

################# Рынок акций🌐 ################################

@router.message(F.text == "Взлеты дня💹")
async def give_up_stocks(message: types.Message):
    info_stocks = parc.growth_stocks()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    for stock in info_stocks:
        Code_name = stock[0][:4]
        Full_name = stock[0][4:]
        Change_percent = stock[1]
        Price = stock[2]
        Subject = stock[10]
        await message.answer(f'(<b>{Code_name}</b>) {Full_name} ({Subject}) -> \n\n'
        f'Изменения за день на <u><b>{Change_percent}</b></u>↗ -> \n\n<u>Текущая цена <b>{Price}</b></u>', parse_mode="HTML")

    await message.answer(f"😎Вот первые <u><b>10</b></u> позиций в лидерах роста на момент времени {current_time}",reply_markup=keyboards.stocks_keyboard,parse_mode="HTML")

@router.message(F.text == 'Падения дня📉')
async def give_down_stocks(message: types.Message):
    inf_stock = parc.drop_stocks()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    for stock in inf_stock:
        Code_name = stock[0][:4]
        Full_name = stock[0][4:]
        Change_percent = stock[1]
        Price = stock[2]
        Subject = stock[10]
        await message.answer(f'(<b>{Code_name}</b>) {Full_name} ({Subject}) -> \n\n'
        f'Изменения за день на <u><b>{Change_percent}</b></u>⬇ -> \n\n<u>Текущая цена <b>{Price}</b></u>', parse_mode="HTML")

    await message.answer(f"😒Вот первые <u><b>10</b></u> позиций в лидерах падения〽 на момент времени {current_time}",reply_markup=keyboards.stocks_keyboard,parse_mode="HTML")


################## Сырье ########################################

@router.message(F.text == "Рынок Сырья⛏️")
async def menu_material(message: types.Message):
    await message.answer("Какой сектор экономики Вас интересует? Данные основаны на <u><b>Фьючерсных контрактах</b></u>", 
        reply_markup=keyboards.material_keyboard, parse_mode="HTML")

@router.message(F.text =="Энергетика⚡")
async def get_energy(message: types.Message):
    energy_data = parc.energy()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    for info_list in energy_data:
        name = info_list[0]
        price,change_day,percent = info_list[1]

        await message.answer(f"Цена на <u>{name.capitalize()}</u> за день <u>изменилась</u> на <b>{change_day}$</b> (<u><b>{percent}</b></u>)."
            f"->\n\nТекущая цена - <u><b>{price}$</b></u>", parse_mode="HTML")
    await message.answer(f"Вот <u><b>6</b></u> позиций цен на сырьё в <u>сфере энергетики</u> на момент времени {current_time}.\n\nВсе цены представлены в долларах$$$",
        reply_markup=keyboards.material_keyboard,parse_mode="HTML")

@router.message(F.text == "Металлы🔩")
async def get_metall(message: types.Message):
    metall_data = parc.metall()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    for info_list in metall_data:
        name = info_list[0]
        price,change_day,percent = info_list[1]

        await message.answer(f"Цена на <u>{name.capitalize()}</u> за день <u>изменилась</u> на <b>{change_day}$</b> (<u><b>{percent}</b></u>)."
            f"->\n\nТекущая цена - <u><b>{price}$</b></u>", parse_mode="HTML")
    await message.answer(f"Вот <u><b>5</b></u> позиций цен на сырьё в <u>сфере металлов</u> на момент времени {current_time}.\n\nВсе цены представлены в долларах$$$",
        reply_markup=keyboards.material_keyboard,parse_mode="HTML")

@router.message(F.text == "Сельское хоз. 🌱")
async def get_agriculture(message: types.Message):
    agriculture_data = parc.agriculture()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    for info_list in agriculture_data:
        name = info_list[0]
        price,change_day,percent = info_list[1]

        await message.answer(f"Цена на <u>{name.capitalize()}</u> за день <u>изменилась</u> на <b>{change_day}$</b> (<u><b>{percent}</b></u>)."
            f"->\n\nТекущая цена - <u><b>{price}$</b></u>", parse_mode="HTML")
    await message.answer(f"Вот <u><b>6</b></u> позиций цен на сырьё в <u>сфере сельского хозяйства</u> на момент времени {current_time}.\n\nВсе цены представлены в долларах$$$",
        reply_markup=keyboards.material_keyboard,parse_mode="HTML")

@router.message(F.text == "Промышленность⚙️")
async def get_industry(message: types.Message):
    industry_data = parc.industry()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    for info_list in industry_data:
        name = info_list[0]
        price,change_day,percent = info_list[1]

        await message.answer(f"Цена на <u>{name.capitalize()}</u> за день <u>изменилась</u> на <b>{change_day}$</b> (<u><b>{percent}</b></u>)."
            f"->\n\nТекущая цена - <u><b>{price}$</b></u>", parse_mode="HTML")
    await message.answer(f"Вот <u><b>6</b></u> позиций цен на сырьё в <u>сфере промышленности</u> на момент времени {current_time}.\n\nВсе цены представлены в долларах$$$",
        reply_markup=keyboards.material_keyboard,parse_mode="HTML")
    
#################################################################

################# Информация📜 ################################

@router.message(F.text == "Информация📜")
async def get_info(message : types.Message):
    await message.answer("Этот бот небольшой пет-проект. Хотелось сделать помощника по финансовому рынку и не только.\n\n"
    "github разработчика - <u>https://github.com/SyntaxSultan-eng</u> (Пока там ничего нет, но вдруг что-то изменится)", reply_markup=keyboards.Information_kb, parse_mode="HTML")

@router.message(F.text == "Версии бота🤖")
async def versions(message: types.Message):
    await message.answer("Версия бота - <u><b>0.1.1version</b></u> (Дата выхода: 12.08.2024  18:19)\n\nВерсия бота - <u><b>0.1version</b></u> (Дата выхода: 12.07.2024  20:46)",reply_markup=keyboards.main_keyboard,parse_mode="HTML")

#################################################################

#0.1.1 version