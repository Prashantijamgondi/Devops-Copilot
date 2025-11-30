#!/bin/bash
# Render Deployment Start Script
# This mimics what Render will do

echo "🚀 Starting DevOps Co-Pilot Backend..."

# Navigate to backend directory
cd backend

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗄️ Running database migrations..."
python -m alembic upgrade head

echo "🌐 Starting server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload
