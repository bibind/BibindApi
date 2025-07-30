"""Kafka consumer to trigger realisation workflows."""

from threading import Thread
from kafka import KafkaConsumer


def _listen() -> None:
    consumer = KafkaConsumer('realisation-topic')
    for msg in consumer:
        # TODO: handle incoming messages
        print(msg.value)


def start_kafka_listener() -> None:
    """Start Kafka consumer in a background thread."""
    thread = Thread(target=_listen, daemon=True)
    thread.start()
