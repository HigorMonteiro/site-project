#!/bin/bash
set -euxo pipefail

poetry run black apps/ tests/ settings/
poetry run isort --profile hug --check --diff tests/
poetry run flake8 apps/ tests/ settings/
poetry run ruff check apps/ tests/ settings/ 