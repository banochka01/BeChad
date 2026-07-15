setup:
	./scripts/codex-setup.sh
dev:
	./scripts/dev.sh
backend-test:
	cd backend && python -m pytest
android-test:
	cd android && ./gradlew testDebugUnitTest
lint:
	cd backend && python -m ruff check app tests
build:
	docker compose build
apk:
	cd android && ./gradlew assembleDebug
check:
	./scripts/check.sh
deploy:
	./scripts/deploy.sh
