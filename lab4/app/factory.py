from app.strategy.base import IOutputStrategy


def create_strategy(config: dict) -> IOutputStrategy:
    name = config["output"]["strategy"]

    if name == "console":
        from app.strategy.console_strategy import ConsoleOutputStrategy
        return ConsoleOutputStrategy()

    if name == "kafka":
        cfg = config["kafka"]
        from app.strategy.kafka_strategy import KafkaOutputStrategy
        return KafkaOutputStrategy(
            bootstrap_servers=cfg["bootstrap_servers"],
            topic=cfg["topic"],
        )

    if name == "redis":
        cfg = config["redis"]
        from app.strategy.redis_strategy import RedisOutputStrategy
        return RedisOutputStrategy(
            host=cfg["host"],
            port=int(cfg["port"]),
            key=cfg["key"],
        )

    raise ValueError(
        f"Unknown strategy '{name}'. Allowed values: console, kafka, redis"
    )
