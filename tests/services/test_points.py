from unittest.mock import MagicMock, patch

import pytest
from discord import Guild
from omegabot.models import User
from omegabot.services.history import log_points_change
from omegabot.services.points import add_points

COMMAND_USER_ID = 123
COMMAND_USERNAME = "COMMAND_USER"
TARGET_USER_ID = 234
TARGET_USERNAME = "TARGET_USER"
GUILD_ID = 345
POINTS_COUNT = 10


@pytest.fixture
def command_user():
    user = User.create(discord_id=COMMAND_USER_ID, guild_id=GUILD_ID, name=COMMAND_USERNAME)
    user.save()
    return user


@pytest.fixture
def target_user():
    user = User.create(discord_id=TARGET_USER_ID, guild_id=GUILD_ID, name=TARGET_USERNAME)
    user.save()
    return user


@pytest.fixture
def target_user_in_other_guild():
    user = User.create(discord_id=TARGET_USER_ID, guild_id=GUILD_ID + 1, name=TARGET_USERNAME)
    user.save()
    return user


@pytest.fixture
def guild() -> Guild:
    return Guild(state=MagicMock(), data={"id": GUILD_ID})


def test_add_points_adds_points_to_correct_user(command_user: User, target_user: User, guild: Guild):
    add_points(command_user, target_user, guild, POINTS_COUNT)
    target_user = User.get(User.id == target_user.id)
    assert target_user.points == POINTS_COUNT


def test_add_points_adds_correct_amount_of_points(command_user: User, target_user: User, guild: Guild):
    target_user.points = 100
    target_user = add_points(command_user, target_user, guild, POINTS_COUNT)
    assert target_user.points == 110


def test_add_points_only_adds_points_to_correct_guild(
    command_user: User, target_user: User, target_user_in_other_guild: User
):
    target_user = add_points(command_user, target_user, guild, POINTS_COUNT)
    target_user_in_other_guild = User.get_by_id(target_user_in_other_guild.id)

    assert target_user.points != target_user_in_other_guild.points


@patch("omegabot.services.points.log_points_change", spec=log_points_change)
def test_add_points_logs_change(mock_log_points_change: MagicMock, command_user: User, target_user: User, guild: Guild):
    add_points(command_user, target_user, guild, POINTS_COUNT)
    mock_log_points_change.assert_called_once_with(command_user, target_user, POINTS_COUNT)
