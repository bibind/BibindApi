"""Generic Kafka consumer using aiokafka."""

from __future__ import annotations

import asyncio
import json
from typing import Any, Callable

from aiokafka import AIOKafkaConsumer


async def _consume(
    topics: list[str],
    handler: Callable[[str, Any], None | asyncio.Future],
    bootstrap_servers: str = "localhost:9092",
) -> None:
    consumer = AIOKafkaConsumer(
        *topics,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="op_bootstrap",
        enable_auto_commit=True,
    )
    await consumer.start()
    try:
        async for msg in consumer:
            result = handler(msg.topic, msg.value)
            if asyncio.iscoroutine(result):
                await result
    finally:
        await consumer.stop()


def start_consumer(
    topics: list[str],
    handler: Callable[[str, Any], None | asyncio.Future],
    loop: asyncio.AbstractEventLoop | None = None,
    bootstrap_servers: str = "localhost:9092",
) -> asyncio.Task:
    """Start consumer in background task and return the task instance."""
    loop = loop or asyncio.get_event_loop()
    return loop.create_task(_consume(topics, handler, bootstrap_servers))
