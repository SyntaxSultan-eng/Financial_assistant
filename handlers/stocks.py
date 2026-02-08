from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards import (
    stocks_keyboard,
    material_keyboard,
    indices_keyboard
)
from .admin import id_check_admin
from services.parcer import (
    growth_stocks,
    drop_stocks,
    # energy,
    metall,
    agriculture,
    industry,
    crypto,
    index_europe,
    index_USA,
    index_Asia
)

####################################

Stocks_Router = Router()

####################################

################## Акции ################################


@Stocks_Router.message(Command('stocks'))
@Stocks_Router.message(F.text == 'Рынок акций🌐')
async def Market_stocks(message: Message):
    await message.answer(
        'Что вы хотите узнать из мира инвестиций?✍',
        reply_markup=stocks_keyboard
    )

# TODO
# Взлеты и падения можно объединить в одну функцию, которой передать
# ссылку на источник


@Stocks_Router.message(F.text == 'Взлеты дня💹')
async def up_stocks(message: Message):
    info_stocks = growth_stocks()
    current_time = datetime.now().strftime("%H:%M:%S")

    if info_stocks == 'error_status':
        await message.answer(
            'Извините, но данная функция на ремонте🔧',
            reply_markup=stocks_keyboard
        )
        await id_check_admin(
            message=message,
            user_id=message.from_user.id,
            text='Необходим ремонт🛠️',
            keyboard_name=stocks_keyboard
        )
        return

    for stock in info_stocks:
        Code_name = stock[0][:4]
        Full_name = stock[0][4:]
        Change_percent = stock[1]
        Price = stock[2]
        Subject = stock[10]

        await message.answer(
            f'(<b>{Code_name}</b>) {Full_name} ({Subject}) -> \n\n'
            f'Изменения за день на <u><b>{Change_percent}</b></u>↗ -> \n\n'
            f'<u>Текущая цена <b>{Price}</b></u>',
            parse_mode="HTML"
        )

    await message.answer(
        '😎Вот первые <u><b>10</b></u> позиций в лидерах роста '
        f'на момент времени {current_time} (по МСК)',
        reply_markup=stocks_keyboard,
        parse_mode="HTML"
    )


@Stocks_Router.message(F.text == 'Падения дня📉')
async def down_stocks(message: Message):
    info_stocks = drop_stocks()
    current_time = datetime.now().strftime("%H:%M:%S")

    if info_stocks == 'error_status':
        await message.answer(
            'Извините, но данная функция на ремонте🔧',
            reply_markup=stocks_keyboard
        )
        await id_check_admin(
            message=message,
            user_id=message.from_user.id,
            text='Необходим ремонт🛠️',
            keyboard_name=stocks_keyboard
        )
        return

    for stock in info_stocks:
        Code_name = stock[0][:4]
        Full_name = stock[0][4:]
        Change_percent = stock[1]
        Price = stock[2]
        Subject = stock[10]

        await message.answer(
            f'(<b>{Code_name}</b>) {Full_name} ({Subject}) -> \n\n'
            f'Изменения за день на <u><b>{Change_percent}</b></u>↗ -> \n\n'
            f'<u>Текущая цена <b>{Price}</b></u>',
            parse_mode="HTML"
        )
    await message.answer(
        '😒Вот первые <u><b>10</b></u> позиций в лидерах падения〽 '
        f'на момент времени {current_time}',
        reply_markup=stocks_keyboard,
        parse_mode="HTML"
    )

################## Сырье ########################################


@Stocks_Router.message(F.text == 'Рынок Сырья⛏️')
async def menu_material(message: Message):
    await message.answer(
        'Какой сектор экономики Вас интересует? '
        'Данные основаны на <u><b>Фьючерсных контрактах</b></u>',
        reply_markup=material_keyboard,
        parse_mode="HTML"
    )


@Stocks_Router.message(F.text == 'Энергетика⚡')
async def get_energy(message: Message):
    # energy_data = energy() Не работает
    # current_time = datetime.now().strftime("%H:%M:%S")

    await message.answer(
        'Извините, но данная функция на ремонте🔧',
        reply_markup=stocks_keyboard
    )
    await id_check_admin(
        message=message,
        user_id=message.from_user.id,
        text='Необходим ремонт🛠️',
        keyboard_name=stocks_keyboard
    )
    return

    # for info_list in energy_data:
    #     name = info_list[0]
    #     price,change_day,percent = info_list[1]

    #     await message.answer(
    #         f'Цена на <u>{name.capitalize()}</u> за день <u>изменилась</u> '
    #         f'на <b>{change_day}$</b> (<u><b>{percent}</b></u>).'
    #         f'->\n\nТекущая цена - <u><b>{price}$</b></u>',
    #         parse_mode="HTML"
    #     )
    # await message.answer(
    #     'Вот <u><b>6</b></u> позиций цен на сырьё в <u>сфере энергетики</u> '
    #     f'на момент времени {current_time}.\n\n'
    #     'Все цены представлены в долларах$$$',
    #     reply_markup=material_keyboard,
    #     parse_mode="HTML"
    # )


@Stocks_Router.message(F.text == 'Металлы🔩')
async def get_metall(message: Message):
    metall_data = metall()
    current_time = datetime.now().strftime("%H:%M:%S")

    if metall_data == 'error_status':
        await message.answer(
            'Извините, но данная функция на ремонте🔧',
            reply_markup=stocks_keyboard
        )
        await id_check_admin(
            message=message,
            user_id=message.from_user.id,
            text='Необходим ремонт🛠️',
            keyboard_name=stocks_keyboard
        )
        return

    for info_list in metall_data:
        name = info_list[0]
        price, change_day, percent = info_list[1]

        await message.answer(
            f'Цена на <u>{name.capitalize()}</u> за день <u>изменилась</u> '
            f'на <b>{change_day}$</b> (<u><b>{percent}</b></u>).'
            f'->\n\nТекущая цена - <u><b>{price}$</b></u>',
            parse_mode="HTML"
        )
    await message.answer(
        'Вот <u><b>5</b></u> позиций цен на сырьё в <u>сфере металлов</u> '
        f'на момент времени {current_time}.\n\n'
        'Все цены представлены в долларах$$$',
        reply_markup=material_keyboard,
        parse_mode="HTML"
    )


@Stocks_Router.message(F.text == 'Сельское хоз. 🌱')
async def get_agriculture(message: Message):
    agriculture_data = agriculture()
    current_time = datetime.now().strftime("%H:%M:%S")

    if agriculture_data == 'error_status':
        await message.answer(
            'Извините, но данная функция на ремонте🔧',
            reply_markup=stocks_keyboard
        )
        await id_check_admin(
            message=message,
            user_id=message.from_user.id,
            text='Необходим ремонт🛠️',
            keyboard_name=stocks_keyboard
        )
        return

    for info_list in agriculture_data:
        name = info_list[0]
        price, change_day, percent = info_list[1]

        await message.answer(
            f'Цена на <u>{name.capitalize()}</u> за день <u>изменилась</u> '
            f'на <b>{change_day}$</b> (<u><b>{percent}</b></u>).'
            f'->\n\nТекущая цена - <u><b>{price}$</b></u>',
            parse_mode="HTML"
        )
    await message.answer(
        'Вот <u><b>6</b></u> позиций цен на сырьё в <u>сфере сельского хозяйства</u> '
        f'на момент времени {current_time}.\n\n'
        'Все цены представлены в долларах$$$',
        reply_markup=material_keyboard,
        parse_mode="HTML"
    )


@Stocks_Router.message(F.text == "Промышленность⚙️")
async def get_industry(message: Message):
    industry_data = industry()
    current_time = datetime.now().strftime("%H:%M:%S")

    if industry_data == "error_status":
        await message.answer(
            'Извините, но данная функция на ремонте🔧',
            reply_markup=stocks_keyboard
        )
        await id_check_admin(
            message=message,
            user_id=message.from_user.id,
            text='Необходим ремонт🛠️',
            keyboard_name=stocks_keyboard
        )
        return

    for info_list in industry_data:
        name = info_list[0]
        price, change_day, percent = info_list[1]

        await message.answer(
            f'Цена на <u>{name.capitalize()}</u> за день <u>изменилась</u> '
            f'на <b>{change_day}$</b> (<u><b>{percent}</b></u>).'
            f'->\n\nТекущая цена - <u><b>{price}$</b></u>',
            parse_mode="HTML"
        )
    await message.answer(
        'Вот <u><b>6</b></u> позиций цен на сырьё в <u>сфере промышленности</u> '
        f'на момент времени {current_time}.\n\n'
        'Все цены представлены в долларах$$$',
        reply_markup=material_keyboard,
        parse_mode="HTML"
    )

################## Крипта ########################################


@Stocks_Router.message(F.text == 'Криптовалюта ₿')
async def give_crypto(message: Message):
    names_crypto, prices_crypto = crypto()
    current_time = datetime.now().strftime("%H:%M:%S")

    if names_crypto == 'error_status1':
        await message.answer(
            'Извините, но данная функция на ремонте🔧',
            reply_markup=stocks_keyboard
        )
        await id_check_admin(
            message=message,
            user_id=message.from_user.id,
            text='Необходим ремонт🛠️',
            keyboard_name=stocks_keyboard
        )
        return

    for index in range(5):
        await message.answer(
            f'Цена <u><b>{names_crypto[index]}</b></u> на рынке равна'
            f' — <u><b>{prices_crypto[index]} $</b></u>',
            parse_mode="HTML"
        )

    await message.answer(
        'Вот <u><b>5</b></u> позиций цен на криптовалюту '
        f'на момент времени {current_time}.',
        reply_markup=stocks_keyboard,
        parse_mode="HTML"
    )

################## Индексы ######################################


@Stocks_Router.message(F.text == 'Индексы бирж📊📈')
async def give_index(message: Message):
    await message.answer(
        'Выберите регион🌎',
        reply_markup=indices_keyboard
    )


@Stocks_Router.callback_query(F.data == 'EU')
async def indices_europe(callback: CallbackQuery):
    await callback.message.delete()
    current_time = datetime.now().strftime("%H:%M:%S")

    europe_names_index, europe_prices_index, europe_change_index, europe_change_percent = index_europe()
    countries = ["Великобритания", "Германия","Франция","Италия","Испания","Россия","Нидерланды", "Турция","Швейцария", "Швеция"]

    if europe_names_index == "error_status1":
        await callback.message.answer(
            'Извините, но данная функция на ремонте🔧',
            reply_markup=stocks_keyboard
        )
        await id_check_admin(
            message=callback.message,
            user_id=callback.from_user.id,
            text='Необходим ремонт🛠️',
            keyboard_name=stocks_keyboard
        )
        return

    for counter in range(10):
        await callback.message.answer(
            f'Биржа <u>{europe_names_index[counter]}</u>({countries[counter]}) изменилась '
            f'за день на <u><b>{europe_change_index[counter]}</b></u> пункта '
            f'(<b>{europe_change_percent[counter]}</b>).\n\n'
            f'Стоимость индекса — <u><b>{europe_prices_index[counter]}</b></u> пунктов.',
            parse_mode="HTML"
        )
    await callback.message.answer(
        '✨Вот <u><b>10</b></u> позиций цен на индексы бирж стран Европы '
        f'на момент времени {current_time}.',
        parse_mode="HTML",
        reply_markup=stocks_keyboard
    )

@Stocks_Router.callback_query(F.data == 'USA')
async def indices_USA(callback: CallbackQuery):
    await callback.message.delete()
    current_time = datetime.now().strftime("%H:%M:%S")

    usa_names_index, usa_prices_index, usa_change_index, usa_change_percent = index_USA()

    if usa_names_index == "error_status1":
        await callback.message.answer(
            'Извините, но данная функция на ремонте🔧',
            reply_markup=stocks_keyboard
        )
        await id_check_admin(
            message=callback.message,
            user_id=callback.from_user.id,
            text='Необходим ремонт🛠️',
            keyboard_name=stocks_keyboard
        )
        return

    for counter in range(3):
        await callback.message.answer(
            f'Биржа <u>{usa_names_index[counter]}</u> изменилась '
            f'за день на <u><b>{usa_change_index[counter]}</b></u> пункта '
            f'(<b>{usa_change_percent[counter]}</b>).\n\n'
            f'Стоимость индекса — <u><b>{usa_prices_index[counter]}</b></u> пунктов.',
            parse_mode="HTML"
        )
    await callback.message.answer(
        '✨Вот <u><b>3</b></u> позиций цен на индексы бирж США '
        f'на момент времени {current_time}.',
        parse_mode="HTML",
        reply_markup=stocks_keyboard
    )


@Stocks_Router.callback_query(F.data == 'Asia')
async def indices_Asia(callback: CallbackQuery):
    await callback.message.delete()
    current_time = datetime.now().strftime("%H:%M:%S")

    asia_names_index, asia_prices_index, asia_change_index, asia_change_percent = index_Asia()
    countries = ["Япония", "Китай","Китай","Китай","Китай","Индия","Бангладеш", "Сингапур"]

    if asia_names_index == "error_status1":
        await callback.message.answer(
            'Извините, но данная функция на ремонте🔧',
            reply_markup=stocks_keyboard
        )
        await id_check_admin(
            message=callback.message,
            user_id=callback.from_user.id,
            text='Необходим ремонт🛠️',
            keyboard_name=stocks_keyboard
        )
        return

    for counter in range(8):
        await callback.message.answer(
            f'Биржа <u>{asia_names_index[counter]}</u>({countries[counter]}) изменилась '
            f'за день на <u><b>{asia_change_index[counter]}'
            f'</b></u> пункта (<b>{asia_change_percent[counter]}</b>).\n\n'
            f'Стоимость индекса — <u><b>{asia_prices_index[counter]}</b></u> пунктов.',
            parse_mode="HTML"
        )
    await callback.message.answer(
        '✨Вот <u><b>8</b></u> позиций цен на индексы бирж стран Азии '
        f'на момент времени {current_time}.',
        parse_mode="HTML",
        reply_markup=
        stocks_keyboard
    )
