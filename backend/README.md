# CrimeX AI FastAPI Backend

Production-oriented FastAPI backend for CrimeX AI.

## Modules

- Authentication with JWT
- Dashboard
- Case Management
- Victim search
- Accused search
- Crime Analytics
- Prediction
- Reports
- Voice
- Chatbot
- Neo4j network analysis

## Database Rule

The official Karnataka Police FIR tables are not created or modified by the backend.

Official tables are reflected at runtime from PostgreSQL:

- `CaseMaster`
- `Victim`
- `Accused`
- `ComplainantDetails`
- `ActSectionAssociation`
- `ArrestSurrender`
- `ChargesheetDetails`
- `CrimeHead`
- `CrimeSubHead`
- `Court`
- `District`
- `State`
- `Unit`
- `Employee`
- `CaseCategory`
- `GravityOffence`
- `Act`
- `Section`

The backend ORM defines only CrimeX-owned AI tables:

- `crimex_ai."ConversationHistory"`
- `crimex_ai."PredictionLogs"`
- `crimex_ai."AuditLogs"`
- `crimex_ai."UserSessions"`

Run the SQL scripts in `../database/postgresql` before using AI logging features.

## Local Run

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

Development login:

```json
{
  "username": "admin",
  "password": "dev-password"
}
```

Production must connect `AuthService` to the police SSO/IdP.

## Docker

```bash
cd backend
cp .env.example .env
docker compose up --build
```

## Catalyst Integration

The backend now includes lightweight Catalyst-compatible adapters for authentication, data-store persistence, NoSQL collections, Stratus-style storage, cache, Signals/Circuits, and deployment manifests. These are designed to preserve the current FastAPI behavior while providing a migration path to Zoho Catalyst services.

## Notes

- Search and filtering are generic because the exact official ERD column list is not present in this repository.
- The official table repository reflects real columns from PostgreSQL and applies filters only to fields that exist.
- Prediction, voice, report generation, and LLM orchestration contain safe integration stubs ready for approved providers/models.

