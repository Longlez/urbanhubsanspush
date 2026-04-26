#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."
cd "${ROOT_DIR}"

IMAGE_NAME="${IMAGE_NAME:-ms-journalisation:ci}"
REGISTRY="${REGISTRY:-}"
TARGET_IMAGE="${TARGET_IMAGE:-${REGISTRY}/${IMAGE_NAME}}"

if [[ -z "${REGISTRY}" ]]; then
  echo "ERROR: REGISTRY environment variable is required for deployment."
  echo "Example: REGISTRY=myregistry.example.com ./scripts/deploy.sh"
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker is required for deployment."
  exit 1
fi

echo "Tagging image ${IMAGE_NAME} as ${TARGET_IMAGE}"
docker tag "${IMAGE_NAME}" "${TARGET_IMAGE}"

echo "Pushing ${TARGET_IMAGE}"
docker push "${TARGET_IMAGE}"

echo "Deployment push completed."