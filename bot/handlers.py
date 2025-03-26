from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import bot.db.requests as rq
import bot.functions as fn
import bot.keyboards as kb
from bot.states import Task, TaskEdit

# Main Router
router = Router()


# Command & Query handler for /start
@router.message(CommandStart())
async def start_command(msg: Message):
	await rq.create_user(msg.from_user.id)
	await fn.start(msg=msg)


@router.callback_query(F.data == 'start')
async def start_command(cb: CallbackQuery):
	await fn.start(cb=cb)


# Command & Query handler for /my_tasks
@router.message(Command('my_tasks'))
async def my_tasks_command(msg: Message):
	await fn.my_tasks(msg=msg)


@router.callback_query(F.data == 'my_tasks')
async def my_tasks_callback(cb: CallbackQuery):
	await fn.my_tasks(cb=cb)


# New Task creation
# Command & Query handler for /add_task
@router.message(Command('add_task'))
async def add_task_command(msg: Message, state: FSMContext):
	await fn.add_task(msg=msg, state=state)


@router.callback_query(F.data == 'add_task')
async def add_task_callback(cb: CallbackQuery, state: FSMContext):
	await fn.add_task(cb=cb, state=state)


# Cancel Button Handler
@router.message(F.text == '❌ Отмена')
async def cancel_task(msg: Message, state: FSMContext):
	current_state = str(await state.get_state()).split(':')[0]
	if current_state == 'Task':
		await msg.answer('🎉 Успешно отменено!', reply_markup=ReplyKeyboardRemove())
		await msg.answer('Выберите пункт ниже 👇', reply_markup=kb.main)
	else:
		data = await state.get_data()
		task = await rq.get_task(data['task_id'])
		txt = '*%s*\n\n%s' % (task.title, task.description)
		await state.clear()
		await msg.answer('🎉 Успешно отменено!', reply_markup=ReplyKeyboardRemove())
		await msg.answer(txt, reply_markup=await kb.task_view_settings(task.id))
	await state.clear()


# New task title
@router.message(Task.title)
async def add_task_title(msg: Message, state: FSMContext):
	await state.update_data(title=msg.text)
	await state.set_state(Task.description)
	await msg.answer('✏️ Введите описание задачи, отправьте точку чтобы оставить пустым.', reply_markup=kb.cancel)


# New task description
@router.message(Task.description)
async def add_task_description(msg: Message, state: FSMContext):
	await state.update_data(description=msg.text)
	data = await state.get_data()
	desc = '' if data['description'] == '.' else data['description']
	task = await rq.create_task(data['title'], desc, data['user_id'])
	await msg.answer('🎉 Задача добавлена', reply_markup=ReplyKeyboardRemove())
	await msg.answer('Вот ваши задачи 👇', reply_markup=await kb.get_user_tasks(msg.from_user.id))
	await state.clear()


# View Task
@router.callback_query(F.data.startswith('task_'))
async def view_task(cb: CallbackQuery):
	task_id = int(cb.data.split('_')[1])
	task = await rq.get_task(task_id)
	txt = '*%s*\n\n%s' % (task.title, task.description)
	await cb.message.edit_text(txt, reply_markup=await kb.task_view_settings(task_id))


# Change task status
@router.callback_query(F.data.startswith('change_task_status_'))
async def change_task_status(cb: CallbackQuery):
	task_id = int(cb.data.split('_')[-1])
	await rq.change_task_stat(task_id)
	await cb.answer('Успешно изменено!', show_alert=True)
	await cb.message.edit_reply_markup(reply_markup=await kb.task_view_settings(task_id))


# Delete task request
@router.callback_query(F.data.startswith('delete_task_'))
async def delete_task(cb: CallbackQuery):
	task_id = int(cb.data.split('_')[-1])
	await cb.message.edit_text('Вы точно хотите удалить эту задачу?',
	                           reply_markup=await kb.delete_task_confirmation(task_id))


# Delete task confirmation
@router.callback_query(F.data.startswith('delete_confirm_'))
async def delete_task_confirm(cb: CallbackQuery):
	task_id = int(cb.data.split('_')[-1])
	await rq.delete_task(task_id)
	await cb.answer('Успешно удалено!', show_alert=True)
	await cb.message.edit_text('Выберите задачу 👇', reply_markup=await kb.get_user_tasks(cb.from_user.id))


# Edit task
@router.callback_query(F.data.startswith('edit_task_'))
async def edit_task(cb: CallbackQuery, state: FSMContext):
	task_id = int(cb.data.split('_')[-1])
	task = await rq.get_task(task_id)
	await state.set_state(TaskEdit.title)
	await state.update_data(task_id=task.id, title=task.title, description=task.description)
	await cb.message.answer(
		f'Введите новую заголовку задачи 👇\nТекущее: _{task.title}_',
		reply_markup=kb.cancel_edit
	)


# Edit task title
@router.message(TaskEdit.title)
async def edit_task_title(msg: Message, state: FSMContext):
	if msg.text != '📌 Оставить текущее':
		await state.update_data(title=msg.text)
		data = await state.get_data()
		txt = f'Введите новое описание 👇\n\nТекущее: _{await data['description']}_'
	else:
		txt = 'Оставлен текущий заголовок\nВведите новое описание задачи 👇'
	await msg.answer(txt, reply_markup=kb.cancel_edit)
	await state.set_state(TaskEdit.description)


# Edit task description
@router.message(TaskEdit.description)
async def edit_task_description(msg: Message, state: FSMContext):
	if msg.text != '📌 Оставить текущее':
		if msg.text == '.':
			await state.update_data(description='')
		else:
			await state.update_data(description=msg.text)
	data = await state.get_data()
	await rq.update_task(data['task_id'], data['title'], data['description'])
	task = await rq.get_task(data['task_id'])
	txt = '*%s*\n\n%s' % (task.title, task.description)
	await msg.answer('✅ Успешно сохранено!', reply_markup=ReplyKeyboardRemove())
	await msg.answer(txt, reply_markup=await kb.task_view_settings(task.id))
	await state.clear()
