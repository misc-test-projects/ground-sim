FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY sample-plan.json ./sample-plan.json
ENV PYTHONPATH=/app/src
ENV KAFKA_BOOTSTRAP_SERVERS=redpanda:9092
EXPOSE 8080
CMD [ "uvicorn", "src.entrypoints.planner_api.main:app", "--host", "0.0.0.0", "--port", "8080" ]
