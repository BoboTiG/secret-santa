#!/bin/bash

python -m isort secret_santa
python -m black secret_santa
python -m flake8 secret_santa
python -m mypy secret_santa --exclude tests
