FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations, seed data, then start server
CMD alembic upgrade head && \
    python scripts/seed_data.py && \
    uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
