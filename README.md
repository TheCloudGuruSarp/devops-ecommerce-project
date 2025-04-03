# DevOps E-commerce Project

## Overview
This project demonstrates a complete DevOps pipeline for an e-commerce application, including CI/CD, infrastructure as code, containerization, and monitoring.

## Features
- Containerized Flask API for e-commerce operations
- Infrastructure as Code using Terraform
- Kubernetes deployment manifests
- CI/CD pipeline with GitHub Actions
- Monitoring with Prometheus and Grafana

## Architecture
The application follows a microservices architecture with the following components:
- **Backend API**: Flask-based RESTful API
- **Database**: MongoDB for product and order storage
- **Infrastructure**: AWS EKS for Kubernetes orchestration
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Monitoring**: Prometheus and Grafana for metrics and visualization

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Kubernetes CLI (kubectl)
- Terraform
- AWS CLI configured with appropriate permissions

### Local Development
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/devops-ecommerce-project.git
   cd devops-ecommerce-project
   ```

2. Build and run the application locally
   ```bash
   docker-compose up --build
   ```

3. Access the API at http://localhost:5000

### Deployment

#### Infrastructure Setup
1. Initialize Terraform
   ```bash
   cd infrastructure
   terraform init
   ```

2. Apply Terraform configuration
   ```bash
   terraform apply
   ```

#### Kubernetes Deployment
1. Update kubeconfig
   ```bash
   aws eks update-kubeconfig --name ecommerce-cluster --region us-west-2
   ```

2. Deploy the application
   ```bash
   kubectl apply -f k8s/
   ```

## CI/CD Pipeline
The project includes a GitHub Actions workflow that:
1. Runs tests on pull requests
2. Builds and pushes Docker images on merge to main
3. Deploys to Kubernetes using a rolling update strategy

## Monitoring
The monitoring stack includes:
- Prometheus for metrics collection
- Grafana for visualization
- AlertManager for alerting

Access Grafana at http://grafana.your-domain.com (after deployment)

## Project Structure
```
 app/                  # Application code
 infrastructure/       # Terraform IaC
 k8s/                  # Kubernetes manifests
 .github/workflows/    # CI/CD pipeline
 monitoring/           # Prometheus and Grafana configs
 docker-compose.yml    # Local development setup
```

## License
MIT

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
