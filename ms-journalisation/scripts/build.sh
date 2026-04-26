#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."
cd "${ROOT_DIR}"

IMAGE_NAME="${IMAGE_NAME:-ms-journalisation:ci}"
NO_CACHE="${NO_CACHE:-false}"

python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Building Docker image: ${IMAGE_NAME}"
if [[ "${NO_CACHE}" == "true" ]]; then
  docker build --no-cache -t "${IMAGE_NAME}" .
else
  docker build -t "${IMAGE_NAME}" .
fi

echo "Docker image ${IMAGE_NAME} built successfully."