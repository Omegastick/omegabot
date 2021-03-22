import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M"
    )
