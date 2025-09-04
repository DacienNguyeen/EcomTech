#!/bin/bash
set -o errexit

echo "Starting Render build process..."

# Change to backend directory
cd /opt/render/project/src/backend

# Verify we are in the right directory
echo "Current directory: $(pwd)"
echo "Contents:"
ls -la

# Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Verify PyJWT installation
echo "Verifying PyJWT installation..."
python -c "import jwt; print(f\"PyJWT version: {jwt.__version__}\")"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=config.settings.production

# Run migrations
echo "Running database migrations..."
python manage.py migrate --settings=config.settings.production

echo "Build completed successfully!"
