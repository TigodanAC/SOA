FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    netcat-openbsd \
    curl \
    gcc \
    python3-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY statistic_serv/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pytest

COPY . .
COPY proto/ ./proto/
COPY broker/ ./broker/

ENV PYTHONPATH=/app:/app/proto:/app/broker
ENV CLICKHOUSE_URL=clickhouse://default:password@clickhouse:8123/default
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092

EXPOSE 50052

CMD sh -c "sleep 20"
CMD sh -c "while ! curl -s 'http://clickhouse:8123/' >/dev/null; do sleep 2; done && python statistic_serv/main.py"