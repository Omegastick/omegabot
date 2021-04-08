from omegabot.models.base import BaseModel
from peewee import CharField, IntegerField


class WelcomeMessage(BaseModel):
    guild_id = IntegerField(primary_key=True)
    message = CharField(max_length=1000)
