import sys
import logging
from datetime import datetime
from functools import wraps
from typing import Callable

LOG_LEVEL = logging.DEBUG


def _config_logger():
    logger = logging.getLogger('simple_logger')
    logger.setLevel(LOG_LEVEL)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(LOG_LEVEL)

    formatter = logging.Formatter("[%(asctime)s][%(processName)s:%(threadName)s][%(levelname)s][%(module)s.%(funcName)s:%(lineno)d] %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def log_time(func: Callable):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        try:
            return func(*args, **kwargs)
        finally:
            end_time = datetime.now()
            logger.debug('function {} took {}s'.format(func.__name__, (end_time - start_time).total_seconds()))

    return wrapper


logger = _config_logger()
