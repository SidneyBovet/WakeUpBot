# WakeUpBot


This bot is based on the [Telegram Bot API wrapper](https://pypi.python.org/pypi/python-telegram-bot).

### How to run the bot

First install the wrapper:
```bash
pip install python-telegram-bot --upgrade
```

Then create a `settings.json` file at the same level as the `bot.py` file, with the API token stored as follows:
```json
{
    "token": "YourApiTokenComesHere"
}
```

And then simply run:
```bash
python3 bot.py
```

The bot should now answer your commands.


### Available commands

| Command		| Effect											|
|---			|---												|
| /git			| Displays the address of the repository.			|
| /start		| Registers you if you are a new player.			|
| /arrive		| Registers your arrival time for today.			|
| /scoreboard	| Displays the scoreboard as of yesterday evening.	|
