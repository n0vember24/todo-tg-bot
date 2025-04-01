import os

from dotenv import load_dotenv

load_dotenv()

# Getting necessary variables from .env file
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite+aiosqlite:///bot/db/db.sqlite3')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1')
ADMINS = tuple(map(int, os.getenv('ADMINS', '0').strip().split(',')))

# Checking variables' values
if not BOT_TOKEN:
	raise ValueError("BOT_TOKEN environment variable not set, please set it in .env file")
