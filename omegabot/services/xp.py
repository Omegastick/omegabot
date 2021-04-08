import logging
import math
from datetime import datetime, timedelta

from omegabot.models import User

XP_CONSTANT = 10

LOG = logging.getLogger(__name__)


def add_xp(user: User, amount: int, cooldown=timedelta(minutes=5)) -> User:
    if user.xp_last_update_time + cooldown > datetime.now():
        return user
    LOG.info(f"Adding {amount} xp for user {user.name}")
    user.xp += amount
    user.xp_last_update_time = datetime.now()
    user.save()
    return user


def xp_to_level(xp: int) -> int:
    return int((math.sqrt(XP_CONSTANT * (2 * xp + XP_CONSTANT * 0.25)) + XP_CONSTANT * 0.5) / XP_CONSTANT)


def level_to_xp(level: int) -> int:
    return int((level ** 2 + level) * 0.5 * XP_CONSTANT - (level * XP_CONSTANT))
