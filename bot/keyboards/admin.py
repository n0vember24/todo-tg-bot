from aiogram.client.bot import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from bot.db.models import Task
from bot.db.requests import UserManager, TaskManager

admin_main = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='👥 Пользователи', callback_data='all_users'),
	 InlineKeyboardButton(text='🏠 Главное', callback_data='start')]
])


async def admin_get_all_users(bot: Bot):
	"""Get all users of the bot"""
	users = await UserManager.get()
	kb = InlineKeyboardBuilder()
	for user in users:
		tg_user = await bot.get_chat(user.tg_id)
		kb.add(InlineKeyboardButton(text=f'{tg_user.first_name} - {tg_user.id}', callback_data=f'user_{tg_user.id}'))
	kb.add(InlineKeyboardButton(text='↩️ Назад', callback_data='admin'))
	return kb.adjust(1).as_markup()


async def admin_get_user_tasks(user_id: int):
	"""Get tasks of specified user by his ID"""
	tasks = await TaskManager.get_by_user(user_id)
	kb = InlineKeyboardBuilder()
	for task in tasks:
		status = '✅' if task.is_done else '❌'
		kb.add(InlineKeyboardButton(text=f'{status} {task.title}', callback_data=f'admin_task_{task.id}'))
	kb.add(InlineKeyboardButton(text='↩️ Назад', callback_data='all_users'))
	return kb.adjust(1).as_markup()


async def admin_view_task_details(task: Task):
	"""View a task details by its ID"""
	kb = InlineKeyboardBuilder()
	status = '✅ Выполнено' if task.is_done else '❌ Не выполнено'
	kb.add(InlineKeyboardButton(text=status, callback_data='0'),
	       InlineKeyboardButton(text='↩️ Назад', callback_data=f'user_{task.user_id}'))
	return kb.as_markup()
