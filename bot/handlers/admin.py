from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db.requests import UserManager, TaskManager
from bot.filters import IsBotAdmin

router = Router()


@router.message(Command('admin'), IsBotAdmin())
async def admin_command(msg: Message):
	admin_txt = f'''
Добро пожаловать в админку, _{msg.from_user.first_name}_ 👮‍♂️

📈 Статистика бота:
- 👥 Количество пользователей за всё время: {await UserManager.count()}
- 📝 Количество задач всех пользователей: {await TaskManager.count()}
'''
	await msg.answer(admin_txt)
