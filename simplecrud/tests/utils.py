import asyncio


def async_to_sync(func):
    """Decorator to convert async function to sync"""

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(func(*args, **kwargs))
        return result

    return wrapper
