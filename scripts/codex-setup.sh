#!/usr/bin/env bash
set -euo pipefail
java -version || true
python3 --version
(cd backend && python3 -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install '.[test]')
command -v sdkmanager >/dev/null && sdkmanager --install 'platforms;android-35' 'build-tools;35.0.0' || echo 'sdkmanager unavailable; CI will install Android SDK components'
