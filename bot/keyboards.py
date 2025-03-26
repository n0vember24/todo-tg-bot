from aiogram.utils.keyboard import (InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder,
                                    ReplyKeyboardMarkup, KeyboardButton)

from bot.db.requests import get_tasks, get_task

main = InlineKeyboardMarkup(inline_keyboard=[
	[
		InlineKeyboardButton(text='📝 Мои задачи', callback_data='my_tasks'),
		InlineKeyboardButton(text='🖋 Добавить задачу', callback_data='add_task'),
	]
])

cancel = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='❌ Отмена')]],
	resize_keyboard=True,
	one_time_keyboard=True
)

cancel_edit = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='❌ Отмена'), KeyboardButton(text='📌 Оставить текущее')]],
	resize_keyboard=True,
	one_time_keyboard=True
)


async def get_user_tasks(user_id: int):
	tasks = await get_tasks(user_id)
	keyboard = InlineKeyboardBuilder()
	for task in tasks:
		status = '✅' if task.is_done else '❌'
		keyboard.add(InlineKeyboardButton(text=f'{status} {task.title}', callback_data='task_%s' % task.id))
	keyboard.add(
		InlineKeyboardButton(text='🖋 Добавить задачу', callback_data='add_task'),
		InlineKeyboardButton(text='↩️ Назад', callback_data='start')
	)
	return keyboard.adjust(1).as_markup()


async def task_view_settings(task_id: int):
	keyboard = InlineKeyboardBuilder()
	task = await get_task(task_id)
	status = '✅ Выполнено' if task.is_done else '❌ Не выполнено'
	keyboard.add(
		InlineKeyboardButton(text=status, callback_data=f'change_task_status_{task_id}'),
		InlineKeyboardButton(text='🗑 Удалить', callback_data=f'delete_task_{task_id}'),
		InlineKeyboardButton(text='✏️ Изменить', callback_data=f'edit_task_{task_id}'),
		InlineKeyboardButton(text='↩️ Назад', callback_data='my_tasks')
	)
	return keyboard.adjust(1, 3).as_markup()


async def delete_task_confirmation(task_id: int):
	keyboard = InlineKeyboardBuilder()
	keyboard.add(
		InlineKeyboardButton(text='🗑 Да', callback_data=f'delete_confirm_{task_id}'),
		InlineKeyboardButton(text='↩️ Отмена', callback_data=f'task_{task_id}'),
	)
	return keyboard.adjust(2).as_markup()
