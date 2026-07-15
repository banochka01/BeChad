# Decisions

- Use Kotlin Serialization consistently for Android/backend DTO naming alignment.
- Keep Android as a single app module with package folders (`core`, `data`, `domain`, `feature`, `designsystem`, `sync`, `camera`) to avoid MVP module overhead.
- Backend is a FastAPI modular monolith using SQLAlchemy 2 and Alembic; XP events are immutable and progress is updated transactionally.
- Rule-based coach is the default; OpenAI is server-only behind `OPENAI_API_KEY` and `OPENAI_COACH_ENABLED`.
- Google sign-in, FCM, Health Connect, Duolingo adapter are feature-flagged so debug builds work without credentials.
- Guest/demo mode is local-first; account linking is represented as an explicit sync/migration operation.
- Exercise recognition is split into camera UI and pure pose state machines for testability.
