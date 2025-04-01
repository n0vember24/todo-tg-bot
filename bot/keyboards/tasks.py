from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

from bot.db.models import Task
from bot.db.requests import TaskManager


async def get_user_tasks(user_id: int):
	tasks = await TaskManager.get_by_user(user_id)
	kb = InlineKeyboardBuilder()
	for task in tasks:
		status = '✅' if task.is_done else '❌'
		kb.add(InlineKeyboardButton(text=f'{status} {task.title}', callback_data=f'task_{task.id}'))
	kb.add(
		InlineKeyboardButton(text='🖋 Добавить задачу', callback_data='add_task'),
		InlineKeyboardButton(text='↩️ Назад', callback_data='start')
	)
	return kb.adjust(1).as_markup()


async def view_task_details(task: Task):
	kb = InlineKeyboardBuilder()
	status = '✅ Выполнено' if task.is_done else '❌ Не выполнено'
	kb.add(
		InlineKeyboardButton(text=status, callback_data=f'change_task_status_{task.id}'),
		InlineKeyboardButton(text='🗑 Удалить', callback_data=f'delete_task_{task.id}'),
		InlineKeyboardButton(text='✏️ Изменить', callback_data=f'edit_task_{task.id}'),
		InlineKeyboardButton(text='↩️ Назад', callback_data='my_tasks')
	)
	return kb.adjust(1, 3).as_markup()


async def delete_task_confirmation(task_id: int):
	kb = InlineKeyboardBuilder()
	kb.add(
		InlineKeyboardButton(text='🗑 Да', callback_data=f'delete_confirm_{task_id}'),
		InlineKeyboardButton(text='↩️ Отмена', callback_data=f'task_{task_id}'),
	)
	return kb.adjust(2).as_markup()
