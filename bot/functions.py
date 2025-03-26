from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import bot.keyboards as kb
from bot.states import Task


# Main functions for command and callback queries
async def start_text(first_name):
	return 'Добро пожаловать, _%s_!\n\n\
	Я готов служить вам как ваш личный помощник в планировке задач и выполнения ваших целей!\n\n\
	Для начала работы выберите пункты ниже 👇' % first_name


async def start(msg: Message = None, cb: CallbackQuery = None):
	if msg:
		await msg.answer(await start_text(msg.from_user.first_name), reply_markup=kb.main)
	else:
		await cb.message.edit_text('Выберите пункты ниже 👇', reply_markup=kb.main)


async def my_tasks(msg: Message = None, cb: CallbackQuery = None):
	task_text = 'Вот ваши задачи 👇'
	if msg:
		await msg.answer(task_text, reply_markup=await kb.get_user_tasks(msg.from_user.id))
	else:
		await cb.message.edit_text(task_text, reply_markup=await kb.get_user_tasks(cb.from_user.id))


async def add_task(msg: Message = None, cb: CallbackQuery = None, state: FSMContext = None):
	await state.set_state(Task.title)
	txt = '✏️ Введите заголовок вашей задачи.'
	if msg:
		await state.update_data(user_id=msg.from_user.id)
		await msg.answer(txt, reply_markup=kb.cancel)
	else:
		await state.update_data(user_id=cb.from_user.id)
		await cb.answer()
		await cb.message.answer(txt, reply_markup=kb.cancel)
