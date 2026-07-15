#!/usr/bin/env bash
set -euo pipefail
command -v docker >/dev/null || { echo "Docker is required"; exit 1; }
[ -f .env ] || cp .env.example .env
docker compose up -d --build db
docker compose up -d --build backend caddy
for i in {1..30}; do curl -fsS http://localhost:8000/health && break || sleep 2; done
echo "BeChad deployed: http://localhost:8000/health"
