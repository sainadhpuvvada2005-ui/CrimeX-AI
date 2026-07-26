Deployment notes and commands for Zoho Catalyst AppSail and Docker

Prerequisites
- Python 3.11
- Node.js 20.x (recommended for Next.js 15 + React 19)
- Docker (for container builds)
- Zoho Catalyst CLI / AppSail access

Backend (local test)
1. Create Python 3.11 venv and activate:

```powershell
python3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Upgrade pip and install dependencies:

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install --prefer-binary -r requirements.txt
```

3. Run the FastAPI app (dev/test):

```powershell
$env:PORT=8000
python -m uvicorn app.main:app --host 0.0.0.0 --port $env:PORT
```

Docker (build image)

```powershell
docker build -t crimex-api:prod .
docker run -e PORT=8000 -p 8000:8000 crimex-api:prod
```

Next.js frontend (build)

```bash
cd frontend
# Use Node 20.x - install dependencies
npm ci
npm run build
npm run start
```

Zoho Catalyst (AppSail)
- Use `appsail-config.json` in `backend/` as the basis for AppSail deployment.
- Replace environment placeholders in `backend/.env.production` and upload secrets to Catalyst secure store.

Example Catalyst deploy steps (conceptual):

1. Package frontend and deploy via Catalyst AppSail or static hosting.
2. For backend, ensure runtime is Python 3.11 and install dependencies from `requirements.txt`.
3. Configure Catalyst environment variables and secrets (DATABASE_URL, JWT_SECRET_KEY, OPENAI_API_KEY, CACHE_URL, STRATUS_BUCKET, QUICKML_MODEL, FRONTEND_URL, BACKEND_URL, PORT).
4. Deploy and verify health endpoint: `GET /api/v1/health`.

Verification
- API health: `curl https://<backend-url>/api/v1/health`
- Frontend: visit `FRONTEND_URL` after deployment.
- Logs: review Catalyst/AppSail logs for startup traces.

Notes
- The `requirements.txt` has been adjusted for Python 3.11 compatibility.
- For production workloads, consider running the app under a process manager or behind a WSGI/ASGI server suited for multi-worker scaling.
