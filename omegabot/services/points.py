import logging
from typing import Optional

from discord import Guild, Member
from discord import Role as DiscordRole
from omegabot.models import User
from omegabot.models.point_leader_role import PointLeaderRole
from omegabot.services.history import log_points_change

LOG = logging.getLogger(__name__)


def add_points(command_user: User, target_user: User, points: int) -> User:
    LOG.info(f"Giving {target_user.name} {points}")
    log_points_change(command_user, target_user, points)
    target_user.points += points
    target_user.save()
    return target_user


async def recalculate_leader(guild: Guild) -> User:
    new_leader: User = User.select().where(User.guild_id == guild.id).order_by(User.points.desc()).get()

    role: Optional[PointLeaderRole] = PointLeaderRole.get_or_none(PointLeaderRole.guild_id == guild.id)
    if not role:
        return new_leader

    discord_role: Optional[DiscordRole] = guild.get_role(role.role_id)
    if not discord_role:
        LOG.info(f"Point leader role no longer exists in guild {guild.name}")
        role.delete_instance()
        return new_leader

    for member in guild.members:
        if discord_role in member.roles:
            await member.remove_roles(discord_role)

    new_leader_discord_member: Member = guild.get_member(new_leader.discord_id)
    await new_leader_discord_member.add_roles(discord_role)

    return new_leader


def set_point_leader_role(role: DiscordRole):
    PointLeaderRole.replace(guild_id=role.guild.id, role_id=role.id).execute()
