# FinTrack

> Simple personal finance tracker built with Flask and SQLite. Provides a minimal UI to add income/expense entries and view a monthly summary chart.

## Project structure

- `app.py` — Flask application and routes
- `models.py` — SQLAlchemy models (`Entry`)
- `utils.py` — helper functions (monthly summary)
- `templates/` — Jinja2 templates (`base.html`, `index.html`, `add_entry.html`, `report.html`)
- `instance/database.db` — default SQLite database (created/used locally)
- `requirements.txt` — Python dependencies
- `Dockerfile` — container image definition (Gunicorn + Flask)
- `.dockerignore` — ignores files from Docker build context

## Quick notes

- The app uses environment variables for configuration. Defaults make it easy to run locally with SQLite.
- For production, replace SQLite with a managed database (Postgres) and set secure `SECRET_KEY`.

## Environment variables

- `SQLALCHEMY_DATABASE_URI` or `DATABASE_URL` — SQLAlchemy DB URI (default: `sqlite:///database.db`)
- `SECRET_KEY` — Flask secret key (default: `dev-secret`)
- `HOST` — host to bind when running `app.py` directly (default: `0.0.0.0`)
- `PORT` — port to bind when running `app.py` directly (default: `5000`)
- `FLASK_DEBUG` — enable debug when running via `app.py` (set to `1`, `true`, or `yes`)

## Run locally (Python)

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Run the app:

```powershell
# create instance folder and DB if needed
python app.py
# or explicitly set host/port
$env:SECRET_KEY='replace-me'; $env:SQLALCHEMY_DATABASE_URI='sqlite:///instance/database.db'; python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Run with Gunicorn (local production-like)

```powershell
# from project root
$env:SECRET_KEY='replace-me'; $env:SQLALCHEMY_DATABASE_URI='sqlite:///instance/database.db'
gunicorn --bind 0.0.0.0:8000 app:app
```

## Docker (recommended for deployment)

Build image:

```powershell
cd D:\CODING\PYTHON\fintrack
docker build -t fintrack-app:local .
```

Run container (expose port 8000):

```powershell
docker run --rm -e SECRET_KEY=replace-me -e SQLALCHEMY_DATABASE_URI="sqlite:///database.db" -p 8000:8000 fintrack-app:local
```

Persist the SQLite file on host (optional):

```powershell
# mounts database.db from current folder into container
docker run --rm -v ${PWD}\\instance\\database.db:/app/instance/database.db -e SECRET_KEY=replace-me -e SQLALCHEMY_DATABASE_URI="sqlite:///instance/database.db" -p 8000:8000 fintrack-app:local
```

Open http://localhost:8000.

## Deploying the container to a cloud host

You can push the Docker image to Docker Hub and deploy to any container host (Render, Fly, Cloud Run, etc.). Key steps:

1. Build image and push to registry (example with Docker Hub):

```powershell
docker tag fintrack-app:local your-dockerhub-user/fintrack-app:latest
docker push your-dockerhub-user/fintrack-app:latest
```

2. Create a service on your chosen host and set environment variables (`SECRET_KEY`, `DATABASE_URL` for Postgres if using one).

Notes: For production, use a managed Postgres database and set `SQLALCHEMY_DATABASE_URI` to the provided connection string. Remove any local SQLite bindings.

## Database and migrations

- This project currently uses a simple `db.create_all()` on startup. For any non-trivial project, add `Flask-Migrate` (Alembic) for schema migrations.

## Security & production recommendations

- Do not commit secrets. Use platform-managed secrets or environment variables.
- Use HTTPS in production (platforms like Render/Fly provide TLS automatically).
- Move from SQLite to Postgres/MySQL for reliability and concurrency.
- Add logging, error reporting, and access controls as needed.

## Future improvements

- Add tests and CI (GitHub Actions) to run linting and tests.
- Add `Flask-Migrate` and migration scripts.
- Add user authentication if you want multi-user support.
- Add input validation and CSRF protection for forms.

## Contact / License

Small personal project. Add a license file to the repo if you want to publish it publicly.

