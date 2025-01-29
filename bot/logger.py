import logging


def set_logger() -> None:
    formatter = logging.Formatter("[%(asctime)s %(levelname)s][Bot] %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger("bot")
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
