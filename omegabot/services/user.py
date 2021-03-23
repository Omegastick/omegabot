import logging

from discord import User as DiscordUser
from omegabot.models import User

LOG = logging.getLogger(__name__)


def get_or_create_user(user: DiscordUser) -> User:
    created_user, created = User.get_or_create(id=user.id, defaults={"name": user.name})
    if created:
        LOG.info(f"Creating user {user.name}")
    if created_user.name != user.name:
        created_user.name = user.name
        created_user.save()
    return created_user
