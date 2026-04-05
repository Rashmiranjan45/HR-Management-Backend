# ---------- Stage 1 : Builder ----------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies required for building packages
RUN apt-get update && \
    apt-get install -y gcc curl default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-cache


# ---------- Stage 2 : Production ----------
FROM python:3.12-slim

WORKDIR /app

# Install runtime libraries only
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /usr/local /usr/local

# Copy application source code
COPY . .

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "app.app:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000"]
