import json
from typing import Dict

from app.strategy.base import IOutputStrategy


class RedisOutputStrategy(IOutputStrategy):
    """Appends each row as a JSON string to a Redis list."""

    def __init__(self, host: str, port: int, key: str) -> None:
        import redis

        self.key = key
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def output(self, row: Dict[str, str]) -> None:
        self.client.rpush(self.key, json.dumps(row))

    def close(self) -> None:
        self.client.close()
