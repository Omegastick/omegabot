from typing import List
from unittest.mock import MagicMock

import pytest
from discord import Guild
from discord import User as DiscordUser
from omegabot.models import User
from omegabot.services.user import get_leaderboard_users, get_or_create_user, get_xp_leaderboard_users

USERNAME = "TEST_USERNAME"
USER_ID = 123
GUILD_ID = 234
NO_POINTS = 0
LOTS_OF_POINTS = 345


@pytest.fixture
def database_user() -> User:
    user = User.create(discord_id=USER_ID, guild_id=GUILD_ID, name=USERNAME, points=LOTS_OF_POINTS)
    return user


@pytest.fixture
def database_user_list() -> List[User]:
    users = []
    for i in range(10):
        users.append(User.create(discord_id=USER_ID + i, guild_id=GUILD_ID, name="Guild 1 User", points=i, xp=i))
    for i in range(10):
        users.append(User.create(discord_id=USER_ID + i, guild_id=GUILD_ID + 1, name="Guild 2 User", points=i, xp=i))
    return users


@pytest.fixture
def discord_user() -> DiscordUser:
    return DiscordUser(
        state=MagicMock(),
        data={
            "username": USERNAME,
            "id": USER_ID,
            "discriminator": "TEST_DISCRIMINATOR",
            "avatar": None,
            "bot": False,
            "system": False,
        },
    )


@pytest.fixture
def guild() -> Guild:
    return Guild(state=MagicMock(), data={"id": GUILD_ID})


def test_get_or_create_user_user_creates_user(discord_user: DiscordUser, guild: Guild):
    created_user = get_or_create_user(discord_user, guild)

    assert User.select().count() == 1
    assert created_user.discord_id == discord_user.id
    assert created_user.guild_id == guild.id
    assert created_user.name == discord_user.name
    assert created_user.points == NO_POINTS


def test_get_or_create_user_user_gets_user(discord_user: DiscordUser, guild: Guild, database_user: User):
    got_user = get_or_create_user(discord_user, guild)

    assert got_user.discord_id == discord_user.id
    assert got_user.guild_id == guild.id
    assert got_user.name == discord_user.name
    assert got_user.points == LOTS_OF_POINTS


def test_get_or_create_user_updates_username(discord_user: DiscordUser, guild: Guild, database_user: User):
    discord_user.name = "CHANGED_USERNAME"
    updated_user = get_or_create_user(discord_user, guild)

    assert updated_user.name == discord_user.name


def test_get_or_create_user_creates_new_user_for_each_guild(discord_user: DiscordUser, guild: Guild):
    user_1 = get_or_create_user(discord_user, guild)
    guild.id += 1
    user_2 = get_or_create_user(discord_user, guild)

    assert user_1.guild_id == user_2.guild_id - 1


def test_get_leaderboard_users_returns_users_from_correct_guild(guild: Guild, database_user_list: List[User]):
    users = get_leaderboard_users(guild)

    for user in users:
        assert user.guild_id == guild.id


def test_get_leaderboard_users_returns_users_in_points_order(guild: Guild, database_user_list: List[User]):
    users = get_leaderboard_users(guild)

    last_points = float("INFINITY")
    for user in users:
        assert user.points <= last_points
        last_points = user.points


def test_get_leaderboard_users_returns_all_users_in_guild(guild: Guild, database_user_list: List[User]):
    users = get_leaderboard_users(guild)

    assert len(users) == 10


def test_get_xp_leaderboard_users_returns_users_from_correct_guild(guild: Guild, database_user_list: List[User]):
    users = get_xp_leaderboard_users(guild)

    for user in users:
        assert user.guild_id == guild.id


def test_get_xp_leaderboard_users_returns_users_in_points_order(guild: Guild, database_user_list: List[User]):
    users = get_xp_leaderboard_users(guild)

    last_xp = float("INFINITY")
    for user in users:
        assert user.xp <= last_xp
        last_xp = user.xp


def test_get_xp_leaderboard_users_returns_all_users_in_guild(guild: Guild, database_user_list: List[User]):
    users = get_xp_leaderboard_users(guild)

    assert len(users) == 10
