from datetime import datetime

from omegabot.models.base import BaseModel
from peewee import CharField, DateTimeField, IntegerField


class User(BaseModel):
    discord_id = IntegerField()
    guild_id = IntegerField()
    name = CharField()
    points = IntegerField(default=0)
    xp = IntegerField(default=0)
    xp_last_update_time = DateTimeField(default=datetime.now)

    class Meta:
        indexes = ((("discord_id", "guild_id"), True),)
