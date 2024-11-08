.PHONY: start check-migrations test lint

run:
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
	@bash scripts/lint.sh

populate-db:
	@echo "Clean the database..."
	@python manage.py flush --no-input
	@echo "Migrating the database..."
	@python manage.py migrate
	@echo "Populating the database ..."
	@python manage.py populate_users
	@python manage.py populate_db
