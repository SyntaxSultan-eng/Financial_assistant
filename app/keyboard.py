from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Курс валют(ЦБ РФ)🏛️')],
    [KeyboardButton(text = '📋Информация')]
], 
    resize_keyboard= True,
    input_field_placeholder='Выберите режим',
)

