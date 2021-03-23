from omegabot.models.base import BaseModel
from omegabot.models.user import User
from peewee import ForeignKeyField, IntegerField


class CommandLog(BaseModel):
    command_user = ForeignKeyField(User, backref="commands")
    target_user = ForeignKeyField(User, backref="transactions")
    points = IntegerField()
