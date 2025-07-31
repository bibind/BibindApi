"""Simple Kafka producer using aiokafka."""

from __future__ import annotations

import json
from aiokafka import AIOKafkaProducer
from typing import Any


class KafkaProducer:
    """Wrapper around :class:`AIOKafkaProducer` for JSON messages."""

    def __init__(self, bootstrap_servers: str = "localhost:9092") -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        self._started = False

    async def start(self) -> None:
        if not self._started:
            await self._producer.start()
            self._started = True

    async def stop(self) -> None:
        if self._started:
            await self._producer.stop()
            self._started = False

    async def send(self, topic: str, message: Any, key: str | None = None) -> None:
        """Send a JSON serializable message to a topic."""
        await self.start()
        await self._producer.send_and_wait(
            topic,
            value=message,
            key=key.encode("utf-8") if key else None,
        )
