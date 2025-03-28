import os

from dotenv import load_dotenv

load_dotenv()

# Getting necessary variables from .env file
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_ENGINE = os.getenv('DB_ENGINE')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1')

# Checking variables' values
if not BOT_TOKEN:
	raise ValueError("BOT_TOKEN environment variable not set, please set it in .env file")

if not DB_ENGINE:
	raise ValueError("DB_ENGINE environment variable not set, please set it in.env file")
