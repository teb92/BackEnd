
import os
from datetime import timedelta

def _as_bool(val: str, default: bool = False) -> bool:
    if val is None:
        return default
    return str(val).strip().lower() in {"1", "true", "yes", "y", "on"}

class Config:
    # ---- Flask ----
    DEBUG = _as_bool(os.getenv("DEBUG", "true"))
    TESTING = _as_bool(os.getenv("TESTING", "false"))
    SECRET_KEY = os.getenv("XX", "dev-XXX-key")
    JSON_SORT_KEYS = _as_bool(os.getenv("JSON_SORT_KEYS", "false"))

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "XX+XX://XX:XX@localhost:XX/postgres"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = _as_bool(os.getenv("SQLALCHEMY_ECHO", "false"))
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
    }

    JWT_SECRET_KEY = os.getenv("XX", "XX")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_TTL_SECONDS", "3600"))
    )
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "redis-xxx.c266.usxxx-3.ec2.redns.redis-cloud.com"
    CACHE_REDIS_PORT = xxx
    CACHE_REDIS_DB = 0
    CACHE_REDIS_USERNAME = "default"
    CACHE_REDIS_PASSWORD = "XXXX"

    CACHE_REDIS_CONNECTION_ARGUMENTS = {
        "ssl": True,
        "ssl_cert_reqs": None,
    }

    CACHE_DEFAULT_TIMEOUT = 120
    CACHE_KEY_PREFIX = "api:"

    DEFAULT_PAGE_SIZE = 20
