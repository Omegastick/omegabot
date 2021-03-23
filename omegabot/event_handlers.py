import logging

from omegabot.app import bot

LOG = logging.getLogger(__name__)


@bot.event
async def on_ready():
    LOG.info("Connected to Discord")
    LOG.info(f"Connected to guilds: {[guild.name for guild in bot.guilds]}")
    LOG.info(f"Bot name: {bot.user.name}")
