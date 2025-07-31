"""Kafka consumer to trigger conception workflows."""

from threading import Thread
from kafka import KafkaConsumer
from pathlib import Path
import yaml

SO_NAME = "so_conception"


def _get_topic() -> str:
    mapping_file = (
        Path(__file__).resolve().parents[2]
        / "op_bootstrap"
        / "app"
        / "config"
        / "so_mapping.yaml"
    )
    with open(mapping_file, "r", encoding="utf-8") as f:
        mapping = yaml.safe_load(f)
    return mapping["topics"][SO_NAME]


def _listen() -> None:
    consumer = KafkaConsumer(_get_topic())
    for msg in consumer:
        # TODO: handle incoming messages
        print(msg.value)


def start_kafka_listener() -> None:
    """Start Kafka consumer in a background thread."""
    thread = Thread(target=_listen, daemon=True)
    thread.start()
