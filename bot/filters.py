from typing import Literal

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
	async def __call__(self, msg: Message):
		return msg.from_user.id in ADMINS
