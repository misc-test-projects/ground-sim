# Ground Planner & TFCC Simulator (Python/Linux, SDP and Formal Test)

A Linux-first, event-driven simulator of a **Ground Planner → TFCC** workflow built with **FastAPI** and **Kafka (Redpanda)**.
It mirrors an **SDP-style lifecycle**: requirements → OO design → code & unit test → support to **formal test/delivery**.
It includes **traceability** artifacts, **observability** (Prometheus metrics), and a **CI pipeline** that collects test evidence.

## Quickstart

### 1) Prereqs
- Docker & Docker Compose
- Make (optional)

### 2) Bring up the stack
```bash
make up          # or: docker compose -f ops/compose.yaml up -d --build
```

This starts:
- **Redpanda** (Kafka) at `localhost:9092`
- **Planner API** at `http://localhost:8080`
- **TFCC Worker** (background consumer)
- **Prometheus** at `http://localhost:9090`
- **Grafana** at `http://localhost:3000` (user/pass: admin/admin)

### 3) Send a sample plan
```bash
curl -s -XPOST localhost:8080/plan \
  -H 'content-type: application/json' \
  -d @sample-plan.json | jq
```

### 4) View metrics / dashboards
- Planner API Prometheus metrics: `http://localhost:8080/metrics`
- Worker metrics: `http://localhost:8001/metrics`
- Grafana: import dashboards from `ops/grafana_dashboards/planner_tfcc.json`

### 5) Run tests locally
```bash
pip install -r requirements.txt
pytest -q --junitxml=reports/junit.xml --cov=src --cov-report=xml:reports/coverage.xml
```

> **Note:** Integration tests that require a Kafka broker will be skipped unless the environment is configured.
> The full end-to-end flow is exercised by `docker compose` via Redpanda.

## Repository layout
```
ground-sim/
  README.md
  requirements.txt
  Makefile
  sample-plan.json
  docs/
    sdp.md
    icd.md
    traceability.csv
  src/
    core/
      models.py
      use_cases.py
    adapters/
      kafka_client.py
      telemetry.py
    entrypoints/
      planner_api/
        main.py
      tfcc_worker/
        worker.py
  tests/
    unit/
      test_models.py
      test_use_cases.py
    integration/
      test_end_to_end.py
  ops/
    compose.yaml
    prometheus.yml
    grafana_dashboards/
      planner_tfcc.json
    docker/
      planner_api.Dockerfile
      tfcc_worker.Dockerfile
  .github/workflows/ci.yml
```
## Formal Test / Evidence
CI collects artifacts into `artifacts/test-evidence/`: JUnit XML, coverage, logs, and dashboard json.

## Security & Compliance
This is a **domain-adjacent** simulator. No export-controlled or classified logic is included.
