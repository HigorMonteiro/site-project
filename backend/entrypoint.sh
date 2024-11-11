#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Print commands and their arguments as they are executed
set -x

# Run database migrations
echo "Running database migrations..."
poetry run python manage.py migrate


# Start the application
echo "Starting the application..."
poetry run python manage.py runserver