from fastapi import FastAPI, Header, HTTPException
import os, time

app = FastAPI(title="fastapi-k8s-demo")

# Read config/secrets from env (with safe defaults if missing)
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
APP_MESSAGE = os.getenv("APP_MESSAGE", "Hello from ConfigMap 👋")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")  # do not default secrets!

@app.get("/")
def read_root():
    return {"service": "fastapi-k8s-demo", "version": APP_VERSION}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/burn")
def burn(seconds: float = 0.5):
    end = time.time() + seconds
    x = 0
    while time.time() < end:
        x += 1
    return {"burn_seconds": seconds, "iterations": x}

@app.get("/config")
def get_config():
    # Do NOT return secrets; just show non-sensitive config
    return {
        "message": APP_MESSAGE,
        "version": APP_VERSION,
        "has_secret": bool(SECRET_TOKEN)  # True/False only
    }

@app.get("/secret-check")
def secret_check(authorization: str | None = Header(default=None)):
    # Basic demonstration: expect header 'Authorization: Bearer <SECRET_TOKEN>'
    if not SECRET_TOKEN:
        raise HTTPException(status_code=500, detail="Secret not configured")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ", 1)[1]
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")

    return {"status": "ok", "msg": "Secret verified"}

