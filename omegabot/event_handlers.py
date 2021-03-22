import logging

from omegabot.app import bot
from omegabot.models.user import User

LOG = logging.getLogger(__name__)


@bot.event
async def on_ready():
    LOG.info("Connected to Discord")
    LOG.info(f"Connected to guilds: {[guild.name for guild in bot.guilds]}")
    LOG.info(f"User: {bot.user.name}")

    for guild in bot.guilds:
        LOG.info(f"Adding members for {guild.name}")
        for member in guild.members:
            if not User.select().where(User.id == member.id).exists():
                LOG.info(f"Adding user {member.name}")
                User.create(id=member.id).save()
    LOG.info("Finished adding members for all guilds")
