import logging

from discord import Message

from omegabot.app import bot

LOG = logging.getLogger(__name__)


@bot.event
async def on_ready():
    LOG.info("Connected to Discord")
    LOG.info(f"Connected to guilds: {[guild.name for guild in bot.guilds]}")
    LOG.info(f"Bot name: {bot.user.name}")


@bot.event
async def on_message(message: Message):
    if message.author.id == 136999062519021568:
        await message.channel.send("I am beyond your commands")
        return

    await bot.process_commands(message)
