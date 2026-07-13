# Calorie Tracker Bot

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)

A Telegram bot for quick, frictionless calorie logging. Send a message like `chicken salad 350` and it's logged — no menus, no forms.

## Features

- **Free-text logging** — send calories and a description in any order (`350 chicken salad` or `chicken salad 350`)
- **Batch logging** — log several items at once, comma-separated: `250 coffee, 75 porridge`
- **Daily goals** — set a target with `/goal` and see remaining calories after every entry
- **History** — `/today` for today's log, `/week` for a 7-day summary
- **Undo** — `/undo` removes the last entry

## Tech stack

- Python 3.10+
- [aiogram 3](https://docs.aiogram.dev/) — async Telegram Bot API framework
- [aiosqlite](https://github.com/omnilib/aiosqlite) — async SQLite storage

## Quick start

```bash
git clone https://github.com/NikyBerochkina/calories_counter_bot.git
cd calories_counter_bot

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env          # then set BOT_TOKEN (get one from @BotFather)

python bot.py
```

## Commands

| Command | Description |
|---|---|
| `/start` | Register and show help |
| `/help` | Show usage help |
| `/today` | Today's entries and total |
| `/week` | Last 7 days summary |
| `/undo` | Delete your last entry |
| `/goal <calories>` | Set your daily calorie goal |

Any other message is parsed as a food log entry.

## Project structure

```
.
├── bot.py           # entry point — starts the aiogram dispatcher
├── config.py        # env-based configuration
├── database.py       # aiosqlite data access layer
├── handlers.py       # command and message handlers
└── requirements*.txt
```

## License

MIT — see [LICENSE](LICENSE).
