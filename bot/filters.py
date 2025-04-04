from typing import Literal, Optional

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import ADMINS


class StatusFilter(BaseFilter):
	"""Filters the status of the task state. Used to create or update the task"""

	def __init__(self, status: Literal['creating', 'editing']):
		self.status = status

	async def __call__(self, msg: Message, state: FSMContext):
		data = await state.get_data()
		return data.get('status') == self.status


class IsBotAdmin(BaseFilter):
	"""Checks if user is admin or not"""

	def __init__(self, user_id: Optional[int]=None):
		self.user_id = user_id

	async def __call__(self, msg: Message):
		if self.user_id:
			return self.user_id in ADMINS
		return msg.from_user.id in ADMINS
