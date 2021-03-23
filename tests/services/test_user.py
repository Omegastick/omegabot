from unittest.mock import MagicMock

import pytest
from discord import User as DiscordUser
from omegabot.models import User
from omegabot.services.user import get_or_create_user

USERNAME = "TEST_USERNAME"
USER_ID = 123
NO_POINTS = 0
LOTS_OF_POINTS = 234


@pytest.fixture
def database_user() -> User:
    user = User.create(id=USER_ID, name=USERNAME, points=LOTS_OF_POINTS)
    user.save()
    return user


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


def test_get_or_create_user_user_creates_user(discord_user: DiscordUser):
    created_user = get_or_create_user(discord_user)

    assert User.select().count() == 1
    assert created_user.id == discord_user.id
    assert created_user.name == discord_user.name
    assert created_user.points == NO_POINTS


def test_get_or_create_user_user_gets_user(discord_user: DiscordUser, database_user: User):
    got_user = get_or_create_user(discord_user)

    assert got_user.id == discord_user.id
    assert got_user.name == discord_user.name
    assert got_user.points == LOTS_OF_POINTS


def test_get_or_create_user_updates_username(discord_user: DiscordUser, database_user: User):
    discord_user.name = "CHANGED_USERNAME"
    updated_user = get_or_create_user(discord_user)

    assert updated_user.name == discord_user.name
