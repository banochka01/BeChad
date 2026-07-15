# Architecture
Android is a single Kotlin/Compose app using domain rules and pure camera analyzers that are testable without a device. Backend is a FastAPI modular monolith backed by SQLAlchemy models and PostgreSQL in Docker. XP events are append-only and idempotency keys prevent duplicate quest rewards. Optional providers are behind flags.
