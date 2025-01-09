import asyncio
import logging
from functools import wraps


def async_to_sync(func):
    """Decorator to convert async function to sync"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(func(*args, **kwargs))
        return result

    return wrapper


def add_log(func):
    """Decorator to add log"""

    @wraps(func)
    def inner(*args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.debug(f"{__name__}.{func.__name__}: args = {args}, kwargs = {kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"{__name__}.{func.__name__}: result = {result}")
        return result

    return inner
