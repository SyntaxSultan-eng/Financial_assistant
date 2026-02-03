from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# Кнопки для главного меню(не админ)
main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Курс валют(ЦБ РФ)🏛️'),KeyboardButton(text = 'Рынок акций🌐')],
    [KeyboardButton(text = "Информация📜"), KeyboardButton(text = "Экономика РФ")]
], 
    resize_keyboard= True,
    input_field_placeholder='Выберите режим',
)

# Кнопки для главного меню(админ)
main_admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Курс валют(ЦБ РФ)🏛️'),KeyboardButton(text = 'Рынок акций🌐')],
    [KeyboardButton(text = "Информация📜"), KeyboardButton(text="Экономика РФ")],
    [KeyboardButton(text = "Панель админа👑")]
], 
    resize_keyboard= True,
    input_field_placeholder='Выберите режим',
)

#################################################
################ Раздел Рынок акций #############

stocks_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = "Взлеты дня💹"), KeyboardButton(text="Падения дня📉"), KeyboardButton(text="Рынок Сырья⛏️")],
    [KeyboardButton(text = "Криптовалюта ₿"),KeyboardButton(text = "Индексы бирж📊📈")],
    [KeyboardButton(text = "Главное меню↩")]
],
    resize_keyboard= True,
    input_field_placeholder='Выберите режим',
)
indices_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Европа",callback_data="EU")],
    [InlineKeyboardButton(text="США", callback_data="USA")],
    [InlineKeyboardButton(text = "Азия", callback_data="Asia")]
])

material_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Энергетика⚡"), KeyboardButton(text="Металлы🔩")],
    [KeyboardButton(text="Сельское хоз. 🌱"), KeyboardButton(text="Промышленность⚙️")],
    [KeyboardButton(text= "Главное меню↩")]
],
    resize_keyboard=True
)

#################################################
############### Раздел Экономика РФ #############

economy_Rus = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Инфляция"), KeyboardButton(text="Безработица")],
    [KeyboardButton(text = "ВВП")],
    [KeyboardButton(text = "Индекс промышленного производства"), KeyboardButton(text = "Индекс потребительских цен")],
    [KeyboardButton(text= "Главное меню↩")]
],
    resize_keyboard=True
)

#################################################
####### Раздел Информации + Админ панель ########

Information_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Версии бота🤖"), KeyboardButton(text= "Главное меню↩")]
],
    resize_keyboard=True
)

admin_panel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Состояние команд📋"), KeyboardButton(text="Отключить/Включить функцию")],
    [KeyboardButton(text="Главное меню↩")]

],
    resize_keyboard=True
)

toggle_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Курс валют(ЦБ РФ)🏛️", callback_data="currency")],
    [InlineKeyboardButton(text="Взлеты дня💹",callback_data="up"), InlineKeyboardButton(text="Падения дня📉", callback_data="down")],
    [InlineKeyboardButton(text="Рынок Сырья⛏️",callback_data="material")],
    [InlineKeyboardButton(text="Криптовалюта ₿",callback_data="crypto"), InlineKeyboardButton(text="Индексы бирж📊📈",callback_data='index')],
    [InlineKeyboardButton(text="Экономика РФ", callback_data="economy")]
])

#TODO
#Разбить код на несколько файлов(main_keyboard.py, stocks_keyboard.py и т.д)
#Создать base.py, где будет храниться константы("Главное меню↩" и т.д) (как в config базовый класс)
#Настроить __init__.py