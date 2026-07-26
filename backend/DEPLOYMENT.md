# Backend Deployment Instructions (Python 3.11)

This guide provides the steps to set up the backend environment for the CrimeX AI application using Python 3.11.

## 1. Prerequisites

- Python 3.11 installed and available in your system's PATH.

## 2. Create and Activate Virtual Environment

First, create a virtual environment to isolate the project dependencies.

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment named .venv
python -m venv .venv
```

Next, activate the virtual environment.

**On Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

## 3. Upgrade Pip

Ensure you have the latest version of pip:
```bash
python -m pip install --upgrade pip
```

## 4. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## 5. Verification

To verify that all dependencies are installed correctly, you can list the installed packages and check for the key libraries.

```bash
pip list
```

Ensure that `fastapi`, `uvicorn`, `SQLAlchemy`, and `faiss-cpu` are present in the list.
