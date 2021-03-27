from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from discord import Guild
from discord import Role as DiscordRole
from discord.member import Member
from omegabot.models import PointLeaderRole, User
from omegabot.services.history import log_points_change
from omegabot.services.points import add_points, recalculate_leader, set_point_leader_role

COMMAND_USER_ID = 123
COMMAND_USERNAME = "COMMAND_USER"
TARGET_USER_ID = 234
TARGET_USERNAME = "TARGET_USER"
GUILD_ID = 345
GUILD_NAME = "GUILD"
POINTS_COUNT = 10
OLD_POINT_LEADER_POINTS = 100
OLD_POINT_LEADER_ID = 456
OLD_POINT_LEADER_NAME = "OLD_POINT_LEADER"
ROLE_ID = 567
ROLE_NAME = "ROLE"


@pytest.fixture
def command_user() -> User:
    return User.create(discord_id=COMMAND_USER_ID, guild_id=GUILD_ID, name=COMMAND_USERNAME)


@pytest.fixture
def target_user() -> User:
    return User.create(discord_id=TARGET_USER_ID, guild_id=GUILD_ID, name=TARGET_USERNAME)


@pytest.fixture
def target_user_in_other_guild() -> User:
    return User.create(discord_id=TARGET_USER_ID, guild_id=GUILD_ID + 1, name=TARGET_USERNAME)


@pytest.fixture
def old_point_leader() -> User:
    return User.create(
        discord_id=OLD_POINT_LEADER_ID, guild_id=GUILD_ID, name=OLD_POINT_LEADER_NAME, points=OLD_POINT_LEADER_POINTS
    )


@pytest.fixture
def guild() -> Guild:
    return Guild(state=MagicMock(), data={"id": GUILD_ID, "name": GUILD_NAME})


@pytest.fixture
def leader_role() -> PointLeaderRole:
    return PointLeaderRole.create(role_id=ROLE_ID, guild_id=GUILD_ID)


@pytest.fixture
def discord_role(guild) -> DiscordRole:
    return DiscordRole(guild=guild, state=MagicMock(), data={"id": ROLE_ID, "name": ROLE_NAME})


def test_add_points_adds_points_to_correct_user(command_user: User, target_user: User, guild: Guild):
    add_points(command_user, target_user, guild, POINTS_COUNT)
    target_user = User.get(User.id == target_user.id)
    assert target_user.points == POINTS_COUNT


def test_add_points_adds_correct_amount_of_points(command_user: User, target_user: User, guild: Guild):
    target_user.points = 100
    target_user = add_points(command_user, target_user, guild, POINTS_COUNT)
    assert target_user.points == 100 + POINTS_COUNT


def test_add_points_only_adds_points_to_correct_guild(
    command_user: User, target_user: User, target_user_in_other_guild: User, guild: Guild
):
    target_user = add_points(command_user, target_user, guild, POINTS_COUNT)
    target_user_in_other_guild = User.get_by_id(target_user_in_other_guild.id)

    assert target_user.points != target_user_in_other_guild.points


@patch("omegabot.services.points.log_points_change", spec=log_points_change)
def test_add_points_logs_change(mock_log_points_change: MagicMock, command_user: User, target_user: User, guild: Guild):
    add_points(command_user, target_user, guild, POINTS_COUNT)
    mock_log_points_change.assert_called_once_with(command_user, target_user, POINTS_COUNT)


@pytest.mark.asyncio
async def test_recalculate_leader_returns_new_highest_points_user(
    target_user: User, old_point_leader: User, guild: Guild
):
    target_user.points = OLD_POINT_LEADER_POINTS + 1
    target_user.save()

    new_leader = await recalculate_leader(guild)

    assert new_leader == target_user


@pytest.mark.asyncio
async def test_recalculate_leader_reassigns_roles(
    target_user: User, old_point_leader: User, leader_role: PointLeaderRole
):
    target_user.points = OLD_POINT_LEADER_POINTS + 1
    target_user.save()

    discord_role = MagicMock()
    old_leader_member = AsyncMock(roles=[discord_role], spec=Member)
    new_leader_member = AsyncMock(roles=[], spec=Member)
    guild = AsyncMock(id=GUILD_ID, spec=Guild)
    guild.get_member.return_value = new_leader_member
    guild.members = [new_leader_member, old_leader_member]
    guild.get_role.return_value = discord_role
    await recalculate_leader(guild)

    new_leader_member.add_roles.assert_called_with(discord_role)
    old_leader_member.remove_roles.assert_called_with(discord_role)


def test_set_point_leader_role_creates_new_role_if_none_exists(discord_role: DiscordRole, guild: Guild):
    set_point_leader_role(discord_role)

    created_role: PointLeaderRole = PointLeaderRole.get(PointLeaderRole.guild_id == guild.id)
    assert created_role.guild_id == guild.id
    assert created_role.role_id == discord_role.id


def test_set_point_leader_role_replaces_old_role_if_one_exists(
    discord_role: DiscordRole, guild: Guild, leader_role: PointLeaderRole
):
    discord_role.id = ROLE_ID + 1
    set_point_leader_role(discord_role)

    assert PointLeaderRole.select().count() == 1
    role = PointLeaderRole.get(PointLeaderRole.guild_id == guild.id)
    assert role.role_id == discord_role.id
