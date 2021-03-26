import logging

from discord import Guild
from omegabot.models import User
from omegabot.services.history import log_points_change

LOG = logging.getLogger(__name__)


def add_points(command_user: User, target_user: User, guild: Guild, points: int) -> User:
    LOG.info(f"Giving {target_user.name} {points} points")
    log_points_change(command_user, target_user, points)
    target_user.points += points
    target_user.save()
    return target_user
