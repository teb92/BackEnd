
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from sqlalchemy import MetaData

DEFAULT_SCHEMA = "ECommercePets"
metadata = MetaData(schema=DEFAULT_SCHEMA)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
cache = Cache()


def cache_key_prefix(app):
    return app.config.get("CACHE_KEY_PREFIX", "")

def delete_pattern(pattern: str):

    try:
        backend = cache.cache
        client = getattr(backend, "_client", None)
        if client is None:
            read_clients = getattr(backend, "_read_clients", None)
            client = read_clients[0] if read_clients else None
        if client is None:
            return 0

        key_prefix = getattr(backend, "key_prefix", "flask_cache_")
        full = f"{key_prefix}{pattern}"

        deleted = 0
        for key in client.scan_iter(match=full):
            client.delete(key)
            deleted += 1
        return deleted
    except Exception:
        return 0
