"""Optional Kafka producer for organisation events."""

from kafka import KafkaProducer
from pathlib import Path
import yaml

SO_NAME = "so_organisation"


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


def get_producer() -> KafkaProducer:
    """Create and return a KafkaProducer instance."""
    return KafkaProducer()
