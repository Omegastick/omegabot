from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock

import pytest
from discord import Guild
from discord import Member as DiscordMember
from discord import Role as DiscordRole
from omegabot.models import RegularRole, User
from omegabot.services.regular import check_and_apply_regular_role, set_regular_role

ROLE_ID = 123
ROLE_NAME = "ROLE"
GUILD_ID = 234
GUILD_NAME = "GUILD"
APPLY_DELAY = 345
USER_ID = 456
USERNAME = "USER"


@pytest.fixture
def guild() -> Guild:
    return Guild(state=MagicMock(), data={"id": GUILD_ID, "name": GUILD_NAME})


@pytest.fixture
def regular_role() -> RegularRole:
    return RegularRole.create(role_id=ROLE_ID, guild_id=GUILD_ID, apply_delay=APPLY_DELAY)


@pytest.fixture
def discord_role(guild) -> DiscordRole:
    return DiscordRole(guild=guild, state=MagicMock(), data={"id": ROLE_ID, "name": ROLE_NAME})


@pytest.fixture
def user() -> User:
    return User.create(discord_id=USER_ID, guild_id=GUILD_ID, name=USERNAME)


@pytest.fixture
def discord_member(discord_role) -> DiscordMember:
    discord_member = MagicMock(spec=DiscordMember)
    discord_member.guild.get_role.return_value = discord_role
    discord_member.joined_at = datetime.utcnow() - timedelta(days=APPLY_DELAY + 1)
    return discord_member


def test_set_regular_role_creates_new_role_if_none_exists(discord_role: DiscordRole, guild: Guild):
    set_regular_role(discord_role, APPLY_DELAY)

    created_role: RegularRole = RegularRole.get(RegularRole.guild_id == guild.id)
    assert created_role.guild_id == guild.id
    assert created_role.role_id == discord_role.id
    assert created_role.apply_delay == APPLY_DELAY


def test_set_regular_role_replaces_old_role_if_one_exists(
    discord_role: DiscordRole, guild: Guild, regular_role: RegularRole
):
    discord_role.id = ROLE_ID + 1
    set_regular_role(discord_role, APPLY_DELAY)

    assert RegularRole.select().count() == 1
    role = RegularRole.get(RegularRole.guild_id == guild.id)
    assert role.role_id == discord_role.id


@pytest.mark.asyncio
async def test_check_and_apply_role_gives_role_if_applicable(
    user: User, discord_role: DiscordRole, regular_role: RegularRole, discord_member: DiscordMember
):
    await check_and_apply_regular_role(user, discord_member)

    discord_member.add_roles.assert_awaited_with(discord_role)


@pytest.mark.asyncio
async def test_check_and_apply_role_doesnt_give_role_if_not_enough_time_has_passed(
    user: User, discord_role: DiscordRole, regular_role: RegularRole, discord_member: DiscordMember
):
    discord_member.joined_at = datetime.utcnow() - timedelta(days=APPLY_DELAY - 1)

    await check_and_apply_regular_role(user, discord_member)

    discord_member.add_roles.await_count == 0


@pytest.mark.asyncio
async def test_check_and_apply_role_doesnt_give_role_if_user_already_has_role(
    user: User, discord_role: DiscordRole, regular_role: RegularRole, discord_member: DiscordMember
):
    discord_member.roles = [Mock(id=ROLE_ID)]

    await check_and_apply_regular_role(user, discord_member)

    discord_member.add_roles.await_count == 0
