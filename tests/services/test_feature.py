from omegabot.models.feature import Feature
from omegabot.services.feature import enable_feature_for_guild


def test_enable_feature_creates_new_row_if_none_exists():
    enable_feature_for_guild("test", 1)
    assert Feature.select().where(Feature.guild_id == 1, Feature.feature == "test").exists()
