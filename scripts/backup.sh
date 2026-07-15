#!/usr/bin/env bash
set -euo pipefail
mkdir -p backups
docker compose exec -T db pg_dump -U "${POSTGRES_USER:-bechad}" "${POSTGRES_DB:-bechad}" > "backups/bechad-$(date +%Y%m%d-%H%M%S).sql"
