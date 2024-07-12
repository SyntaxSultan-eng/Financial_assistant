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
    [KeyboardButton(text = "Главное меню↩")]
],
    resize_keyboard= True,
    input_field_placeholder='Выберите режим',
)
#################################################
material_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Энергетика⚡"), KeyboardButton(text="Металлы🔩")],
    [KeyboardButton(text="Сельское хоз. 🌱"), KeyboardButton(text="Промышленность⚙️")],
    [KeyboardButton(text= "Главное меню↩")]
],
    resize_keyboard=True
)
#################################################
setting_currency = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Мировые валюты💲",callback_data="world_currency")],
    [InlineKeyboardButton(text="Конкретная валюта🔎", callback_data="need_currency")],
],
    resize_keyboard= True,
)
#################################################
checkingNONE_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Да", callback_data="True_info"), InlineKeyboardButton(text="Нет", callback_data="False_info")]    
],
    resize_keyboard = True,
)

checking_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Да", callback_data="Right_info"), InlineKeyboardButton(text="Нет", callback_data="Lie_info")]    
],
    resize_keyboard = True,
)
#################################################
Information_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Версии бота🤖"), KeyboardButton(text= "Главное меню↩")]
],
    resize_keyboard=True
)

#0.1 version