from omegabot.models.base import BaseModel
from peewee import IntegerField


class PointLeaderRole(BaseModel):
    guild_id = IntegerField(unique=True)
    role_id = IntegerField()
