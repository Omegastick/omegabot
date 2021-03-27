import logging

from omegabot.models import CommandLog, User

LOG = logging.getLogger(__name__)


def log_points_change(command_user: User, target_user: User, points: int):
    CommandLog.create(command_user=command_user, target_user=target_user, points=points)
