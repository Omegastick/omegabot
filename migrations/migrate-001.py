#!/usr/bin/env python

import os
from datetime import datetime

from peewee import DateTimeField, IntegerField, SqliteDatabase
from playhouse.migrate import SqliteMigrator, migrate

db = SqliteDatabase(os.getenv("DATABASE_FILE", "omegabot.db"))
migrator = SqliteMigrator(db)

with db.atomic():
    migrate(
        migrator.add_column("user", "xp", IntegerField(default=0)),
        migrator.add_column("user", "xp_last_update_time", DateTimeField(default=datetime.now)),
    )
