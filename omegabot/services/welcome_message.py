import logging

from discord import TextChannel
from omegabot.models.welcome_message import WelcomeMessage

LOG = logging.getLogger(__name__)


def set_welcome_message(channel: TextChannel, new_message: str):
    LOG.info(f"Setting welcome messasge for {channel.guild.name} to {new_message} in channel {channel.name}")
    message, _ = WelcomeMessage.get_or_create(
        guild_id=channel.guild.id, defaults={"message": "", "channel_id": channel.id}
    )
    message.message = new_message
    message.channel_id = channel.id
    message.save()
