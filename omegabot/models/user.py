from omegabot.models.base import BaseModel
from peewee import CharField, IntegerField


class User(BaseModel):
    discord_id = IntegerField()
    guild_id = IntegerField()
    name = CharField()
    points = IntegerField(default=0)

    class Meta:
        indexes = ((("discord_id", "guild_id"), True),)
