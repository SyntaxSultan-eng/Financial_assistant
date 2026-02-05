from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import LinkPreviewOptions
from .mainmenu import Mainmenu_Router
from .admin import Admin_Router
from config import config

import keyboards.keyboard as keyboards
import services.parcer as parc
import datetime

#############################################
#TODO
#Разделить ├── mainmenu.py +
#      │   ├── currency.py
#      │   ├── stocks.py
#      │   ├── economy.py
#      │   ├── admin.py +
#      │   └── states.py
#Или что-то подобное.

router = Router()
router.include_router(Admin_Router)
router.include_router(Mainmenu_Router)

class Form(StatesGroup):
    need_currency = State()


##################### Главные команды ########################

@router.message(Command("stocks"))
@router.message(F.text == 'Рынок акций🌐')
async def Market_stocks(message: types.Message):
    await message.answer("Что вы хотите узнать из мира инвестиций?✍",reply_markup=keyboards.stocks_keyboard)

@router.message(Command("menu"))
@router.message(F.text == "Главное меню↩")
async def return_menu(message: types.Message):
    await message.answer("Возвращаю Вас на главное меню👨🏻‍💻", reply_markup=keyboards.main_keyboard)
    if message.from_user.id == config.bot.admin_id:
        await message.answer("Вы вошли как администратор👑",reply_markup=keyboards.main_admin_keyboard)

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
    if info_world_currency == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.main_keyboard)
        if message.from_user.id == config.bot.admin_id:
            await message.answer("Необходим ремонт🛠️",reply_markup=keyboards.main_admin_keyboard)
    else:
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
        if message.from_user.id == config.bot.admin_id:
            await message.answer("Вы вошли как администратор👑",reply_markup=keyboards.main_admin_keyboard)


#################################################################

################# Рынок акций🌐 ################################

@router.message(F.text == "Взлеты дня💹")
async def give_up_stocks(message: types.Message):
    info_stocks = parc.growth_stocks()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    if info_stocks == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.stocks_keyboard)
    else:
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

    if inf_stock == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.stocks_keyboard)
    else:
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

    if energy_data == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.stocks_keyboard)
    else:
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
    
    if metall_data == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.stocks_keyboard)
    else:
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
    
    if agriculture_data == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.stocks_keyboard)
    else:
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

    if industry_data == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.stocks_keyboard)
    else:
        for info_list in industry_data:
            name = info_list[0]
            price,change_day,percent = info_list[1]

            await message.answer(f"Цена на <u>{name.capitalize()}</u> за день <u>изменилась</u> на <b>{change_day}$</b> (<u><b>{percent}</b></u>)."
                f"->\n\nТекущая цена - <u><b>{price}$</b></u>", parse_mode="HTML")
        await message.answer(f"Вот <u><b>6</b></u> позиций цен на сырьё в <u>сфере промышленности</u> на момент времени {current_time}.\n\nВсе цены представлены в долларах$$$",
            reply_markup=keyboards.material_keyboard,parse_mode="HTML")

################## Крипта ########################################

@router.message(F.text == "Криптовалюта ₿")
async def give_crypto(message: types.Message):
    names_crypto,prices_crypto = parc.crypto()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    if names_crypto == "error_status1":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.stocks_keyboard)
    else:
        for index in range(5):
            await message.answer(f"Цена <u><b>{names_crypto[index]}</b></u> на рынке равна — <u><b>{prices_crypto[index]} $</b></u>",parse_mode="HTML")

        await message.answer(f"Вот <u><b>5</b></u> позиций цен на криптовалюту на момент времени {current_time}.",
            reply_markup=keyboards.stocks_keyboard,parse_mode="HTML")

################## Индексы ######################################

@router.message(F.text == "Индексы бирж📊📈")
async def give_index(message: types.Message):
    await message.answer("Выберите регион🌎",reply_markup=keyboards.indices_keyboard)

@router.callback_query(F.data == "EU")    
async def indices_europe(callback: types.CallbackQuery):
    await callback.message.delete()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    europe_names_index, europe_prices_index, europe_change_index, europe_change_percent = parc.index_europe()
    countries = ["Великобритания", "Германия","Франция","Италия","Испания","Россия","Нидерланды", "Турция","Швейцария", "Швеция"]

    if europe_names_index == "error_status1":
        await callback.message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.stocks_keyboard)
    else:
        for counter in range(10):
            await callback.message.answer(f'Биржа <u>{europe_names_index[counter]}</u>({countries[counter]}) изменилась за день на <u><b>{europe_change_index[counter]}</b></u> пункта (<b>{europe_change_percent[counter]}</b>).\n\n'
            f"Стоимость индекса — <u><b>{europe_prices_index[counter]}</b></u> пунктов.",parse_mode="HTML")
        await callback.message.answer(f"✨Вот <u><b>10</b></u> позиций цен на индексы бирж стран Европы на момент времени {current_time}.",parse_mode="HTML",reply_markup=keyboards.stocks_keyboard)

@router.callback_query(F.data == "USA")
async def indices_USA(callback: types.CallbackQuery):
    await callback.message.delete()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    usa_names_index, usa_prices_index, usa_change_index, usa_change_percent = parc.index_USA()

    if usa_names_index == "error_status1":
        await callback.message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.stocks_keyboard)
    else:
        for counter in range(3):
            await callback.message.answer(f'Биржа <u>{usa_names_index[counter]}</u> изменилась за день на <u><b>{usa_change_index[counter]}</b></u> пункта (<b>{usa_change_percent[counter]}</b>).\n\n'
            f"Стоимость индекса — <u><b>{usa_prices_index[counter]}</b></u> пунктов.",parse_mode="HTML")
        await callback.message.answer(f"✨Вот <u><b>3</b></u> позиций цен на индексы бирж США на момент времени {current_time}.",parse_mode="HTML",reply_markup=keyboards.stocks_keyboard)

@router.callback_query(F.data == "Asia")
async def indices_Asia(callback: types.CallbackQuery):
    await callback.message.delete()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    asia_names_index, asia_prices_index, asia_change_index, asia_change_percent = parc.index_Asia()
    countries = ["Япония", "Китай","Китай","Китай","Китай","Индия","Бангладеш", "Сингапур"]

    if asia_names_index == "error_status1":
        await callback.message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.stocks_keyboard)
    else:
        for counter in range(8):
            await callback.message.answer(f'Биржа <u>{asia_names_index[counter]}</u>({countries[counter]}) изменилась за день на <u><b>{asia_change_index[counter]}</b></u> пункта (<b>{asia_change_percent[counter]}</b>).\n\n'
            f"Стоимость индекса — <u><b>{asia_prices_index[counter]}</b></u> пунктов.",parse_mode="HTML")
        await callback.message.answer(f"✨Вот <u><b>8</b></u> позиций цен на индексы бирж стран Азии на момент времени {current_time}.",parse_mode="HTML",reply_markup=keyboards.stocks_keyboard)
##########################################################

################# Экономика РФ ################################

@router.message(F.text == "Экономика РФ")
async def main_menu_economy(message:types.Message):
    current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    await message.answer(f"Здесь Вы можете найти информацию о состоянии <b>экономики РФ</b> на момент времени: {current_time}",
    reply_markup=keyboards.economy_Rus,parse_mode="HTML")

@router.message(F.text == "Инфляция")
async def get_inflation(message: types.Message):
    data, next_meeting = parc.inflation()

    if data == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.main_keyboard)
        if message.from_user.id == config.bot.admin_id:
            await message.answer("Необходим ремонт🛠️",reply_markup=keyboards.main_admin_keyboard)
    else:
        await message.answer(f"Инфляция на момент времени {list(data['Инфляция'].keys())[1]} (ЦБ РФ) равна - <u><b>{data["Инфляция"][list(data['Инфляция'].keys())[1]]}</b></u>", 
        parse_mode = "HTML")
        await message.answer(f"Цель по инфляции ЦБ РФ равна - <u><b>{data["Инфляция"][list(data['Инфляция'].keys())[0]]}</b></u>", parse_mode="HTML")
        await message.answer(f"Значение ключевой ставки равно - <u><b>{data["Ключевая ставка"]}</b></u>",
        parse_mode="HTML")
        await message.answer(f"{list(next_meeting.keys())[0]} - <u><b>{next_meeting[list(next_meeting.keys())[0]]}</b></u>",
        parse_mode="HTML", reply_markup=keyboards.economy_Rus)

@router.message(F.text == "Безработица")
async def unemployment(message: types.Message):
    info_dict = parc.info_economy_rus()

    if info_dict == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.main_keyboard)
        if message.from_user.id == config.bot.admin_id:
            await message.answer("Необходим ремонт🛠️",reply_markup=keyboards.main_admin_keyboard)
    else:
        keys_dict = list(info_dict.keys())

        await message.answer(f"{keys_dict[-2]} - <u><b>{info_dict[keys_dict[-2]][0]+info_dict[keys_dict[-2]][1]}</b></u>",
        parse_mode="HTML")
        await message.answer(f"{keys_dict[0]} - равна <u><b>{info_dict[keys_dict[0]][0]+" "+info_dict[keys_dict[0]][1]}</b></u> ",
        parse_mode="HTML")
        await message.answer(f"{keys_dict[-1]} равна - <u><b>{info_dict[keys_dict[-1]][0]+' '+info_dict[keys_dict[-1]][1]}</b></u>",parse_mode="HTML",reply_markup=keyboards.economy_Rus)

@router.message(F.text == "ВВП")
async def VVP(message: types.Message):
    info_dict = parc.info_economy_rus()

    if info_dict == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.main_keyboard)
        if message.from_user.id == config.bot.admin_id:
            await message.answer("Необходим ремонт🛠️",reply_markup=keyboards.main_admin_keyboard)
    else:
        keys_dict = list(info_dict.keys())

        await message.answer(f"{keys_dict[1]} - <u><b>{info_dict[keys_dict[1]][0]+' '+info_dict[keys_dict[1]][1]}</b></u>",
        parse_mode="HTML")
        await message.answer(f"{keys_dict[2]} - <u><b>{info_dict[keys_dict[2]][0]+info_dict[keys_dict[2]][1]}</b></u>",
        parse_mode="HTML",reply_markup=keyboards.economy_Rus)

@router.message(F.text == "Индекс промышленного производства")
async def index_production(message: types.Message):
    info_dict = parc.info_economy_rus()

    if info_dict == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.main_keyboard)
        if message.from_user.id == config.bot.admin_id:
            await message.answer("Необходим ремонт🛠️",reply_markup=keyboards.main_admin_keyboard)
    else:
        keys_dict = list(info_dict.keys())

        await message.answer(f"{keys_dict[3]} - <u><b>{info_dict[keys_dict[3]][0]+info_dict[keys_dict[3]][1]}</b></u>",
        parse_mode="HTML",reply_markup=keyboards.economy_Rus)

@router.message(F.text == "Индекс потребительских цен")
async def index_price(message: types.Message):
    info_dict = parc.info_economy_rus()

    if info_dict == "error_status":
        await message.answer("Извините, но данная функция на ремонте🔧",reply_markup=keyboards.main_keyboard)
        if message.from_user.id == config.bot.admin_id:
            await message.answer("Необходим ремонт🛠️",reply_markup=keyboards.main_admin_keyboard)
    else:
        keys_dict = list(info_dict.keys())

        await message.answer(f"{keys_dict[4]} - <u><b>{info_dict[keys_dict[4]][0]+info_dict[keys_dict[4]][1]}</b></u>",
        parse_mode="HTML",reply_markup=keyboards.economy_Rus)

#################################################################

#0.5 version