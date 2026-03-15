#!/bin/bash
# Docker entrypoint script for Render deployment
# Runs migrations, syncs curriculum, then starts the API

set -e  # Exit on error

echo "=========================================="
echo "🚀 OOP Journey API - Startup Sequence"
echo "=========================================="

# Step 1: Run database migrations
echo ""
echo "📊 Step 1/3: Running database migrations..."
alembic upgrade head
if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migration failed - continuing anyway (may be already applied)"
fi

# Step 2: Sync curriculum data
echo ""
echo "📚 Step 2/3: Syncing curriculum data..."
python scripts/sync_curriculum.py
if [ $? -eq 0 ]; then
    echo "✅ Curriculum sync completed successfully"
else
    echo "⚠️ Curriculum sync had issues - API may still work with existing data"
fi

# Step 3: Verify database (optional, for logging)
echo ""
echo "🔍 Step 3/3: Verifying database..."
python scripts/verify_database.py || true  # Don't fail if verify has issues

echo ""
echo "=========================================="
echo "✨ Starting API Server..."
echo "=========================================="
echo ""

# Start the API server
exec uvicorn api.main:app --host 0.0.0.0 --port 8000
