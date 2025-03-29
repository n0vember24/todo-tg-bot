import logging
from typing import Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.db.requests import UserManager
import bot.keyboards as kb

router = Router()


async def start_text(first_name):
	return f'Добро пожаловать, _{first_name}_!\n\n\
Я готов служить вам как ваш личный помощник в планировке задач и выполнения ваших целей!\n\n\
Для начала работы выберите пункты ниже 👇'


async def start(msg_or_cb: Union[Message, CallbackQuery]):
	first_name = msg_or_cb.from_user.first_name
	if isinstance(msg_or_cb, Message):
		await msg_or_cb.answer(await start_text(first_name), reply_markup=kb.main)
	else:
		await msg_or_cb.message.edit_text('Выберите пункты ниже 👇', reply_markup=kb.main)


@router.message(Command('start'))
async def start_command(msg: Message):
	try:
		user = UserManager(msg.from_user.id)
		await user.create()
		await start(msg)
	except Exception as e:
		logging.error(f'An error occurred while creating user: {e}')


@router.callback_query(F.data == 'start')
async def start_callback(cb: CallbackQuery):
	await start(cb)
