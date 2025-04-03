# DevOps E-commerce Project

✨ **Developed by Sarper** ✨

---

![DevOps Pipeline](https://img.shields.io/badge/DevOps-Pipeline-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-brightgreen)
![Terraform](https://img.shields.io/badge/Infrastructure-Terraform-purple)
![Monitoring](https://img.shields.io/badge/Monitoring-Prometheus-orange)

## About the Project

This project demonstrates the development, deployment, and management of a simple e-commerce application using modern DevOps practices. The project includes CI/CD pipelines, containerization, infrastructure management, and monitoring solutions.

## Project Components

### 1. Application
- Simple e-commerce API developed with Flask
- Features for product listing, order creation, and user management
- Containerized with Docker
- RESTful API design

### 2. Infrastructure Management (Terraform)
- Kubernetes Cluster (EKS) creation
- Load Balancer (AWS ALB) configuration
- S3 bucket creation (for static files and backups)
- IAM roles and permissions
- Modular Terraform structure

### 3. CI/CD Pipeline (GitHub Actions)
- Automated testing and build processes
- Docker image creation and pushing to ECR
- Automated deployment to Kubernetes
- Canary deployment strategy

### 4. Kubernetes Orchestration
- Deployment, Service, and Ingress configurations
- ConfigMap and Secret management
- Horizontal Pod Autoscaler (HPA) for automatic scaling
- NGINX Ingress Controller

### 5. Monitoring and Logging
- Metric collection with Prometheus
- Visualization with Grafana
- Alert management with Alertmanager
- Log management with Loki

## Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  GitHub Actions │────▶│  ECR Registry  │────▶│  EKS Cluster    │
│  (CI/CD)        │     │  (Container)   │     │  (Orchestration)│
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐                             ┌─────────────────┐
│                 │                             │                 │
│  Terraform      │─────────────────────────────│  AWS Services   │
│  (IaC)          │                             │  (Cloud Infra)  │
│                 │                             │                 │
└─────────────────┘                             └─────────────────┘
                                                         ▲
                                                         │
                                                ┌────────┴────────┐
                                                │                 │
                                                │  Prometheus     │
                                                │  Grafana        │
                                                │  (Monitoring)   │
                                                │                 │
                                                └─────────────────┘
```

## Setup and Running

### Prerequisites
- Docker and Docker Compose
- Kubernetes CLI (kubectl)
- Terraform
- AWS CLI
- Python 3.8+

### Local Development

```bash
# Run the application locally
cd app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Run with Docker
docker build -t ecommerce-api:latest .
docker run -p 5000:5000 ecommerce-api:latest
```

### Infrastructure Creation

```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

### Kubernetes Deployment

```bash
cd k8s
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
kubectl apply -f hpa.yaml
```

### Monitoring Setup

```bash
cd monitoring
kubectl apply -f prometheus/
kubectl apply -f grafana/
```

## CI/CD Pipeline

The GitHub Actions pipeline automatically performs the following steps:

1. Runs tests when code changes are pushed
2. Creates a Docker image if tests are successful
3. Pushes the image to ECR
4. Updates Kubernetes manifest files
5. Deploys the application to Kubernetes

## Monitoring

### Grafana Dashboards

The project includes comprehensive Grafana dashboards for monitoring the health of the Kubernetes cluster and the application.

### Prometheus Alerts

Example alert rules:
- High CPU usage (>80%)
- High memory usage (>80%)
- High error rate (>5%)
- Service response time (>2s)

## Project Structure

```
├── app/                    # Application code
│   ├── api/                # API endpoints
│   ├── models/             # Data models
│   ├── tests/              # Unit tests
│   ├── Dockerfile          # Application container configuration
│   └── requirements.txt    # Python dependencies
│
├── infrastructure/         # Terraform code
│   ├── modules/            # Terraform modules
│   │   ├── eks/           # EKS cluster module
│   │   ├── networking/    # VPC, subnet, etc.
│   │   └── storage/       # S3 bucket module
│   ├── main.tf            # Main Terraform configuration
│   └── variables.tf       # Terraform variables
│
├── k8s/                    # Kubernetes manifest files
│   ├── deployment.yaml     # Application deployment
│   ├── service.yaml        # Service configuration
│   ├── ingress.yaml        # Ingress configuration
│   ├── configmap.yaml      # Configuration values
│   ├── secret.yaml         # Secret values
│   └── hpa.yaml            # Horizontal Pod Autoscaler
│
├── .github/workflows/      # GitHub Actions workflow files
│   ├── ci.yaml             # Continuous Integration
│   └── cd.yaml             # Continuous Deployment
│
└── monitoring/             # Monitoring configurations
    ├── prometheus/         # Prometheus configuration
    ├── grafana/            # Grafana dashboards
    └── alertmanager/       # Alert rules
```

## Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push your branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Project Owner - [Sarper](https://github.com/TheCloudGuruSarp)

Project Link: [https://github.com/TheCloudGuruSarp/devops-ecommerce-project](https://github.com/TheCloudGuruSarp/devops-ecommerce-project)
