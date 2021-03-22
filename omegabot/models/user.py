from omegabot.models.base import BaseModel
from peewee import IntegerField


class User(BaseModel):
    id = IntegerField(primary_key=True)
    points = IntegerField(default=0)
