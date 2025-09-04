#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting Render build process..."

# Ensure we are in the backend directory
cd "$(dirname "$0")"

# Install Python dependencies from backend directory
echo "Installing Python packages from backend/requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found in backend directory"
    exit 1
fi
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=config.settings.production

# Run migrations
echo "Running database migrations..."
python manage.py migrate --settings=config.settings.production

echo "Build completed successfully!"
