from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Курс валют(ЦБ РФ)🏛️'),KeyboardButton(text = 'Рынок акций🌐')],
    [KeyboardButton(text = "Информация📜")]
], 
    resize_keyboard= True,
    input_field_placeholder='Выберите режим',
)
main_admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Курс валют(ЦБ РФ)🏛️'),KeyboardButton(text = 'Рынок акций🌐')],
    [KeyboardButton(text = "Информация📜"), KeyboardButton(text = "Панель админа👑")]
], 
    resize_keyboard= True,
    input_field_placeholder='Выберите режим',
)
#################################################
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
#################################################
material_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Энергетика⚡"), KeyboardButton(text="Металлы🔩")],
    [KeyboardButton(text="Сельское хоз. 🌱"), KeyboardButton(text="Промышленность⚙️")],
    [KeyboardButton(text= "Главное меню↩")]
],
    resize_keyboard=True
)
#################################################
Information_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Версии бота🤖"), KeyboardButton(text= "Главное меню↩")]
],
    resize_keyboard=True
)
#################################################
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
    [InlineKeyboardButton(text="Криптовалюта ₿",callback_data="crypto"), InlineKeyboardButton(text="Индексы бирж📊📈",callback_data='index')]
])

#0.3.5 version