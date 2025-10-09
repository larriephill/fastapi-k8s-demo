from fastapi import FastAPI
import os, time

app = FastAPI(title="fastapi-k8s-demo")

@app.get("/")
def read_root():
    return {"service": "fastapi-k8s-demo", "version": os.getenv("APP_VERSION", "0.1.0")}

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
