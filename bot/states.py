from aiogram.fsm.state import State, StatesGroup


class Task(StatesGroup):
	title = State()
	description = State()
	user_id = State()


class TaskEdit(StatesGroup):
	task_id = State()
	title = State()
	description = State()
	user_id = State()
