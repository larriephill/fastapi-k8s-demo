# fastapi-k8s-demo

A tiny FastAPI service to learn DevOps fundamentals:
- Docker containerization
- Kubernetes (kind/minikube)
- Ingress for external access
- Horizontal Pod Autoscaler (HPA)
- CI/CD with GitHub Actions

## Local Dev
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

## Docker
docker build -t fastapi-k8s-demo:dev .
docker run --rm -p 8000:8000 fastapi-k8s-demo:dev
curl -s http://localhost:8000/healthz
