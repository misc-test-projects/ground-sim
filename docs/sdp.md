# Software Development Plan (SDP) – Ground Planner & TFCC Simulator

## Lifecycle
1. **Requirements** → 2. **OO Design** → 3. **Code & Unit Test** → 4. **Integration Test** → 5. **Support to Formal Test/Delivery**

## Requirements (subset)
- REQ-001: The system SHALL accept versioned mission plans via a REST endpoint.
- REQ-002: Mission plans SHALL be validated for time windows and resource constraints.
- REQ-003: Valid plans SHALL publish `mission.plan.created` to Kafka.
- REQ-004: The TFCC worker SHALL verify plans and emit `mission.plan.verified` or `mission.plan.rejected`.
- REQ-005: The worker SHALL implement retry with backoff; unresolvable messages go to DLQ.
- REQ-006: The system SHALL expose Prometheus metrics (latency, error rate, throughput).

## OO Design
- Domain model: `Plan`, `Resource`, `Constraint`
- Use cases: `validate_plan(plan)`, `verify_plan(plan)`
- Adapters: Kafka producer/consumer, telemetry
- Entrypoints: FastAPI service (planner_api), async worker (tfcc_worker)

## Verification
- Unit tests for models and use cases
- Integration test for end-to-end flow (when Kafka available)
- Evidence: junit.xml, coverage.xml, logs, dashboards

## Delivery
- Docker Compose brings up the full stack
- CI builds, tests, and publishes evidence artifacts
