FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY src/ ./src/
COPY scripts/ ./scripts/
COPY benchmarks/ ./benchmarks/

CMD ["python", "-m", "timberland_analytics.cli", "--help"]
