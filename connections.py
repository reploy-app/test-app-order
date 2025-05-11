import psycopg2
import redis
import logging
from config import (
    POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER,
    POSTGRES_PASSWORD, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD,
)

logger = logging.getLogger(__name__)


# PostgreSQL connection
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        return conn
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
        if conn:
            conn.close()
        return None


# Redis connection
def get_redis_connection():
    try:
        if REDIS_PASSWORD:
            r = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                decode_responses=True
            )
        else:
            r = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True
            )
        return r
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")
        return None


# Health check function
async def check_connections():
    results = {
        "postgres": False,
        "redis": False
    }

    # Check PostgreSQL
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            results["postgres"] = True
    except Exception as e:
        logger.error(f"PostgreSQL health check failed: {e}")

    # Check Redis
    try:
        r = get_redis_connection()
        if r and r.ping():
            results["redis"] = True
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")

    return results, all(results.values())
