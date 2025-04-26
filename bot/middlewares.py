import logging
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Update, CallbackQuery


class ErrorHandler(BaseMiddleware):
	"""
	Middleware for all updates(Message/Callback).
	Automatically check for error and keep running the bot
	"""

	async def __call__(
			self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
			event: Update, data: Dict[str, Any]
	) -> Any:
		try:
			return await handler(event, data)
		except Exception as e:
			logging.error('Error in %s: %s', event, e, exc_info=True)
			state: FSMContext = data.get('state')
			if state:
				await state.clear()
			if isinstance(event, Message):
				await event.answer('❌ Ошибка. Пожалуйства, повторите попытку ещё раз или позже.')
			elif isinstance(event, CallbackQuery):
				await event.message.answer('❌ Ошибка. Пожалуйства, повторите попытку ещё раз или позже.')
