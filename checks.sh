#!/bin/bash

python -m isort secret_santa tests
python -m black secret_santa tests
python -m flake8 secret_santa tests
python -m mypy secret_santa
