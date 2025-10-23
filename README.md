# Containerized FastAPI App on Kubernetes with Ingress, HPA & GitHub Actions

A fully containerized **FastAPI** application deployed on **Kubernetes**, showcasing real-world **DevOps fundamentals** — containerization, orchestration, scaling, and CI/CD automation.

This project demonstrates how code moves from **commit → build → deploy → scale** automatically using **Docker**, **Helm**, **Kubernetes**, and **GitHub Actions**.  
It was built to simulate production-grade DevOps workflows — end to end — on a local **kind cluster** (Kubernetes-in-Docker).

---

## Project Overview

**Goal:**  
To deploy a FastAPI app on Kubernetes using a modern DevOps toolchain:

- **Docker** for containerization  
- **Kubernetes (kind)** for orchestration  
- **Helm** for packaging and configuration management  
- **GitHub Actions** for automated CI/CD  
- **NGINX Ingress** for external access  
- **Horizontal Pod Autoscaler (HPA)** for dynamic scaling  
- **Metrics-Server** for resource monitoring  

This project mirrors the type of DevOps workflow used in real cloud environments (EKS, AKS, GKE), but runs locally in **WSL2 + Docker Desktop**, providing a portable and cost-free lab.

---

## System Design

### Flow

1. Developer pushes code → GitHub.
2. **GitHub Actions** runs tests → builds Docker image → pushes it to **GHCR** (GitHub Container Registry).
3. A **self-hosted GitHub runner** deploys the new image to the **kind cluster** via Helm.
4. Kubernetes runs the FastAPI app as a **Deployment**, exposes it through a **Service**, and routes traffic using **NGINX Ingress**.
5. **HPA** scales pods dynamically based on CPU usage.
6. The app is available locally at `http://fastapi.local:8080/healthz`.
   <img width="940" height="53" alt="image" src="https://github.com/user-attachments/assets/735c94ce-742e-4efa-bbaf-b53ea75f9f66" />

   

---

## Architecture Diagram

```
GitHub → GitHub Actions → GHCR (Image Registry)
     ↘
      Self-hosted Runner → kind Cluster (Kubernetes)
           ↘
            Helm Chart (Deployment + Service + Ingress + HPA)
                 ↘
                  FastAPI Pods → Browser via fastapi.local
```
<img width="1536" height="1024" alt="architectural diagram" src="https://github.com/user-attachments/assets/e5e57dba-ff8e-4039-a4f4-f6e0ba04c0ca" />


---

## Tech Stack

| Category | Tools / Technologies |
|-----------|----------------------|
| **Language & Framework** | Python 3.12, FastAPI |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes (kind) |
| **Configuration Management** | Helm |
| **CI/CD** | GitHub Actions |
| **Autoscaling** | Horizontal Pod Autoscaler (HPA) |
| **Ingress** | NGINX Ingress Controller |
| **Registry** | GitHub Container Registry (GHCR) |
| **Monitoring** | kubectl top, kubectl logs, metrics-server |
| **Environment** | WSL2 Ubuntu + Docker Desktop |

---

## Core Components

### FastAPI Application
Simple REST API with:
- `/healthz` → health check endpoint  
- `/burn` → CPU load generator (used for HPA testing)

### Dockerfile
Lightweight image build using a non-root user for improved security.

### Kubernetes Manifests (`/k8s`)
Base YAMLs for Deployment, Service, Ingress, ConfigMap, Secret, and HPA — used for local testing before Helm packaging.

### Helm Chart (`/helm/fastapi`)
Reusable Helm chart supporting variable overrides (replicas, image tags, etc.) for different environments.

### CI/CD Workflow (`.github/workflows/ci.yml`)
- Runs **pytest** on every commit  
- Builds & pushes images to **GHCR** (`latest` + short commit SHA)  
- Deploys to the cluster automatically via Helm upgrade  

### Ingress & Local DNS
Traffic routed through **NGINX Ingress Controller** and mapped via `/etc/hosts`:
```
127.0.0.1 fastapi.local
```
Accessible at [http://fastapi.local:8080/healthz](http://fastapi.local:8080/healthz).
<img width="897" height="268" alt="image" src="https://github.com/user-attachments/assets/59522a6c-91d4-4733-ae2d-da1ce20355db" />




### Autoscaling
HPA dynamically scales pods between 1 and 5 replicas based on CPU utilization.
<img width="940" height="104" alt="image" src="https://github.com/user-attachments/assets/a373f056-29d0-4757-b088-710e3bb53471" />

---

## Key DevOps Concepts Demonstrated

- **Containerization** – Packaging the app for consistent deployment across environments  
- **Infrastructure as Code** – Declarative Kubernetes manifests & Helm  
- **Continuous Integration** – Automated testing & image building  
- **Continuous Delivery** – Auto-deployments via GitHub Actions + Helm  
- **Observability** – Metrics-server, `kubectl top`, and live logs  
- **Scalability** – HPA automatically resizing the workload  
- **Security** – Principle of least privilege for CI/CD runner & non-root containers  

---

## Project Outcome

- FastAPI app deployed successfully to local Kubernetes (kind)  
- External access via `fastapi.local` through NGINX Ingress  
- CI/CD pipeline automatically builds and deploys from GitHub  
- HPA scales pods dynamically (1-5 replicas based on load)  
- Production-ready Helm chart reusable for EKS/GKE/AKS  
- Demonstrates hands-on mastery of **core DevOps workflows**

---

## Repository Structure

```
fastapi-k8s-demo/
├── app/
│   └── main.py                  # FastAPI app (healthz, burn)
├── helm/fastapi/                # Helm chart for K8s deployment
│   ├── templates/               # Deployment, Service, Ingress, HPA, etc.
│   └── values.yaml
├── k8s/                         # Raw manifests (for testing)
├── tests/                       # Pytest unit tests
├── Dockerfile
├── kind-config.yaml             # Local cluster config
├── .github/workflows/ci.yml     # CI/CD pipeline
└── README.md
```

---

## Future Enhancements

To take this project closer to production-grade, I plan to:
- Add **Prometheus + Grafana** for full observability  
- Integrate **OpenAPI docs** for API visibility  
- Deploy to a managed Kubernetes service (e.g., AWS EKS)  
- Introduce **GitOps** with ArgoCD or FluxCD  
- Expand automated testing coverage and security scanning  

---

## Author

**Oluwaseyi Philip Abiola**  
  London, UK  
  DevOps Engineer (in progress)  

 **GitHub:** [Larriephill](https://github.com/Larriephill)  
**LinkedIn:** [philipabiola](https://www.linkedin.com/in/philipabiola)

---

## License

This project is released under the **MIT License**.  
© 2025 Oluwaseyi Abiola. All rights reserved.

---

> *This repository demonstrates continuous growth across my DevOps journey — from my previous [AWS Serverless URL Shortener](https://github.com/Larriephill/url-shortener) (IaC + AWS + CI/CD) to this Kubernetes-based FastAPI deployment (Docker + Helm + Autoscaling). It demonstrates my hands-on commitment to mastering cloud-native DevOps engineering.*
