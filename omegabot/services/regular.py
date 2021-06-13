import logging
from datetime import datetime, timedelta

from discord import Member as DiscordMember
from discord import Role as DiscordRole
from omegabot.models import User
from omegabot.models.regular_role import RegularRole

LOG = logging.getLogger(__name__)


def set_regular_role(role: DiscordRole, apply_delay_in_days: int) -> None:
    RegularRole.replace(guild_id=role.guild.id, role_id=role.id, apply_delay=apply_delay_in_days).execute()


async def check_and_apply_regular_role(user: User, discord_member: DiscordMember) -> None:
    regular_role: RegularRole = RegularRole.get_or_none(guild_id=user.guild_id)
    if (
        not regular_role
        or any(r.id == regular_role.role_id for r in discord_member.roles)
        or discord_member.joined_at + timedelta(days=regular_role.apply_delay) > datetime.utcnow()
    ):
        return
    discord_role = discord_member.guild.get_role(regular_role.role_id)
    LOG.info(f"Giving regular role {discord_role.name} to user {user.name} in server {discord_member.guild.name}")
    await discord_member.add_roles(discord_role)
