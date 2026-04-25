
from common.utils.logger import Logger

logger = Logger()

def safe_handler(func):
    async def wrapper(message, *args, **kwargs):
        try:
            return await func(message, *args, **kwargs)
        except Exception as e:
            logger.error(f"Handler Error in {func.__name__}: {e}", exc_info=True)
    return wrapper