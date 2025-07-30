import json
import redis


class CacheManager:
    def __init__(self, host, port, password, *args, **kwargs):
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                password=password,
                *args,
                **kwargs,
            )
            connection_status = self.redis_client.ping()
            if connection_status:
                print("Connection created successfully")
            else:
                raise redis.ConnectionError("Redis ping failed")
        except redis.RedisError as error:
            print(f"Failed to connect to Redis: {error}")
            self.redis_client = None

    def is_connected(self):
        if self.redis_client is None:
            return False
        try:
            return self.redis_client.ping()
        except redis.RedisError:
            return False

    def store_data(self, key, value, time_to_live=None):
        try:
            serialized = json.dumps(value)
            if time_to_live is None:
                self.redis_client.set(key, serialized)
            else:
                self.redis_client.setex(key, time_to_live, serialized)
        except redis.RedisError as error:
            print(f"An error ocurred while storing data in Redis: {error}")

    def check_key(self, key):
        try:
            key_exists = self.redis_client.exists(key)
            if key_exists:
                ttl = self.redis_client.ttl(key)
                return True, ttl

            return False, None
        except redis.RedisError as error:
            print(f"An error ocurred while checking a key in Redis: {error}")
            return False, None

    def get_data(self, key):
        try:
            output = self.redis_client.get(key)
            if output is not None:
                result = json.loads(output.decode("utf-8"))
                return result
            else:
                return None
        except redis.RedisError as error:
            print(f"An error ocurred while retrieving data from Redis: {error}")

    def delete_data(self, key):
        try:
            output = self.redis_client.delete(key)
            return output == 1
        except redis.RedisError as error:
            print(f"An error ocurred while deleting data from Redis: {error}")
            return False

    def delete_data_with_pattern(self, pattern):
        try:
            # Iterar sobre las claves que coinciden con el patrón
            for key in self.redis_client.scan_iter(match=pattern):
                self.delete_data(key)
        except redis.RedisError as error:
            print(f"An error ocurred while deleting data from Redis: {error}")
    def get(self, key):
        return self.get_data(key)

    def set(self, key, value, ttl=None):
        return self.store_data(key, value, ttl)

    def delete(self, key):
        return self.delete_data(key) 