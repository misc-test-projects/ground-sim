SHELL:=/bin/bash

up:
	docker compose -f ops/compose.yaml up -d --build

down:
	docker compose -f ops/compose.yaml down -v

test:
	pytest -q --junitxml=reports/junit.xml --cov=src --cov-report=xml:reports/coverage.xml

format:
	python -m pip install ruff black && ruff check src tests && black src tests

evidence:
	mkdir -p artifacts/test-evidence && cp -r reports artifacts/test-evidence || true
