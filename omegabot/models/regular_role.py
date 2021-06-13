from omegabot.models.base import BaseModel
from peewee import IntegerField


class RegularRole(BaseModel):
    guild_id = IntegerField(unique=True)
    role_id = IntegerField()
    apply_delay = IntegerField()
