.PHONY: start check-migrations test lint

start:
	@echo "Starting the project..."
	@python manage.py runserver

check-migrations:
	@echo "Checking migrations..."
	@python manage.py makemigrations --check --dry-run

test:
	@echo "Running tests with coverage..."
	@pytest --cov

lint:
	@echo "Running linters..."
	@isort .
	@ruff check . --config pyproject.toml
	@black . --check 