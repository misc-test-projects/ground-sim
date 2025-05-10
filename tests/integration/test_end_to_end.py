import os
import pytest
from datetime import datetime, timedelta, timezone
import asyncio
import json

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_KAFKA_TESTS") != "1",
    reason="Set RUN_KAFKA_TESTS=1 to run Kafka integration tests"
)

from src.core.models import Plan, Resource
from src.adapters.kafka_client import send_event, get_consumer

@pytest.mark.asyncio
async def test_end_to_end_kafka():
    plan = Plan(
        id="it-plan", version=1,
        window_start=datetime.now(timezone.utc),
        window_end=datetime.now(timezone.utc) + timedelta(hours=1),
        resources=[Resource(name="radar", capacity=2)],
        constraints={"min_separation_minutes": 5},
    )
    await send_event("mission.plan.created", key=plan.id, value=plan.model_dump(mode="json"))
    consumer = await get_consumer("mission.plan.verified", group_id="it-tests")
    try:
        async for msg in consumer:
            if msg.get("plan_id") == "it-plan":
                return
    finally:
        await consumer.stop()
    assert False, "No verified message observed"
