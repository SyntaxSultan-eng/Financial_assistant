from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Курс валют(ЦБ РФ)🏛️'),KeyboardButton(text = '📋Информация')]
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