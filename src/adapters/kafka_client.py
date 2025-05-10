import asyncio
import json
import os
from typing import Any, Dict, Optional
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "redpanda:9092")

async def get_producer() -> AIOKafkaProducer:
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
    await producer.start()
    return producer

async def send_event(topic: str, key: Optional[str], value: Dict[str, Any]) -> None:
    producer = await get_producer()
    try:
        await producer.send_and_wait(topic, key=(key.encode() if key else None), value=value)
    finally:
        await producer.stop()

async def get_consumer(topic: str, group_id: str) -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP,
        group_id=group_id,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        enable_auto_commit=True,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    return consumer
