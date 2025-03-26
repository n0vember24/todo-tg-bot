# Required variables
___
## Set them in the `.env` file
* BOT_TOKEN = Token of the telegram bot
* DB_ENGINE = Database engine (PostgreSQL, SQLite and etc.)
# Run:
___
Run `python3 main.py` in order to run the bot, if you have no any database engine, set variable `DB_ENGINE` with `sqlite+aiosqlite:///db.sqlite3`, it will automatically create local sqlite database file.