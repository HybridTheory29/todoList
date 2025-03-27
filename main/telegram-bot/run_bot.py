import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from decouple import config

from body.handlers import user_router

bot = Bot(config('TG_BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def main():
    dp.include_router(user_router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot)

async def startup(dispatcher: Dispatcher):
    print('Starting up...')


async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass