from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response

registry = CollectorRegistry()

planner_requests_total = Counter("planner_requests_total", "Total planner requests", registry=registry)
planner_request_latency_seconds = Histogram("planner_request_latency_seconds", "Planner request latency", registry=registry)

tfcc_processed_total = Counter("tfcc_processed_total", "TFCC processed messages", ["status"], registry=registry)
tfcc_dlq_total = Counter("tfcc_dlq_total", "TFCC messages sent to DLQ", registry=registry)

def metrics_router() -> APIRouter:
    router = APIRouter()

    @router.get("/metrics")
    def metrics() -> Response:
        data = generate_latest(registry)
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)

    return router
