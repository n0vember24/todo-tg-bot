import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN, DEBUG
from bot.db.models import async_main
from bot.handlers import start_router, tasks_router, admin_router
from bot.middlewares import ErrorHandler


# Main function
async def start_bot():
	"""Main function to start the bot"""
	await async_main()
	bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='markdown'))
	dp = Dispatcher()
	dp.include_routers(start_router, tasks_router, admin_router)
	dp.message.middleware(ErrorHandler())
	await dp.start_polling(bot)


# Running the bot
if __name__ == '__main__':
	try:
		if DEBUG:
			logging.basicConfig(level=logging.INFO)
			logging.basicConfig(level=logging.DEBUG)
		else:
			logging.basicConfig(level=logging.WARNING)
		asyncio.run(start_bot())
	except KeyboardInterrupt:
		print('Shutdown')
	except Exception as e:
		logging.error('Error in running: %s', e)
