from omegabot.models.base import BaseModel
from peewee import CharField, IntegerField


class User(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    points = IntegerField(default=0)
