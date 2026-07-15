# BeChad

BeChad is an MVP Android + FastAPI product for gamified self-improvement: onboarding creates a deterministic 7-day plan, users complete quests, backend awards XP, streaks and achievements, and the app can run in local demo mode.

## Quick start backend
```bash
cp .env.example .env
./scripts/deploy.sh
```
Open `http://localhost:8000/health` and `http://localhost:8000/api/v1/openapi.json`.

## Android
```bash
cd android
./gradlew assembleDebug
```
Debug APK artifact path in CI is `artifacts/bechad-debug.apk`; local Gradle output is `android/app/build/outputs/apk/debug/app-debug.apk` (copy/rename to `bechad-debug.apk` in CI).

## Make commands
- `make setup` installs backend dependencies and checks SDK tooling.
- `make backend-test` runs Pytest.
- `make android-test` runs JVM tests.
- `make apk` builds debug APK.
- `make check` runs backend tests, Ruff, Android tests and debug assembly.
- `make deploy` starts Docker Compose.

## Feature flags and secrets
All optional integrations are disabled unless configured in `.env`: OpenAI coach, Google auth, FCM, Duolingo adapter. Never commit real secrets, keystores, `google-services.json`, or production passwords.

## Codex Cloud setup
Use `./scripts/codex-setup.sh` during environment setup to prepare Python dependencies and Android SDK components when `sdkmanager` is available.

## APK from GitHub Actions on phone
Open the repository Actions tab, choose a successful CI run, download `bechad-debug-apk`, unzip it on the phone, and install `bechad-debug.apk` after allowing installs from the browser/files app.
