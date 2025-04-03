# DevOps E-commerce Project

✨ **Developed by Sarper** ✨

---

![DevOps Pipeline](https://img.shields.io/badge/DevOps-Pipeline-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-brightgreen)
![Terraform](https://img.shields.io/badge/Infrastructure-Terraform-purple)
![Monitoring](https://img.shields.io/badge/Monitoring-Prometheus-orange)

## About the Project

This comprehensive project demonstrates the end-to-end development, deployment, and management of a scalable e-commerce application using modern DevOps methodologies and cloud-native technologies. The implementation showcases industry best practices for continuous integration and delivery, containerization, infrastructure as code, Kubernetes orchestration, and observability solutions.

## Project Components

### 1. Application Architecture
- Microservices-based e-commerce platform developed with Flask and Python 3.9
- RESTful API design with OpenAPI/Swagger documentation
- Core services include product catalog, inventory management, order processing, and user authentication
- Domain-driven design principles with clear service boundaries
- Containerized with multi-stage Docker builds for optimized image size
- Stateless design for horizontal scalability

### 2. Infrastructure as Code (Terraform)
- Declarative infrastructure definition using HashiCorp Terraform v1.0+
- AWS EKS cluster provisioning with node groups and auto-scaling configurations
- Network architecture with VPC, subnets, and security groups following AWS best practices
- Application Load Balancer (ALB) with TLS termination and web application firewall integration
- S3 buckets with appropriate lifecycle policies for static assets and database backups
- IAM roles and policies implementing principle of least privilege
- DynamoDB tables for application data with on-demand capacity
- Modular Terraform structure with reusable modules and remote state management
- Terraform Cloud integration for collaborative infrastructure management

### 3. CI/CD Pipeline (GitHub Actions)
- Comprehensive continuous integration and delivery pipeline using GitHub Actions
- Multi-stage workflow with parallel execution for efficiency
- Automated unit, integration, and end-to-end testing with detailed reporting
- Static code analysis and security scanning with SonarQube and Snyk
- Semantic versioning of artifacts with automated changelog generation
- Docker image building, scanning, and publishing to Amazon ECR
- Infrastructure validation using Terraform plan in CI pipeline
- GitOps approach with ArgoCD for Kubernetes deployments
- Progressive delivery with canary and blue-green deployment strategies
- Automated rollback mechanisms based on health metrics

### 4. Kubernetes Orchestration
- Production-grade Kubernetes configuration with declarative manifests
- Namespace isolation with resource quotas and network policies
- Deployment strategies with rolling updates and readiness gates
- Service mesh implementation with Istio for advanced traffic management
- External-DNS integration for automatic DNS record management
- Cert-Manager for automated TLS certificate provisioning and renewal
- ConfigMap and Secret management with external secrets integration
- Horizontal Pod Autoscaler (HPA) with custom metrics from Prometheus
- NGINX Ingress Controller with rate limiting and WAF capabilities
- StatefulSets for stateful components with persistent volume claims
- CronJobs for scheduled maintenance tasks and data processing

### 5. Observability Stack
- Comprehensive monitoring with Prometheus for metrics collection and storage
- Custom instrumentation of application code with Prometheus client libraries
- RED method monitoring (Request rate, Error rate, and Duration)
- Grafana dashboards with business and technical KPIs
- Multi-dimensional alerting with Alertmanager
- PagerDuty integration for on-call notification
- Distributed tracing with Jaeger for request flow visualization
- Centralized logging with Loki and structured JSON log format
- Log aggregation and analysis with Elasticsearch, Fluentd, and Kibana (EFK stack)
- Service level objectives (SLOs) and error budgets tracking
- Synthetic monitoring for critical user journeys

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
- Docker Engine (20.10+) and Docker Compose (v2.0+)
- Kubernetes CLI (kubectl v1.22+) configured to access your cluster
- Terraform (v1.0+) with AWS provider
- AWS CLI (v2.0+) configured with appropriate IAM permissions
- Python 3.9+ with virtualenv or conda for local development
- Helm (v3.0+) for Kubernetes package management
- ArgoCD CLI for GitOps deployments
- AWS IAM Authenticator for EKS authentication

### Local Development Environment

```bash
# Clone the repository
git clone https://github.com/TheCloudGuruSarp/devops-ecommerce-project.git
cd devops-ecommerce-project

# Set up Python virtual environment
cd app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Run tests
python -m pytest tests/ --cov=app

# Run the application locally with hot-reloading
FLASK_ENV=development FLASK_DEBUG=1 python app.py

# Run with Docker Compose (includes dependencies like Redis and PostgreSQL)
cd ..
docker-compose up --build

# Access the application at http://localhost:5000
# API documentation available at http://localhost:5000/api/docs
```

### Infrastructure Provisioning

```bash
# Navigate to infrastructure directory
cd infrastructure

# Initialize Terraform with backend configuration
terraform init -backend-config=environments/dev/backend.hcl

# Select appropriate workspace
terraform workspace select dev  # Options: dev, staging, prod

# Validate configuration
terraform validate

# Plan the deployment with variables
terraform plan -var-file=environments/dev/terraform.tfvars -out=tfplan

# Review the plan output carefully

# Apply the infrastructure changes
terraform apply tfplan

# Configure kubectl to use the new EKS cluster
aws eks update-kubeconfig --name $(terraform output -raw eks_cluster_name) --region $(terraform output -raw aws_region)

# Verify connectivity to the cluster
kubectl get nodes
```

### Kubernetes Deployment

```bash
# Navigate to Kubernetes manifests directory
cd k8s

# Create namespace and apply RBAC configurations
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-rbac.yaml

# Apply ConfigMaps and Secrets
kubectl apply -f 02-configmap.yaml
kubectl apply -f 03-secrets.yaml

# Deploy database and cache (if not using managed services)
kubectl apply -f 04-database.yaml
kubectl apply -f 05-redis.yaml

# Deploy application components
kubectl apply -f 06-deployments/

# Create services
kubectl apply -f 07-services/

# Configure ingress and TLS
kubectl apply -f 08-ingress.yaml

# Apply autoscaling configuration
kubectl apply -f 09-hpa.yaml

# Verify deployment status
kubectl get pods -n ecommerce
kubectl get svc -n ecommerce
kubectl get ingress -n ecommerce

# For GitOps-based deployment with ArgoCD
cd ../argocd
argocd app create ecommerce-app -f application.yaml
argocd app sync ecommerce-app
```

### Observability Stack Deployment

```bash
# Navigate to monitoring directory
cd monitoring

# Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Create monitoring namespace
kubectl create namespace monitoring

# Deploy Prometheus Operator with CRDs
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values prometheus/values.yaml

# Deploy Loki for log aggregation
helm install loki grafana/loki-stack \
  --namespace monitoring \
  --values loki/values.yaml \
  --set grafana.enabled=false

# Deploy Jaeger for distributed tracing
kubectl apply -f jaeger/jaeger-operator.yaml
kubectl apply -f jaeger/jaeger-instance.yaml

# Apply custom Grafana dashboards
kubectl apply -f grafana/dashboards/

# Apply PrometheusRules for alerting
kubectl apply -f prometheus/rules/

# Apply ServiceMonitor resources for scraping metrics
kubectl apply -f prometheus/service-monitors/

# Verify monitoring stack deployment
kubectl get pods -n monitoring

# Port-forward to access Grafana locally
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring

# Access Grafana at http://localhost:3000 (default credentials: admin/prom-operator)
```

## CI/CD Pipeline Architecture

The project implements a sophisticated CI/CD pipeline using GitHub Actions that automates the entire software delivery process:

### Continuous Integration
1. **Code Quality Checks**: Triggered on pull requests to verify code quality
   - Linting with flake8, pylint, and black
   - Static code analysis with SonarQube
   - Security scanning with Snyk and Bandit
   - Dependency vulnerability scanning

2. **Automated Testing**: Comprehensive test suite execution
   - Unit tests with pytest and code coverage reporting
   - Integration tests with test containers
   - Contract tests for API endpoints
   - End-to-end tests with Cypress

3. **Build Process**: Triggered on merge to main branch
   - Multi-stage Docker builds with layer optimization
   - Image tagging with semantic versioning
   - Container image scanning with Trivy
   - Publishing to Amazon ECR with image signing

### Continuous Delivery
4. **Infrastructure Validation**:
   - Terraform plan generation and validation
   - Policy compliance checking with OPA/Conftest
   - Cost estimation for infrastructure changes

5. **Deployment Automation**:
   - Environment-specific configuration generation
   - Kubernetes manifest updates with kustomize
   - ArgoCD synchronization for GitOps deployment
   - Database schema migrations with safety checks

6. **Verification and Promotion**:
   - Smoke tests against newly deployed services
   - Canary analysis with progressive traffic shifting
   - Automated rollback on failure detection
   - Promotion to next environment upon success

## Observability Implementation

### Grafana Dashboards

The project includes a suite of purpose-built Grafana dashboards providing comprehensive visibility into system performance and business metrics:

- **Kubernetes Cluster Overview**: Resource utilization, node status, and control plane health
- **Application Performance**: Request rates, error rates, and latency percentiles (RED method)
- **Business Metrics**: Order volume, conversion rates, and revenue tracking
- **Database Performance**: Query performance, connection pools, and transaction rates
- **Service Mesh**: Request flows, retry rates, and circuit breaker status
- **User Experience**: Page load times, API response times, and error rates by endpoint

### Prometheus Alert Rules

The monitoring system includes carefully tuned alert rules with appropriate thresholds:

- **Infrastructure Alerts**:
  - High CPU utilization (>85% for 15 minutes)
  - High memory usage (>85% for 15 minutes)
  - Disk space running low (<10% free)
  - Node not ready or unreachable

- **Application Alerts**:
  - High error rate (>2% of requests over 5 minutes)
  - Elevated latency (95th percentile >500ms for 10 minutes)
  - Service availability below SLO (<99.9% over 1 hour)
  - Abnormal request rate (±50% from baseline)

- **Business Alerts**:
  - Order processing failures
  - Payment gateway connectivity issues
  - Inventory discrepancies
  - Unusual traffic patterns indicating potential security issues

## Project Structure

```
├── app/                              # Application source code
│   ├── api/                          # API endpoints and controllers
│   │   ├── v1/                      # API version 1 endpoints
│   │   │   ├── products.py          # Product endpoints
│   │   │   ├── orders.py            # Order endpoints
│   │   │   ├── users.py             # User endpoints
│   │   │   └── auth.py              # Authentication endpoints
│   │   └── openapi/                 # OpenAPI/Swagger documentation
│   ├── core/                         # Core application logic
│   │   ├── config.py                # Application configuration
│   │   ├── exceptions.py            # Custom exception handlers
│   │   ├── logging.py               # Logging configuration
│   │   └── middleware.py            # Request/response middleware
│   ├── models/                        # Data models and schemas
│   │   ├── product.py               # Product model
│   │   ├── order.py                 # Order model
│   │   ├── user.py                  # User model
│   │   └── base.py                  # Base model class
│   ├── services/                      # Business logic services
│   │   ├── product_service.py        # Product business logic
│   │   ├── order_service.py          # Order business logic
│   │   ├── user_service.py           # User business logic
│   │   └── auth_service.py           # Authentication service
│   ├── repositories/                  # Data access layer
│   │   ├── product_repository.py     # Product data access
│   │   ├── order_repository.py       # Order data access
│   │   ├── user_repository.py        # User data access
│   │   └── base_repository.py        # Base repository class
│   ├── tests/                         # Test suite
│   │   ├── unit/                     # Unit tests
│   │   ├── integration/              # Integration tests
│   │   ├── e2e/                      # End-to-end tests
│   │   └── fixtures/                 # Test fixtures
│   ├── Dockerfile                     # Multi-stage Docker build
│   ├── docker-compose.yml              # Local development environment
│   ├── requirements.txt                # Production dependencies
│   └── requirements-dev.txt            # Development dependencies
│
├── infrastructure/                     # Infrastructure as Code
│   ├── modules/                        # Reusable Terraform modules
│   │   ├── eks/                      # EKS cluster module
│   │   ├── networking/               # VPC, subnets, etc.
│   │   ├── database/                 # RDS, DynamoDB modules
│   │   ├── security/                 # IAM, security groups
│   │   └── storage/                  # S3 buckets, EFS
│   ├── environments/                   # Environment-specific configs
│   │   ├── dev/                      # Development environment
│   │   ├── staging/                  # Staging environment
│   │   └── prod/                     # Production environment
│   ├── main.tf                        # Main Terraform configuration
│   ├── variables.tf                    # Input variables
│   ├── outputs.tf                      # Output values
│   └── providers.tf                    # Provider configuration
│
├── k8s/                              # Kubernetes manifests
│   ├── 00-namespace.yaml               # Namespace definition
│   ├── 01-rbac.yaml                    # RBAC configuration
│   ├── 02-configmap.yaml               # ConfigMaps
│   ├── 03-secrets.yaml                 # Secrets (encrypted)
│   ├── 04-database.yaml                # Database resources
│   ├── 05-redis.yaml                   # Redis cache
│   ├── 06-deployments/                 # Application deployments
│   │   ├── api-deployment.yaml        # API service deployment
│   │   ├── worker-deployment.yaml     # Background worker deployment
│   │   └── frontend-deployment.yaml   # Frontend deployment
│   ├── 07-services/                   # Service definitions
│   │   ├── api-service.yaml           # API service
│   │   └── frontend-service.yaml      # Frontend service
│   ├── 08-ingress.yaml                 # Ingress configuration
│   ├── 09-hpa.yaml                     # Horizontal Pod Autoscaler
│   └── kustomization.yaml              # Kustomize configuration
│
├── argocd/                            # ArgoCD configuration
│   ├── application.yaml                # Application definition
│   └── project.yaml                    # Project configuration
│
├── .github/workflows/                  # CI/CD pipelines
│   ├── ci.yaml                         # Continuous Integration
│   ├── cd-dev.yaml                     # CD for development
│   ├── cd-staging.yaml                 # CD for staging
│   ├── cd-prod.yaml                    # CD for production
│   └── security-scan.yaml              # Security scanning
│
├── monitoring/                         # Observability stack
│   ├── prometheus/                     # Prometheus configuration
│   │   ├── values.yaml                # Helm values
│   │   ├── rules/                     # Alert rules
│   │   └── service-monitors/          # Service monitors
│   ├── grafana/                        # Grafana configuration
│   │   ├── values.yaml                # Helm values
│   │   └── dashboards/                # Dashboard definitions
│   ├── loki/                           # Loki configuration
│   │   └── values.yaml                # Helm values
│   ├── jaeger/                         # Jaeger configuration
│   │   ├── jaeger-operator.yaml       # Operator deployment
│   │   └── jaeger-instance.yaml       # Jaeger instance
│   └── alertmanager/                   # Alertmanager config
│       └── alertmanager.yaml            # Alert configuration
│
├── docs/                              # Documentation
│   ├── architecture.md                 # Architecture overview
│   ├── development.md                  # Development guide
│   ├── deployment.md                   # Deployment guide
│   └── monitoring.md                   # Monitoring guide
│
└── scripts/                            # Utility scripts
    ├── setup-dev.sh                    # Development setup
    ├── deploy.sh                       # Deployment script
    └── monitoring-setup.sh              # Monitoring setup
```

## Contributing

We welcome contributions to enhance this DevOps e-commerce project. To contribute effectively:

1. Fork this repository to your GitHub account
2. Create a feature branch from the main branch (`git checkout -b feature/amazing-feature`)
3. Implement your changes following the project's coding standards and best practices
4. Add appropriate tests to validate your changes
5. Ensure all tests pass and code quality checks succeed
6. Update documentation to reflect your changes
7. Commit your changes using conventional commit messages (`git commit -m 'feat: Add amazing feature'`)
8. Push your branch to your fork (`git push origin feature/amazing-feature`)
9. Open a Pull Request against the main branch with a clear description of the changes

Please review our [contribution guidelines](./docs/CONTRIBUTING.md) for more detailed information on our development workflow, coding standards, and pull request process.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Architecture Overview](./docs/architecture.md) - Detailed explanation of the system architecture
- [Development Guide](./docs/development.md) - Setup instructions for local development
- [Deployment Guide](./docs/deployment.md) - Instructions for deploying to different environments
- [Monitoring Guide](./docs/monitoring.md) - Information about the observability stack

## Contact

Project Owner - [Sarper](https://github.com/TheCloudGuruSarp)

Project Link: [https://github.com/TheCloudGuruSarp/devops-ecommerce-project](https://github.com/TheCloudGuruSarp/devops-ecommerce-project)
