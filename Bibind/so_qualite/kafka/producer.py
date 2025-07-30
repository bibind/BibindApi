"""Optional Kafka producer for qualite events."""

from kafka import KafkaProducer


def get_producer() -> KafkaProducer:
    """Create and return a KafkaProducer instance."""
    return KafkaProducer()
