from typing import Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import bot.keyboards as kb
from bot.db.requests import TaskManager
from bot.filters import StatusFilter
from bot.states import Task as TaskState

router = Router()


@router.message(Command('my_tasks'))
@router.callback_query(F.data == 'my_tasks')
async def my_tasks(msg_or_cb: Union[Message, CallbackQuery]):
	"""View a list of user tasks"""
	user_id = msg_or_cb.from_user.id
	task_text = 'Вот ваши задачи 👇'
	if isinstance(msg_or_cb, Message):
		await msg_or_cb.answer(task_text, reply_markup=await kb.get_user_tasks(user_id))
	else:
		await msg_or_cb.message.edit_text(task_text, reply_markup=await kb.get_user_tasks(user_id))


@router.message(Command('add_task'))
@router.callback_query(F.data == 'add_task')
async def add_task(msg_or_cb: Union[Message, CallbackQuery], state: FSMContext):
	"""Create a new task"""
	user_id = msg_or_cb.from_user.id
	title_text = '✏️ Введите заголовок вашей задачи.'
	await state.set_state(TaskState.title)
	await state.update_data(user_id=user_id, status='creating')
	if isinstance(msg_or_cb, Message):
		await msg_or_cb.answer(title_text, reply_markup=kb.cancel)
	else:
		await msg_or_cb.answer()
		await msg_or_cb.message.answer(title_text, reply_markup=kb.cancel)


@router.message(F.text == '❌ Отмена')
async def cancel(msg: Message, state: FSMContext):
	current_status = await state.get_value('status', None)
	cancel_text = '🎉 Успешно отменено!'
	choose_operation_text = 'Выберите пункты ниже 👇'
	if current_status == 'creating':
		await msg.answer(cancel_text, reply_markup=ReplyKeyboardRemove())
		await msg.answer(choose_operation_text, reply_markup=kb.main)
	elif current_status == 'editing':
		task_id = await state.get_value('task_id', None)
		if task_id:
			task = await TaskManager.get(task_id)
			if task:
				await msg.answer(cancel_text, reply_markup=ReplyKeyboardRemove())
				await msg.answer(
					f'*{task.title}*\n\n{task.description}',
					reply_markup=await kb.view_task_details(task))
			else:
				await msg.answer('❌ Задача не найдена', reply_markup=ReplyKeyboardRemove())
				await msg.answer(choose_operation_text, reply_markup=kb.main)
		else:
			await msg.answer('❌ Ошибка при обнаружении задачи', reply_markup=ReplyKeyboardRemove())
			await msg.answer(choose_operation_text, reply_markup=kb.main)
	else:
		await msg.answer('❌ Нет действия чтобы отменить.', reply_markup=ReplyKeyboardRemove())
		await msg.answer(choose_operation_text, reply_markup=kb.main)
	await state.clear()


@router.message(TaskState.title, StatusFilter('creating'))
async def add_task_title(msg: Message, state: FSMContext):
	await state.update_data(title=msg.text)
	await state.set_state(TaskState.description)
	await msg.answer(
		'✏️ Введите описание задачи.',
		reply_markup=kb.cancel_empty)


@router.message(TaskState.description, StatusFilter('creating'))
async def add_task_description(msg: Message, state: FSMContext):
	user_id = msg.from_user.id
	description = msg.text if msg.text != '🗒 Оставить пустым' else ''
	title = await state.get_value('title')
	task = TaskManager(user_id, title, description)
	await task.create()
	await msg.answer('🎉 Задача добавлена', reply_markup=ReplyKeyboardRemove())
	await msg.answer('Вот ваши задачи 👇', reply_markup=await kb.get_user_tasks(user_id))
	await state.clear()


@router.callback_query(F.data.startswith('task_'))
async def view_task(cb: CallbackQuery):
	task_id = int(cb.data.split('_')[-1])
	task = await TaskManager.get(task_id)
	txt = f'*{task.title}*\n\n{task.description}'
	await cb.message.edit_text(txt, reply_markup=await kb.view_task_details(task))


@router.callback_query(F.data.startswith('change_task_status_'))
async def change_task_status(cb: CallbackQuery):
	task_id = int(cb.data.split('_')[-1])
	await TaskManager(task_id=task_id).toggle_status()
	task = await TaskManager.get(task_id)
	await cb.answer('Успешно изменено!', show_alert=True)
	await cb.message.edit_reply_markup(reply_markup=await kb.view_task_details(task))


@router.callback_query(F.data.startswith('delete_task_'))
async def delete_task(cb: CallbackQuery):
	task_id = int(cb.data.split('_')[-1])
	await cb.message.edit_text(
		'Вы точно хотите удалить эту задачу?',
		reply_markup=await kb.delete_task_confirmation(task_id))


@router.callback_query(F.data.startswith('delete_confirm_'))
async def delete_task_confirm(cb: CallbackQuery):
	task_id = int(cb.data.split('_')[-1])
	await TaskManager(task_id=task_id).delete()
	await cb.answer('Успешно удалено!', show_alert=True)
	await cb.message.edit_text('Выберите задачу 👇', reply_markup=await kb.get_user_tasks(cb.from_user.id))


@router.callback_query(F.data.startswith('edit_task_'))
async def edit_task(cb: CallbackQuery, state: FSMContext):
	task_id = int(cb.data.split('_')[-1])
	task = await TaskManager.get(task_id)
	await state.set_state(TaskState.title)
	await state.update_data(
		task_id=task.id,
		title=task.title,
		description=task.description,
		status='editing'
	)
	await cb.message.answer(
		f'Введите новую заголовку задачи 👇\nТекущее: _{task.title}_',
		reply_markup=kb.cancel_edit
	)


@router.message(TaskState.title, StatusFilter('editing'))
async def edit_task_title(msg: Message, state: FSMContext):
	if msg.text != '📌 Оставить текущее':
		await state.update_data(title=msg.text)
		data = await state.get_data()
		txt = f'Введите новое описание 👇\n\nТекущее: _{data.get('description')}_'
	else:
		data = await state.get_data()
		txt = f'Оставлен текущий заголовок\nВведите новое описание задачи.\n\nТекущее: _{data.get('description')}_'
	await msg.answer(txt, reply_markup=kb.cancel_edit_empty)
	await state.set_state(TaskState.description)


@router.message(TaskState.description, StatusFilter('editing'))
async def edit_task_description(msg: Message, state: FSMContext):
	if msg.text != '📌 Оставить текущее':
		await state.update_data(description=msg.text if msg.text != '🗒 Оставить пустым' else '')
	data = await state.get_data()
	task_id = data.get('task_id')
	task_title = data.get('title')
	task_description = data.get('description')
	task = TaskManager(None, task_title, task_description, task_id)
	await task.update()
	await msg.answer('✅ Успешно сохранено!', reply_markup=ReplyKeyboardRemove())
	await msg.answer(
		f'*{task_title}*\n\n{task_description}',
		reply_markup=await kb.view_task_details(await TaskManager.get(task_id)))
	await state.clear()
