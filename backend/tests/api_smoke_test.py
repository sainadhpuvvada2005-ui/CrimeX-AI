import requests

BASE = "http://127.0.0.1:8002"

endpoints = [
    ("GET", "/api/v1/health"),
    ("GET", "/api/v1/openapi.json"),
    ("GET", "/docs"),
]

print("Starting API smoke tests against:", BASE)
for method, path in endpoints:
    url = BASE + path
    try:
        resp = requests.request(method, url, timeout=5)
        print(f"{method} {path} -> {resp.status_code}")
    except Exception as e:
        print(f"{method} {path} -> ERROR: {e}")

# Attempt developer login
login_url = BASE + "/api/v1/auth/login"
payload = {"username": "admin", "password": "dev-password"}
try:
    r = requests.post(login_url, json=payload, timeout=5)
    print("POST /api/v1/auth/login ->", r.status_code, r.text)
    if r.status_code == 200:
        tokens = r.json()
        access = tokens.get("access_token")
        if access:
            refresh_url = BASE + "/api/v1/auth/refresh"
            r2 = requests.post(refresh_url, json={"access_token": access}, timeout=5)
            print("POST /api/v1/auth/refresh ->", r2.status_code, r2.text)
except Exception as e:
    print("Login -> ERROR:", e)
