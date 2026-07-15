# Security
Passwords are hashed with Argon2. JWT access tokens are short-lived and refresh tokens are hash-stored and rotatable/revocable. Production CORS must use explicit origins. Do not log passwords or bearer tokens. Optional OpenAI keys stay on backend only. CI runs lint/tests and Docker image build.
