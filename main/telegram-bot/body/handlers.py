from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Это бот сайта TodoList. Он будет присылать вам напоминания о ваших невыполненных задачах.')