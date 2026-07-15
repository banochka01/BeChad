# BeChad agent instructions

## Structure
- `android/` Kotlin Android app (single `app` module) using Compose, Room, Retrofit, Hilt-ready package layout.
- `backend/` FastAPI modular monolith with SQLAlchemy 2, Alembic, PostgreSQL support.
- `infra/`, `scripts/`, `.github/workflows/` deployment and CI.

## Commands
- `make setup` prepares local tooling.
- `make dev` starts Docker Compose.
- `make backend-test` runs backend tests.
- `make android-test` runs JVM tests.
- `make lint` runs backend lint and Android lint where possible.
- `make apk` builds `android/app/build/outputs/apk/debug/bechad-debug.apk`.
- `make check` runs safe full checks.
- `make deploy` runs deployment script.

## Rules
- Never commit secrets, signing keystores, tokens, real production passwords, or `google-services.json`.
- Update `PROGRESS.md` after significant stages and before finishing.
- Keep BeChad naming consistent; Android app id is `com.bechad.app`.
- Backend XP is authoritative; Android may estimate UI state but must sync idempotently.
- Camera/video stays local; backend receives only aggregate exercise session metadata.
- Prefer deterministic local logic for demo/onboarding; no external AI is required.
- Before completion run formatting/lint/tests/builds that the environment supports and document failures honestly.
