from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, \
	ReplyKeyboardMarkup, KeyboardButton

from bot.filters import IsBotAdmin


async def main(user_id: int):
	is_admin = IsBotAdmin(user_id)
	kb = InlineKeyboardBuilder()
	kb.add(InlineKeyboardButton(text='📝 Мои задачи', callback_data='my_tasks'),
	       InlineKeyboardButton(text='🖋 Добавить задачу', callback_data='add_task'))
	if is_admin:
		kb.add(InlineKeyboardButton(text='👮‍♂️ Админ панель', callback_data='admin'))
	return kb.adjust(2).as_markup()


cancel = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='❌ Отмена')]],
	resize_keyboard=True,
	one_time_keyboard=True
)

cancel_empty = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='🗒 Оставить пустым'), KeyboardButton(text='❌ Отмена')]],
	resize_keyboard=True,
	one_time_keyboard=True
)

cancel_edit = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='📌 Оставить текущее'), KeyboardButton(text='❌ Отмена')]],
	resize_keyboard=True,
	one_time_keyboard=True
)

cancel_edit_empty = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='🗒 Оставить пустым'), KeyboardButton(text='📌 Оставить текущее')],
	[KeyboardButton(text='❌ Отмена')]],
	resize_keyboard=True,
	one_time_keyboard=True
)
