from omegabot.models.base import BaseModel
from peewee import CharField, IntegerField


class WelcomeMessage(BaseModel):
    guild_id = IntegerField(primary_key=True)
    channel_id = IntegerField()
    message = CharField(max_length=1000)
