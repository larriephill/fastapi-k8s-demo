import os, time
import logging, json, sys
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest

# --- Structured JSON Logging ---
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
        }
        return json.dumps(log_record)

def setup_json_logging():
    formatter = JsonFormatter()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Force Uvicorn loggers to use our handler
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.addHandler(handler)
        logger.propagate = False
        logger.setLevel(logging.INFO)

app = FastAPI(title="fastapi-k8s-demo")

# Make sure logging is configured once the app starts
@app.on_event("startup")
async def init_logging():
    setup_json_logging()

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
APP_MESSAGE = os.getenv("APP_MESSAGE", "Hello from ConfigMap 👋")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

REQUEST_COUNT = Counter("http_requests_total", "Total number of HTTP requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Histogram of request latency (seconds)", ["endpoint"])

@app.middleware("http")
async def track_metrics(request: Request, call_next):
    t0 = time.time()
    resp = await call_next(request)
    dt = time.time() - t0
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(dt)
    resp.headers["X-Process-Time"] = str(round(dt, 4))
    return resp

@app.get("/")
def root():
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
    return {"message": APP_MESSAGE, "version": APP_VERSION, "has_secret": bool(SECRET_TOKEN)}

@app.get("/secret-check")
def secret_check(authorization: str | None = Header(default=None)):
    if not SECRET_TOKEN:
        raise HTTPException(status_code=500, detail="Secret not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"status": "ok", "msg": "Secret verified"}

# Force text/plain exposition explicitly
@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest()

