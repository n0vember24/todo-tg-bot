from typing import Literal

from aiogram.fsm.state import State, StatesGroup


class Task(StatesGroup):
	"""FSM State. Used to create and edit tasks"""
	task_id: int = State()
	status: Literal['creating', 'editing'] = State()
	title: str = State()
	description: str = State()
	user_id: int = State()
