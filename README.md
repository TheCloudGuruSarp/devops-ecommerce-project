# E-Ticaret DevOps Projesi

![DevOps Pipeline](https://img.shields.io/badge/DevOps-Pipeline-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-brightgreen)
![Terraform](https://img.shields.io/badge/Infrastructure-Terraform-purple)
![Monitoring](https://img.shields.io/badge/Monitoring-Prometheus-orange)

## Proje Hakkında

Bu proje, modern DevOps pratiklerini kullanarak basit bir e-ticaret uygulamasının geliştirilmesi, dağıtımı ve yönetimini göstermektedir. Proje, CI/CD pipeline'ları, konteynerizasyon, altyapı yönetimi ve izleme çözümlerini içermektedir.

## Proje Bileşenleri

### 1. Uygulama
- Flask ile geliştirilmiş basit bir e-ticaret API'si
- Ürün listeleme, sipariş oluşturma ve kullanıcı yönetimi özellikleri
- Docker ile konteynerize edilmiş
- RESTful API tasarımı

### 2. Altyapı Yönetimi (Terraform)
- Kubernetes Cluster (EKS) oluşturma
- Load Balancer (AWS ALB) yapılandırması
- S3 bucket oluşturma (statik dosyalar ve yedekler için)
- IAM rolleri ve izinleri
- Modüler Terraform yapısı

### 3. CI/CD Pipeline (GitHub Actions)
- Otomatik test ve build süreçleri
- Docker image oluşturma ve ECR'ye push etme
- Kubernetes'e otomatik deployment
- Canary deployment stratejisi

### 4. Kubernetes Orkestrasyonu
- Deployment, Service ve Ingress yapılandırmaları
- ConfigMap ve Secret yönetimi
- Horizontal Pod Autoscaler (HPA) ile otomatik ölçeklendirme
- NGINX Ingress Controller

### 5. Monitoring ve Logging
- Prometheus ile metrik toplama
- Grafana ile görselleştirme
- Alertmanager ile uyarı yönetimi
- Loki ile log yönetimi

## Mimari Diyagram

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

## Kurulum ve Çalıştırma

### Ön Koşullar
- Docker ve Docker Compose
- Kubernetes CLI (kubectl)
- Terraform
- AWS CLI
- Python 3.8+

### Yerel Geliştirme

```bash
# Uygulamayı yerel olarak çalıştırma
cd app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Docker ile çalıştırma
docker build -t ecommerce-api:latest .
docker run -p 5000:5000 ecommerce-api:latest
```

### Altyapı Oluşturma

```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

### Kubernetes'e Deployment

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

### Monitoring Kurulumu

```bash
cd monitoring
kubectl apply -f prometheus/
kubectl apply -f grafana/
```

## CI/CD Pipeline

GitHub Actions pipeline'ı aşağıdaki adımları otomatik olarak gerçekleştirir:

1. Kod değişikliği push edildiğinde testleri çalıştırır
2. Testler başarılı olursa Docker image oluşturur
3. Image'ı ECR'ye push eder
4. Kubernetes manifest dosyalarını günceller
5. Uygulamayı Kubernetes'e deploy eder

## Monitoring

### Grafana Dashboards

![Grafana Dashboard](docs/images/grafana-dashboard.png)

### Prometheus Alerts

Örnek alert kuralları:
- Yüksek CPU kullanımı (>80%)
- Yüksek bellek kullanımı (>80%)
- Yüksek hata oranı (>5%)
- Servis yanıt süresi (>2s)

## Proje Yapısı

```
├── app/                    # Uygulama kodu
│   ├── api/                # API endpoint'leri
│   ├── models/             # Veri modelleri
│   ├── tests/              # Birim testleri
│   ├── Dockerfile          # Uygulama container yapılandırması
│   └── requirements.txt    # Python bağımlılıkları
│
├── infrastructure/         # Terraform kodları
│   ├── modules/            # Terraform modülleri
│   │   ├── eks/           # EKS cluster modülü
│   │   ├── networking/    # VPC, subnet vb.
│   │   └── storage/       # S3 bucket modülü
│   ├── main.tf            # Ana Terraform yapılandırması
│   └── variables.tf       # Terraform değişkenleri
│
├── k8s/                    # Kubernetes manifest dosyaları
│   ├── deployment.yaml     # Uygulama deployment
│   ├── service.yaml        # Servis yapılandırması
│   ├── ingress.yaml        # Ingress yapılandırması
│   ├── configmap.yaml      # Yapılandırma değerleri
│   ├── secret.yaml         # Gizli değerler
│   └── hpa.yaml            # Horizontal Pod Autoscaler
│
├── .github/workflows/      # GitHub Actions workflow dosyaları
│   ├── ci.yaml             # Continuous Integration
│   └── cd.yaml             # Continuous Deployment
│
└── monitoring/             # Monitoring yapılandırmaları
    ├── prometheus/         # Prometheus yapılandırması
    ├── grafana/            # Grafana dashboard'ları
    └── alertmanager/       # Alert kuralları
```

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## İletişim

Proje Sahibi - [GitHub Profiliniz](https://github.com/yourusername)

Proje Linki: [https://github.com/yourusername/devops-ecommerce-project](https://github.com/yourusername/devops-ecommerce-project)