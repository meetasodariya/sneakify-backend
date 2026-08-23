#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "📦 Installing backend Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎨 Collecting static files with WhiteNoise..."
python manage.py collectstatic --no-input

echo "🗄️ Running database migrations on Neon PostgreSQL..."
python manage.py migrate --no-input

echo "🌱 Seeding initial sneaker models and customizer catalog..."
python manage.py seed_catalog || true

echo "✅ Backend build finished successfully!"
