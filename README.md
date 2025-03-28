# ToDo Bot - Open Source Telegram bot project

## Usage

* Clone this repository into your local machine.

```bash
git clone https://github.com/n0vember24/todo-tg-bot
```

* Create local virtual environment by using your favourite one (in my case it is `virtualenv`) and activate it.

```bash
# Unix systems:
python3 -m virtualenv .venv
source .venv/bin/activate

# Windows systems:
python -m virtualenv .venv
.venv\Scripts\activate
```

* Install all required dependencies

```bash
pip install -r requirements.txt
```

* Then, create new .env file and set all necessary variables there

```python
# How it should look like:

BOT_TOKEN = 'your-bot-token'  # REQUIRED!

# If you do not set, it will automatically create local sqlite database in bot/db folder
DB_ENGINE = 'your-async-db-engine'

# Set false before deploying
DEBUG = True
```

* Finally, run the bot by typing

```bash
python3 run.py 
```

## Info

> This is my first real telegram bot, `aiogram` library has been used for production.
> Also check [TODO](TODO.md) to find out about future plans and what was done since today.
