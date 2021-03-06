import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(name)-30s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M"
    )
