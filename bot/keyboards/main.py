from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[[
	InlineKeyboardButton(text='📝 Мои задачи', callback_data='my_tasks'),
	InlineKeyboardButton(text='🖋 Добавить задачу', callback_data='add_task'),
]])

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
