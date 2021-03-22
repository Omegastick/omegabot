#!/usr/bin/env python


import logging

import omegabot.commands  # noqa
import omegabot.event_handlers  # noqa
from omegabot.app import db, start_bot
from omegabot.logging import setup_logging
from omegabot.models import ALL_MODELS

LOG = logging.getLogger(__name__)


def init_db():
    LOG.info("Initializing database")
    db.connect()
    db.create_tables(ALL_MODELS)


if __name__ == "__main__":
    setup_logging()
    init_db()
    start_bot()
