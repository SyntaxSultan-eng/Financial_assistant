from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Курс валют(ЦБ РФ)🏛️'),KeyboardButton(text = 'Рынок акций🌐')],
    [KeyboardButton(text = "Информация📜")]
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

#0.2 version