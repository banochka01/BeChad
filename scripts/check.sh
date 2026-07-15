#!/usr/bin/env bash
set -euo pipefail
(cd backend && python -m pytest)
(cd backend && python -m ruff check app tests)
(cd android && ./gradlew testDebugUnitTest assembleDebug)
