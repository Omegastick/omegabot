from unittest.mock import MagicMock, patch

import pytest
from omegabot.models import User
from omegabot.services.history import log_points_change
from omegabot.services.points import add_points

COMMAND_USER_ID = 123
COMMAND_USERNAME = "COMMAND_USER"
TARGET_USER_ID = 234
TARGET_USERNAME = "TARGET_USER"
POINTS_COUNT = 10


@pytest.fixture
def command_user():
    user = User.create(id=COMMAND_USER_ID, name=COMMAND_USERNAME)
    user.save()
    return user


@pytest.fixture
def target_user():
    user = User.create(id=TARGET_USER_ID, name=TARGET_USERNAME)
    user.save()
    return user


def test_add_points_adds_points_to_correct_user(command_user: User, target_user: User):
    add_points(command_user, target_user, POINTS_COUNT)
    target_user = User.get(User.id == target_user.id)
    assert target_user.points == POINTS_COUNT


def test_add_points_adds_correct_amount_of_points(command_user: User, target_user: User):
    target_user.points = 100
    target_user = add_points(command_user, target_user, POINTS_COUNT)
    assert target_user.points == 110


@patch("omegabot.services.points.log_points_change", spec=log_points_change)
def test_add_points_logs_change(mock_log_points_change: MagicMock, command_user: User, target_user: User):
    add_points(command_user, target_user, POINTS_COUNT)
    mock_log_points_change.assert_called_once_with(command_user, target_user, POINTS_COUNT)
