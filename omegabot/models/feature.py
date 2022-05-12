from omegabot.models.base import BaseModel
from peewee import IntegerField, TextField


class Feature(BaseModel):
    guild_id = IntegerField()
    feature = TextField()

    class Meta:
        indexes = ((("guild_id", "feature"), True),)
