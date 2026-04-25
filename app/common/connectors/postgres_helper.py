import json
import asyncpg
from fastapi import HTTPException
from common.utils.config import config
from common.utils.logger import Logger

logger = Logger()


class PostgresHelper:
    def __init__(self):
        logger.debug("event=postgres_init status=initialized")
        self.pool = None

    async def init_pool(self):
        """Initialize PostgreSQL connection pool (call once on startup)."""
        try:
            self.pool = await asyncpg.create_pool(
                host=config.postgres.host,
                port=config.postgres.port,
                user=config.postgres.user_name,
                password=config.postgres.password,
                database=config.postgres.db_name,
                min_size=1,
                max_size=15,   # tune based on load
                command_timeout=60
            )
            logger.debug("event=postgres_pool status=created")
        except Exception as e:
            logger.error(f"event=postgres_pool status=failed error={e}")
            raise HTTPException(status_code=500, detail="Failed to create PostgreSQL pool")

    async def close_pool(self):
        if self.pool:
            await self.pool.close()
            logger.debug("event=postgres_pool status=closed")

    async def execute(self, query, *args, fetch=False, lastrowid=False):
        """
        Execute SQL query using asyncpg.
        Automatically JSON-encode dict/list params.
        """
        logger.info(f"Postgres Helper:::Execute:::Query:{query} values::{args}")

        if not self.pool:
            raise HTTPException(status_code=500, detail="PostgreSQL pool not initialized")

        processed_args = tuple(
            json.dumps(arg) if isinstance(arg, (dict, list)) else arg
            for arg in args
        )

        async with self.pool.acquire() as conn:
            try:
                if fetch:
                    result = await conn.fetch(query, *processed_args)
                    result = [dict(row) for row in result]

                    logger.debug(
                        f"event=postgres_execute status=success query_type={query.split()[0]}"
                    )
                    return result


                result = await conn.execute(query, *processed_args)

                logger.debug(
                    f"event=postgres_execute status=success query_type={query.split()[0]}"
                )
                return result

            except asyncpg.PostgresError as e:
                logger.error(
                    f"event=postgres_execute status=failed error={e} query_type={query.split()[0]}"
                )
                raise HTTPException(
                    status_code=500,
                    detail=f"PostgreSQL query execution failed: {e}"
                )

            except Exception as e:
                logger.error(
                    f"event=postgres_execute status=failed error={e} query_type={query.split()[0]}"
                )
                raise HTTPException(
                    status_code=500,
                    detail=f"PostgreSQL query execution failed: {e}"
                )

    async def get_table_columns(self, table_name: str):
        """
        Retrieve column names and data types for a given table.
        """
        query = """
            SELECT 
                column_name,
                data_type
            FROM information_schema.columns
            WHERE table_catalog = $1
            AND table_name = $2
            ORDER BY ordinal_position
        """

        result = await self.execute(
            query,
            config.postgres.db_name,
            table_name,
            fetch=True
        )

        logger.info(f"get_table_columns::result->{result}")

        logger.info(
            f"event=postgres_get_table_columns status=success table={table_name}"
        )
        return result

    async def get_foreign_keys(self, table_name: str):
        """
        Retrieve foreign key relationships for a table.
        """
        query = """
            SELECT
                kcu.column_name,
                ccu.table_name AS referenced_table_name,
                ccu.column_name AS referenced_column_name
            FROM information_schema.key_column_usage kcu
            JOIN information_schema.constraint_column_usage ccu
                ON kcu.constraint_name = ccu.constraint_name
            WHERE kcu.table_catalog = $1
            AND kcu.table_name = $2
        """

        result = await self.execute(
            query,
            config.postgres.db_name,
            table_name,
            fetch=True
        )

        logger.info(f"get_foreign_keys::{result}")
        return result
    

pg=PostgresHelper()
