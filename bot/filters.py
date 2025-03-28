from typing import Literal

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class StatusFilter(BaseFilter):
	def __init__(self, status: Literal['creating', 'editing']):
		self.status = status

	async def __call__(self, msg: Message, state: FSMContext):
		data = await state.get_data()
		return data.get('status') == self.status
