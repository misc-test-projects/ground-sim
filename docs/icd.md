# Interface Control Document (ICD)

## REST API
`POST /plan`

Request (JSON):
```json
{
  "id": "plan-001",
  "version": 1,
  "window_start": "2025-01-01T00:00:00Z",
  "window_end": "2025-01-01T02:00:00Z",
  "resources": [{"name":"radar-a","capacity":1}],
  "constraints": {"min_separation_minutes": 5}
}
```

Response:
```json
{"status":"accepted","plan_id":"plan-001","version":1}
```

## Kafka Topics
- `mission.plan.created` (key: plan_id, value: Plan JSON)
- `mission.plan.verified` (key: plan_id, value: status + reasons)
- `mission.plan.rejected` (key: plan_id, value: reasons)
- `mission.plan.dlq` (key: plan_id, value: original + error)

## Metrics
- `planner_requests_total`, `planner_request_latency_seconds`
- `tfcc_processed_total`, `tfcc_rejections_total`, `tfcc_dlq_total`
