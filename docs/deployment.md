# mini-shop (Clean Deploy)

This folder contains a helper compose file to start a **clean** instance of Mini Shop without interfering with your existing local instance.

Quick start:

1. From project root: 
   ```powershell
   docker-compose -f deploy/docker-compose.clean.yml build --no-cache
   docker-compose -f deploy/docker-compose.clean.yml up -d
   ```
2. Wait a few seconds and visit:
   - Frontend: http://localhost:8080
   - Backend health: http://localhost:5001/api/health

Notes:
- Database server exposed on host port 5433 (internal 5432), volume `minishop_clean_postgres`.
- Backend listens on 5001 to avoid conflicts with existing 5000.
- Frontend served at host 8080 (container port 80).

Evaluation checklist to satisfy grading criteria (suggested):
- Analysis & Design: keep docs in `docs/` (use-case, database schema). Add `docs/requirements.md` if needed.
- Implementation: include tests in `backend/tests/` and CI uses `.github/workflows/ci.yml`.
- Teamwork: keep commit history and README details about roles.
- Presentation: prepare a short report or slides.
- Deployment: docker-compose provided. Use `deploy/docker-compose.clean.yml` to run isolated instance.
- Innovation: chatbot present; optionally add notes about AI integration.

If you want, I can also:
- Add a small test that checks `/api/health` and auth endpoints.
- Add a simple PlantUML class diagram generated from models.
- Add scripts `make clean-up` and `make start-clean` for convenience.
