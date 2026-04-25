import time
import functools
from common.utils.logger import Logger

logger = Logger()



def timing_decorator_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()          # Start timer
        result = func(*args, **kwargs)    # Call normal function
        end_time = time.time()            # End timer

        execution_time = end_time - start_time
        logger.debug(
            f"Function '{func.__name__}' executed in {execution_time:.6f} seconds"
        )
        return result
    return wrapper

def timing_decorator_async(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()          # Start timer
        result = await func(*args, **kwargs)    # Call normal function
        end_time = time.time()            # End timer

        execution_time = end_time - start_time
        logger.info(
            f"Function '{func.__name__}' executed in {execution_time:.6f} seconds"
        )
        return result
    return wrapper
