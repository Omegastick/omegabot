import logging

from omegabot.models.feature import Feature

LOG = logging.getLogger(__name__)


def enable_feature_for_guild(feature: str, guild_id: int) -> None:
    LOG.info(f"Enabling feature {feature} for guild {guild_id}")
    Feature.replace(guild_id=guild_id, feature=feature).execute()
