import redis
from fastapi import HTTPException
from common.utils.logger import Logger
from common.utils.config import config

logger=Logger()

class Redis:
    def __init__(self):
        try:
            self.redis_conn = redis.StrictRedis(
                host=config.Redis.host,
                port=config.Redis.port,
                db=0,
                decode_responses=True
            )
            # Test connection
            self.redis_conn.ping()
            
        except Exception as e:
            logger.error(f"Redis connection failed: {str(e)}")
            self.redis_conn = None
            raise HTTPException(status_code=500, detail="Redis connection failed")

    def get_redis_conn(self):
        if not self.redis_conn:
            logger.error("Redis connection not available")
            raise HTTPException(status_code=500, detail="Redis connection not available")
        return self.redis_conn

    def insert_data(self, key: str, value: str, expiry: int = None):
        """
        Insert a simple key-value pair into Redis using SET.
        Optionally set an expiry time in seconds.
        """

        try:
            conn = self.get_redis_conn()

            conn.set(key, value)
            logger.info(f"Inserted into Redis: {key} -> {value}")

            if expiry:
                conn.expire(key, expiry)
                logger.info(f"Expiry set for {key}: {expiry} seconds")

            return True

        except Exception as e:
            logger.error(f"Redis insert failed ({key}): {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to write into Redis")
        
    def retrieve_data(self, key: str):
        """
        Retrieve a value from Redis using GET.
        Returns:
            - value (str) if key exists
            - None if key does not exist
        """
        try:
            conn = self.get_redis_conn()

            value = conn.get(key)

            if value is None:
                logger.info(f"Redis: Key '{key}' not found")
            else:
                logger.info(f"Redis retrieved: {key} -> {value}")

            return value

        except Exception as e:
            logger.error(f"Redis retrieve failed ({key}): {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to read from Redis")

    def delete_data(self, key: str):
        try:
            logger.debug("Redis Delete is in Process")
            conn = self.get_redis_conn()
            deleted_count = conn.delete(key)
            logger.debug("Redis Delete is Completed")

            if deleted_count == 0:
                logger.info(f"Redis: Key '{key}' not found")
            else:
                logger.info(f"Redis Deleted: {key}")

            return deleted_count

        except Exception as e:
            logger.error(f"Redis Delete failed ({key}): {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to Delete from Redis")
