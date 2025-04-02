# ToDo Bot - Open Source Telegram bot project

[![wakatime](https://wakatime.com/badge/user/b805ecb4-4a3d-4805-815f-410bf2e510c9/project/d08980b1-043e-4231-909f-270f22fb9637.svg)](https://wakatime.com/badge/user/b805ecb4-4a3d-4805-815f-410bf2e510c9/project/d08980b1-043e-4231-909f-270f22fb9637)
[![DeepSource](https://app.deepsource.com/gh/n0vember24/todo-tg-bot.svg/?label=active+issues&show_trend=true&token=Z29lcCx2K2Spwi1iKrUKj_9-)](https://app.deepsource.com/gh/n0vember24/todo-tg-bot/)
[![DeepSource](https://app.deepsource.com/gh/n0vember24/todo-tg-bot.svg/?label=resolved+issues&show_trend=true&token=Z29lcCx2K2Spwi1iKrUKj_9-)](https://app.deepsource.com/gh/n0vember24/todo-tg-bot/)
[![CodeFactor](https://www.codefactor.io/repository/github/n0vember24/todo-tg-bot/badge)](https://www.codefactor.io/repository/github/n0vember24/todo-tg-bot)
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

* Then, create new `.env` file in root folder and set all necessary variables there

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
