import logging
from typing import Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import bot.db.requests as rq
import bot.keyboards as kb
from bot.filters import StatusFilter
from bot.states import Task as TaskState

router = Router()


async def my_tasks(msg_or_cb: Union[Message, CallbackQuery]):
	user_id = msg_or_cb.from_user.id
	task_text = 'Вот ваши задачи 👇'
	if isinstance(msg_or_cb, Message):
		await msg_or_cb.answer(task_text, reply_markup=await kb.get_user_tasks(user_id))
	else:
		await msg_or_cb.message.edit_text(task_text, reply_markup=await kb.get_user_tasks(user_id))


async def add_task(msg_or_cb: Union[Message, CallbackQuery], state: FSMContext):
	user_id = msg_or_cb.from_user.id
	title_text = '✏️ Введите заголовок вашей задачи.'
	await state.set_state(TaskState.title)
	await state.update_data(user_id=user_id, status='creating')
	if isinstance(msg_or_cb, Message):
		await msg_or_cb.answer(title_text, reply_markup=kb.cancel)
	else:
		await msg_or_cb.answer()
		await msg_or_cb.message.answer(title_text, reply_markup=kb.cancel)


@router.message(Command('my_tasks'))
async def my_tasks_command(msg: Message):
	await my_tasks(msg)


@router.callback_query(F.data == 'my_tasks')
async def my_tasks_callback(cb: CallbackQuery):
	await my_tasks(cb)


@router.message(Command('add_task'))
async def add_task_command(msg: Message, state: FSMContext):
	await add_task(msg, state)


@router.callback_query(F.data == 'add_task')
async def add_task_callback(cb: CallbackQuery, state: FSMContext):
	await add_task(cb, state)


@router.message(F.text == '❌ Отмена')
async def cancel_task(msg: Message, state: FSMContext):
	current_status = await state.get_value('status', None)
	cancel_text = '🎉 Успешно отменено!'
	choose_operation_text = 'Выберите пункты ниже 👇'

	if current_status == 'creating':
		await msg.answer(cancel_text, reply_markup=ReplyKeyboardRemove())
		await msg.answer(choose_operation_text, reply_markup=kb.main)

	elif current_status == 'editing':
		task_id = await state.get_value('task_id', None)

		if task_id:
			task = await rq.get_task(task_id)

			if task:
				await msg.answer(cancel_text, reply_markup=ReplyKeyboardRemove())
				await msg.answer(
					f'_{task.title}_\n\n{task.description}',
					reply_markup=await kb.task_view_settings(task.id))
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
	await msg.answer('✏️ Введите описание задачи, отправьте точку чтобы оставить пустым.', reply_markup=kb.cancel)


@router.message(TaskState.description, StatusFilter('creating'))
async def add_task_description(msg: Message, state: FSMContext):
	await state.update_data(description=msg.text)
	data = await state.get_data()
	user_id = msg.from_user.id
	desc = '' if data.get('description', '.') == '.' else data['description']
	try:
		task = await rq.create_task(data.get('title'), desc, user_id)
		await msg.answer('🎉 Задача добавлена', reply_markup=ReplyKeyboardRemove())
		await msg.answer('Вот ваши задачи 👇', reply_markup=await kb.get_user_tasks(user_id))
	except Exception as e:
		logging.error(f'An error occurred while creating task: {e}')
		await msg.answer(
			'❌ Ошибка при создании задачи.\nПожалуйста, попробуйте ещё раз или через некоторое время.',
			reply_markup=kb.main)
	await state.clear()


@router.callback_query(F.data.startswith('task_'))
async def view_task(cb: CallbackQuery):
	try:
		task_id = int(cb.data.split('_')[-1])
		task = await rq.get_task(task_id)
		txt = f'*{task.title}*\n\n{task.description}'
		await cb.message.edit_text(txt, reply_markup=await kb.task_view_settings(task_id))
	except Exception as e:
		logging.error(e)
		await cb.message.edit_text('❌ Ошибка при получении данных о задаче', reply_markup=kb.main)


@router.callback_query(F.data.startswith('change_task_status_'))
async def change_task_status(cb: CallbackQuery):
	try:
		task_id = int(cb.data.split('_')[-1])
		await rq.change_task_stat(task_id)
		await cb.answer('Успешно изменено!', show_alert=True)
		await cb.message.edit_reply_markup(reply_markup=await kb.task_view_settings(task_id))
	except Exception as e:
		logging.error(e)
		await cb.answer('❌  Ошибка при изменении статуса задачи', show_alert=True)


@router.callback_query(F.data.startswith('delete_task_'))
async def delete_task(cb: CallbackQuery):
	try:
		task_id = int(cb.data.split('_')[-1])
		await cb.message.edit_text(
			'Вы точно хотите удалить эту задачу?',
			reply_markup=await kb.delete_task_confirmation(task_id))
	except Exception as e:
		logging.error(e)
		await cb.answer('❌ Ошибка при удалении', show_alert=True)


@router.callback_query(F.data.startswith('delete_confirm_'))
async def delete_task_confirm(cb: CallbackQuery):
	try:
		task_id = int(cb.data.split('_')[-1])
		await rq.delete_task(task_id)
		await cb.answer('Успешно удалено!', show_alert=True)
		await cb.message.edit_text('Выберите задачу 👇', reply_markup=await kb.get_user_tasks(cb.from_user.id))
	except Exception as e:
		logging.error(e)
		await cb.answer('Ошибка при удалении', show_alert=True)


@router.callback_query(F.data.startswith('edit_task_'))
async def edit_task(cb: CallbackQuery, state: FSMContext):
	try:
		task_id = int(cb.data.split('_')[-1])
		task = await rq.get_task(task_id)
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
	except Exception as e:
		logging.error(e)
		await cb.answer('❌ Ошибка при получении данных о задаче', show_alert=True)


@router.message(TaskState.title, StatusFilter('editing'))
async def edit_task_title(msg: Message, state: FSMContext):
	if msg.text != '📌 Оставить текущее':
		await state.update_data(title=msg.text)
		data = await state.get_data()
		txt = f'Введите новое описание 👇\n\nТекущее: _{data.get('description')}_'
	else:
		txt = 'Оставлен текущий заголовок\nВведите новое описание задачи или отправьте точку чтобы оставить пустым.'
	await msg.answer(txt, reply_markup=kb.cancel_edit)
	await state.set_state(TaskState.description)


@router.message(TaskState.description, StatusFilter('editing'))
async def edit_task_description(msg: Message, state: FSMContext):
	try:
		if msg.text != '📌 Оставить текущее':
			await state.update_data(description=msg.text if msg.text != '.' else '')
		data = await state.get_data()
		task_id = data.get('task_id')
		task_title = data.get('title')
		task_description = data.get('description')
		await rq.update_task(task_id, task_title, task_description)
		await msg.answer('✅ Успешно сохранено!', reply_markup=ReplyKeyboardRemove())
		await msg.answer(
			f'*{task_title}*\n\n{task_description}',
			reply_markup=await kb.task_view_settings(task_id))
		await state.clear()
	except Exception as e:
		logging.error(e)
		await msg.answer(
			'❌ Ошибка при сохранении изменений.\nПожалуйста, попробуйте ещё раз или через некоторое время.',
			reply_markup=kb.main)
