FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
ENV PYTHONPATH=/app/src
ENV KAFKA_BOOTSTRAP_SERVERS=redpanda:9092
EXPOSE 8001
CMD [ "python", "-m", "src.entrypoints.tfcc_worker.worker" ]
