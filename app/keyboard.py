from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Курс валют(ЦБ РФ)🏛️'),KeyboardButton(text = 'Рынок акций🌐')]
], 
    resize_keyboard= True,
    input_field_placeholder='Выберите режим',
)

stocks_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = "Взлеты дня💹"), KeyboardButton(text="Падения дня📉")],
    [KeyboardButton(text = "Главное меню↩")]
],
    resize_keyboard= True,
    input_field_placeholder='Выберите режим',
)

setting_currency = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Мировые валюты💲",callback_data="world_currency")],
    [InlineKeyboardButton(text="Конкретная валюта🔎", callback_data="need_currency")],
],
    resize_keyboard= True,
)

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