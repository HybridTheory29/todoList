from aiogram import Router, F
from keyboards.all_keyboards import main_kb, item_kb, action_kb
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from main.models import Profile


start_router = Router()

@start_router.message(CommandStart())
async def start_cmd(message: Message):
    user = message.from_user
    chat_id = message.chat.id
    username = user.username

    try:
        profile = Profile.objects.get(user__username=username)
        profile.telegram_chat_id = chat_id
        profile.save()
        await message.answer("Ваш Telegram ID успешно сохранен!")
    except Profile.DoesNotExist:
        await message.answer("Профиль не найден. Пожалуйста, зарегистрируйтесь на сайте.")

    await message.answer('Привет!')

async def send_telegram_notification(chat_id: int, message: str):
    await bot.send_message(chat_id, message, parse_mode=ParseMode.HTML)