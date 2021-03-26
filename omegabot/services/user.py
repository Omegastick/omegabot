import logging
from typing import List

from discord import Guild
from discord import User as DiscordUser
from omegabot.models import User

LOG = logging.getLogger(__name__)


def get_or_create_user(discord_user: DiscordUser, guild: Guild) -> User:
    user, created = User.get_or_create(
        discord_id=discord_user.id, guild_id=guild.id, defaults={"name": discord_user.name}
    )
    if created:
        LOG.info(f"Creating user {discord_user.name}")
    if user.name != discord_user.name:
        LOG.info(f"Changing name for user {user.name} to {discord_user.name}")
        user.name = discord_user.name
        user.save()
    return user


def get_leaderboard_users(guild: Guild) -> List[User]:
    return User.select().where(User.guild_id == guild.id).order_by(User.points.desc())
