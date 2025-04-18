import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoList.settings')
django.setup()

import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from decouple import config
from main.models import Task

user_router = Router()
bot = Bot(config('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('start connect to site db...')
    await message.answer(Task.objects)

async def main():
    dp.include_router(user_router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot)

async def startup(dispatcher: Dispatcher):
#    await async_main()
    print('Starting up...')


async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass