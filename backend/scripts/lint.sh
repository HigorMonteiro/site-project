#!/bin/bash
set -euxo pipefail

poetry run black apps/ settings/ tests/
poetry run isort apps/ settings/ tests/
poetry run flake8 apps/ settings/ tests/
poetry run ruff check apps/ settings/ tests/