from aiogram import Router, F
from aiogram.types import Message, CallbackQuery


from keyboards import (
    main_admin_keyboard,
    admin_panel,
    toggle_panel
)
from config import config


###############################

Admin_Router = Router()


class AdminFunctionManager:
    """Класс для управления функциями в боте"""
    def __init__(self):
        self.callbackquery_commands = {
            'currency': True,
            'up': True,
            'down': True,
            'material': True,
            'crypto': True,
            'index': True,
            'economy': True
        }
        self.func_names = {
            'currency': 'Курс валют(ЦБ РФ)🏛️',
            'up': 'Взлеты дня💹',
            'down': 'Падения дня📉',
            'material': 'Рынок Сырья⛏️',
            'crypto': 'Криптовалюта ₿',
            'index': '(Индексы бирж📊📈',
            'economy': 'Экономика РФ'
        }

    def get_status(self, callback: str) -> bool:
        return self.callbackquery_commands.get(callback, False)

    def toggle_status(self, callback: str) -> bool:
        self.callbackquery_commands[callback] = not self.callbackquery_commands[callback]
        return self.callbackquery_commands[callback]

    def get_func_name(self, callback: str) -> str:
        return self.func_names.get(callback)

    def get_all_keys(self) -> list:
        return list(self.callbackquery_commands.keys())


Manager = AdminFunctionManager()

###############################


async def id_check_admin(message: Message, user_id: int, text: str, keyboard_name=main_admin_keyboard) -> None:
    """Функция для проверки id пользователя с id админа и вывода нужной клавиатуры."""
    if config.bot.admin_id == user_id:
        await message.answer(
            text,
            reply_markup=keyboard_name
        )


@Admin_Router.message(F.text == 'Панель админа👑')
async def admin_menu(message: Message) -> None:
    await id_check_admin(
        message=message,
        user_id=message.from_user.id,
        text='Пункт управления🕹️',
        keyboard_name=admin_panel
    )


@Admin_Router.message(F.text == "Отключить/Включить функцию")
async def admin_toggle(message: Message):
    await id_check_admin(
        message=message,
        user_id=message.from_user.id,
        text='Выбери функцию, которую нужно вкл/выкл.',
        keyboard_name=toggle_panel
    )


@Admin_Router.callback_query(F.data.in_(Manager.get_all_keys()))
async def switch_command(callback: CallbackQuery):
    await callback.message.delete()

    switch = ['❌ ВЫКЛЮЧЕНО', '✅ ВКЛЮЧЕНО']
    result = Manager.toggle_status(callback=callback.data)
    name_of_func = Manager.get_func_name(callback=callback.data)

    await callback.message.answer(
        f'Функция {name_of_func} изменила своё состояние на <u><b>{switch[int(result)]}</b></u>💻',
        parse_mode="HTML",
        reply_markup=admin_panel
    )


@Admin_Router.message(F.text == "Состояние команд📋")
async def check_admin_command(message: Message):

    answer = ''
    work_or_not = ['Не Работает❗', 'Работает✔️']

    for callback in Manager.get_all_keys():
        answer += f'{Manager.get_func_name(callback)} - {work_or_not[int(Manager.get_status(callback))]}\n\n'

    await id_check_admin(
        message=message,
        user_id=message.from_user.id,
        text=answer,
        keyboard_name=admin_panel
    )
