#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."
cd "${ROOT_DIR}"

python -m pip install --upgrade pip
pip install -r requirements.txt

rm -rf coverage_html
mkdir -p coverage_html

echo "Running pytest and generating reports..."
pytest --junitxml=rapport_tests.xml \
  --cov=src \
  --cov-report=xml \
  --cov-report=html:coverage_html \
  --cov-report=term-missing | tee rapport_tests.txt

echo "Generated: rapport_tests.txt, rapport_tests.xml, coverage_html/"