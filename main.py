import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from bot.db.models import async_main
from bot.handlers import router

# Set False at the production
DEBUG = True


# Main function
async def main():
	load_dotenv()
	await async_main()
	bot = Bot(getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode='markdown'))
	dp = Dispatcher()
	dp.include_router(router)
	await dp.start_polling(bot)


# Running the bot
if __name__ == '__main__':
	try:
		if DEBUG:
			logging.basicConfig(level=logging.INFO)
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Shutdown')
