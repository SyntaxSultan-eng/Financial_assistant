import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import router
from decouple import config

############################################

API_TOKEN = config('API_KEY',default = '')
bot = Bot(API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

############################################

async def on_startup():
    print("Bot has started working🚀", end = '\n\n')

async def main() -> None:
    dp.include_router(router = router)
    dp.startup.register(callback = on_startup)
    await dp.start_polling(bot)

############################################

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot has stopped working❌')

#0.3 version