#!/bin/bash
set -euxo pipefail

poetry run black apps/ settings/
poetry run isort apps/ settings/
poetry run flake8 apps/ settings/
poetry run ruff check apps/ settings/ 