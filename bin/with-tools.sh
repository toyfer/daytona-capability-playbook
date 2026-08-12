#!/usr/bin/env bash
# Run a command with /workspace/.tools on PATH.
set -euo pipefail
ENV_FILE="${TOOLS_ENV:-/workspace/.tools/env}"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi
exec "$@"
