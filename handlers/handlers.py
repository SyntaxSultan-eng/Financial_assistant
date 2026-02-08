from aiogram import Router 

from .mainmenu import Mainmenu_Router
from .admin import Admin_Router
from .currency import Currency_Router
from .economy import Economy_Router
from .stocks import Stocks_Router



#############################################
#TODO
#Разобраться с этим файлом. Как-то модифицировать 
#или просто убрать.

router = Router()
router.include_router(Admin_Router)
router.include_router(Stocks_Router)
router.include_router(Currency_Router)
router.include_router(Economy_Router)
router.include_router(Mainmenu_Router)

# class Form(StatesGroup):
#     need_currency = State()

##################### Главные команды ########################


# @router.message(Command('cancel'))
# async def choose_cancel(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()

#     if current_state is None:
#         await message.answer("Нечего отменять💀", reply_markup=keyboards.main_keyboard)
#         return
    
#     await state.clear()
#     await message.answer("Действие отменено⛔",reply_markup=keyboards.main_keyboard)


#################################################################

#0.5 version