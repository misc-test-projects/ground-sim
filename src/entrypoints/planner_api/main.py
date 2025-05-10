import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware
from time import perf_counter

from ...core.models import Plan
from ...core.use_cases import validate_plan
from ...adapters.kafka_client import send_event
from ...adapters.telemetry import metrics_router, planner_requests_total, planner_request_latency_seconds

app = FastAPI(title="Planner API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(metrics_router())

@app.post("/plan")
async def create_plan(plan: Plan):
    start = perf_counter()
    planner_requests_total.inc()
    try:
        validate_plan(plan)
    except (ValidationError, Exception) as e:
        raise HTTPException(status_code=400, detail=str(e))

    payload = plan.model_dump(mode="json")
    await send_event("mission.plan.created", key=plan.id, value=payload)
    planner_request_latency_seconds.observe(perf_counter() - start)
    return {"status": "accepted", "plan_id": plan.id, "version": plan.version}
