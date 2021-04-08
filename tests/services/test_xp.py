from datetime import timedelta

import pytest
from omegabot.models import User
from omegabot.services.xp import add_xp, level_to_xp, xp_to_level

USER_ID = 123
USERNAME = "TEST_USERNAME"
GUILD_ID = 234
XP_COUNT = 10


@pytest.fixture
def user() -> User:
    return User.create(discord_id=USER_ID, guild_id=GUILD_ID, name=USERNAME)


@pytest.fixture
def user_in_other_guild() -> User:
    return User.create(discord_id=USER_ID, guild_id=GUILD_ID + 1, name=USERNAME)


def test_add_xp_adds_xp_to_correct_user(user: User):
    add_xp(user, XP_COUNT, cooldown=timedelta(0))
    user = User.get_by_id(user.id)
    assert user.xp == XP_COUNT


def test_add_xp_adds_correct_amount_of_xp(user: User):
    user.xp = 100
    user = add_xp(user, XP_COUNT, cooldown=timedelta(0))
    assert user.xp == 100 + XP_COUNT


def test_add_xp_only_adds_xp_to_correct_guild(user: User, user_in_other_guild: User):
    user = add_xp(user, XP_COUNT, cooldown=timedelta(0))
    user_in_other_guild = User.get_by_id(user_in_other_guild.id)

    assert user.xp != user_in_other_guild.xp


def test_add_xp_sets_user_new_xp_update_time(user: User):
    old_update_time = user.xp_last_update_time
    user = add_xp(user, XP_COUNT, cooldown=timedelta(0))

    assert user.xp_last_update_time > old_update_time


def test_add_xp_respects_cooldown(user: User):
    user = add_xp(user, XP_COUNT, cooldown=timedelta(days=1))

    assert user.xp == User.xp.default


def test_xp_to_level_returns_expected_values():
    assert xp_to_level(0) == 1
    assert xp_to_level(5) == 1
    assert xp_to_level(10) == 2
    assert xp_to_level(20) == 2
    assert xp_to_level(30) == 3
    assert xp_to_level(35) == 3
    assert xp_to_level(60) == 4


def test_level_to_xp_returns_expected_values():
    assert level_to_xp(1) == 0
    assert level_to_xp(2) == 10
    assert level_to_xp(3) == 30
    assert level_to_xp(4) == 60
