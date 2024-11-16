#!/bin/bash
set -eu
python -m ruff format secret_santa tests
python -m ruff check --fix --unsafe-fixes secret_santa tests
python -m mypy secret_santa
