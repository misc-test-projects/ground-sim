import asyncio
import json
import os
import signal
from time import perf_counter
from typing import Any, Dict

from ...core.models import Plan
from ...core.use_cases import verify_plan
from ...adapters.kafka_client import get_consumer, send_event
from ...adapters.telemetry import tfcc_processed_total, tfcc_dlq_total, metrics_router

from fastapi import FastAPI
from uvicorn import Config, Server

KAFKA_GROUP = os.getenv("KAFKA_GROUP", "tfcc-worker")

async def process_message(msg_value: Dict[str, Any]):
    plan = Plan(**msg_value)
    ok, reasons = verify_plan(plan)
    status = "verified" if ok else "rejected"
    out_topic = f"mission.plan.{status}"
    await send_event(out_topic, key=plan.id, value={"plan_id": plan.id, "version": plan.version, "reasons": reasons})
    tfcc_processed_total.labels(status=status).inc()

async def consume_loop():
    consumer = await get_consumer("mission.plan.created", group_id=KAFKA_GROUP)
    try:
        async for msg in consumer:
            try:
                await process_message(msg.value)
            except Exception as e:
                # DLQ on deserialize/processing errors
                tfcc_dlq_total.inc()
                await send_event("mission.plan.dlq", key=None, value={"error": str(e), "raw": msg.value})
    finally:
        await consumer.stop()

# Expose metrics as a small HTTP server (port 8001)
metrics_app = FastAPI(title="TFCC Worker Metrics")
metrics_app.include_router(metrics_router())

async def main():
    server = Server(Config(app=metrics_app, host="0.0.0.0", port=8001, log_level="info"))
    loop = asyncio.get_event_loop()
    loop.create_task(server.serve())
    await consume_loop()

if __name__ == "__main__":
    asyncio.run(main())
