#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."
cd "${ROOT_DIR}"

python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Running unit tests with coverage"
pytest --cov=src --cov-report=xml --cov-report=term-missing

echo "Tests completed successfully."