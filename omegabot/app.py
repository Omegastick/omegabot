import logging
import os

from discord import Intents
from discord.ext.commands import Bot
from peewee import SqliteDatabase

LOG = logging.getLogger(__name__)

bot = Bot(command_prefix="*", intents=Intents.all())
db = SqliteDatabase(os.getenv("DATABASE_FILE", "omegabot.db"))


def start_bot():
    LOG.info("Starting Omegabot")

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN environment variable not set")

    bot.run(token)
