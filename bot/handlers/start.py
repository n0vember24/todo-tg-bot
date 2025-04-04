from typing import Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import bot.keyboards as kb
from bot.db.requests import UserManager

router = Router()


@router.message(Command('start'))
@router.callback_query(F.data == 'start')
async def start(msg_or_cb: Union[Message, CallbackQuery]):
	start_text = f'Добро пожаловать, _{msg_or_cb.from_user.full_name}_!\n\n\
Я готов служить вам как ваш личный помощник в планировке задач и выполнения ваших целей!\n\n\
Для начала работы выберите пункты ниже 👇'
	if isinstance(msg_or_cb, Message):
		user = UserManager(msg_or_cb.from_user.id)
		await user.create()
		await msg_or_cb.answer(
			start_text, reply_markup=await kb.main(msg_or_cb.from_user.id))
	else:
		await msg_or_cb.message.edit_text(
			'Выберите пункты ниже 👇', reply_markup=await kb.main(msg_or_cb.from_user.id))
