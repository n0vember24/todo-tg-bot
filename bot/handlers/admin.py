from typing import Union

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import bot.keyboards as kb
from bot.db.requests import UserManager, TaskManager
from bot.filters import IsBotAdmin

router = Router()


@router.message(Command('admin'), IsBotAdmin())
@router.callback_query(F.data == 'admin', IsBotAdmin())
async def admin_command(msg_or_cb: Union[Message, CallbackQuery]):
	"""Handler for :code:`/admin` command and :code:`admin` callback"""
	users_count = await UserManager.count()
	tasks_count = await TaskManager.count()
	admin_txt = f'''
Добро пожаловать в админку, _{msg_or_cb.from_user.first_name}_ 👮‍♂️

📈 Статистика бота:
- 👥 Количество пользователей за всё время: {users_count}
- 📝 Количество задач всех пользователей: {tasks_count}
	'''
	if isinstance(msg_or_cb, Message):
		await msg_or_cb.answer(admin_txt, reply_markup=kb.admin_main)
	else:
		await msg_or_cb.message.edit_text(admin_txt, reply_markup=kb.admin_main)


@router.callback_query(F.data == 'all_users')
async def all_users(cb: CallbackQuery):
	await cb.message.edit_text(
		'Вот список всех пользователей бота, вы можете посмотреть на их задачи:',
		reply_markup=await kb.admin_get_all_users(cb.bot))


@router.callback_query(F.data.startswith('user_'))
async def view_user_tasks(cb: CallbackQuery):
	"""View tasks of a specified user"""
	user_id = int(cb.data.split('_')[-1])
	user = await cb.bot.get_chat(user_id)
	user_info = f'Полное имя пользователя: *{user.full_name}*\nUsername: *@{user.username}*\nID: *{user.id}*'
	await cb.message.edit_text(user_info, reply_markup=await kb.admin_get_user_tasks(user_id))


@router.callback_query(F.data.startswith('admin_task_'))
async def view_task(cb: CallbackQuery):
	"""View task details"""
	task = await TaskManager.get(int(cb.data.split('_')[-1]))
	txt = f'*{task.title}*\n\n{task.description}'
	await cb.message.edit_text(txt, reply_markup=await kb.admin_view_task_details(task))
