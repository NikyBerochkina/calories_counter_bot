import os
import sys

from dotenv import load_dotenv

load_dotenv()

try:
    BOT_TOKEN = os.environ["BOT_TOKEN"]
except KeyError:
    sys.exit("BOT_TOKEN is not set. Copy .env.example to .env and add your token.")

DB_PATH = os.environ.get("DB_PATH", "calories.db")
