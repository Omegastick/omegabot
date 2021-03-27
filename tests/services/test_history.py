import pytest
from omegabot.models import CommandLog, User
from omegabot.services.history import log_points_change

COMMAND_USER_ID = 123
COMMAND_USERNAME = "COMMAND_USER"
TARGET_USER_ID = 234
TARGET_USERNAME = "TARGET_USER"
GUILD_ID = 345
POINTS_COUNT = 10


@pytest.fixture
def command_user():
    user = User.create(discord_id=COMMAND_USER_ID, guild_id=GUILD_ID, name=COMMAND_USERNAME)
    return user


@pytest.fixture
def target_user():
    user = User.create(discord_id=TARGET_USER_ID, guild_id=GUILD_ID, name=TARGET_USERNAME)
    return user


def test_log_points_change_creates_one_log(command_user: User, target_user: User):
    log_points_change(command_user, target_user, POINTS_COUNT)
    assert CommandLog.select().count() == 1


def test_log_points_change_logs_correct_information(command_user: User, target_user: User):
    log_points_change(command_user, target_user, POINTS_COUNT)

    log: User = CommandLog.select().first()
    assert log.command_user == command_user
    assert log.target_user == target_user
    assert log.points == POINTS_COUNT
