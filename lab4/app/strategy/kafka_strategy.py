import json
from typing import Dict

from app.strategy.base import IOutputStrategy


class KafkaOutputStrategy(IOutputStrategy):
    """Sends each row as a JSON message to a Kafka topic."""

    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        from kafka import KafkaProducer

        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def output(self, row: Dict[str, str]) -> None:
        self.producer.send(self.topic, row)

    def close(self) -> None:
        self.producer.flush()
        self.producer.close()
