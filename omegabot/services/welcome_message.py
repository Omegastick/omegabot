import logging

from discord import Guild
from omegabot.models.welcome_message import WelcomeMessage

LOG = logging.getLogger(__name__)


def set_welcome_message(guild: Guild, new_message: str):
    LOG.info(f"Setting welcome messasge for {guild.name} to {new_message}")
    message, _ = WelcomeMessage.get_or_create(guild_id=guild.id, defaults={"message": ""})
    message.message = new_message
    message.save()
