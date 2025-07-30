# Docker Container and CI/CD Deployment Plan

## Overview

This document provides a comprehensive guide for containerizing the UNLOCK RESO MCP Server for local development with Docker Desktop and deploying it across multiple cloud platforms using CI/CD pipelines.

## 1. Docker Local Development Setup

### A. Development Dockerfile

Create `Dockerfile` in the project root:

```dockerfile
# Multi-stage build for development
FROM python:3.10-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv package manager
RUN pip install uv

# Install dependencies
RUN uv sync --dev

# Development stage
FROM python:3.10-slim

# Create non-root user
RUN useradd -m -u 999 mcp && \
    mkdir -p /app && \
    chown -R mcp:mcp /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy from builder
COPY --from=builder /root/.cache/uv /root/.cache/uv
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=mcp:mcp . .

# Switch to non-root user
USER mcp

# Set Python path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"

# Default command
CMD ["python", "-m", "src.server"]
```

### B. Production Dockerfile

Create `Dockerfile.prod`:

```dockerfile
# Production multi-stage build
FROM python:3.10-slim as builder

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv and dependencies (no dev)
RUN pip install uv && \
    uv sync --no-dev

# Production stage
FROM python:3.10-slim

# Security: Create non-root user
RUN useradd -m -u 999 mcp && \
    mkdir -p /app && \
    chown -R mcp:mcp /app

# Install only essential runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only necessary files
COPY --from=builder /app/.venv /app/.venv
COPY --chown=mcp:mcp src/ ./src/
COPY --chown=mcp:mcp main.py ./

# Switch to non-root user
USER mcp

# Set minimal environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Security: Read-only root filesystem
# (uncomment if your app supports it)
# RUN chmod -R 555 /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"

# Run with minimal privileges
CMD ["python", "-m", "main"]
```

### C. Docker Compose Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  unlock-reso-mcp:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: unlock-reso-mcp-dev
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=DEBUG
      - MCP_SERVER_NAME=unlock-reso-mcp-dev
    env_file:
      - .env.docker
    volumes:
      - ./src:/app/src:ro
      - ./tests:/app/tests:ro
    restart: unless-stopped
    networks:
      - mcp-network
    healthcheck:
      test: ["CMD", "python", "-c", "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Production profile with NGINX
  nginx:
    image: nginx:alpine
    profiles: ["production"]
    container_name: unlock-reso-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - unlock-reso-mcp
    networks:
      - mcp-network
    restart: unless-stopped

  unlock-reso-mcp-prod:
    build:
      context: .
      dockerfile: Dockerfile.prod
    profiles: ["production"]
    container_name: unlock-reso-mcp-prod
    environment:
      - LOG_LEVEL=INFO
      - MCP_SERVER_NAME=unlock-reso-mcp
    env_file:
      - .env.production
    networks:
      - mcp-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

networks:
  mcp-network:
    driver: bridge
```

### D. Environment Configuration Files

Create `.env.docker`:

```bash
# Development Docker Environment
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2
BRIDGE_SERVER_TOKEN=your_dev_server_token_here
BRIDGE_MLS_ID=your_mls_id_here
LOG_LEVEL=DEBUG
CACHE_ENABLED=true
CACHE_TTL_SECONDS=60
```

Create `.dockerignore`:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.ruff_cache/

# Virtual environments
venv/
.venv/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.*
!.env.example
!.env.docker

# Git
.git/
.gitignore

# Tests
tests/
coverage.xml
*.cover

# Documentation
docs/
*.md
!README.md

# CI/CD
.github/
scripts/
terraform/
kubernetes/
```

## 2. CI/CD Pipeline Configuration

### A. GitHub Actions Main Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Testing and validation
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install uv
      run: pip install uv
    
    - name: Install dependencies
      run: uv sync --dev
    
    - name: Run tests
      run: |
        source .venv/bin/activate
        pytest --cov=src --cov-report=xml
    
    - name: Run linting
      run: |
        source .venv/bin/activate
        ruff check src tests
        mypy src
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  # Build Docker images
  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to GitHub Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.DOCKER_REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        file: ./Dockerfile.prod
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  # Deploy to Google Cloud Platform
  deploy-gcp:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Authenticate to Google Cloud
      uses: google-github-actions/auth@v2
      with:
        credentials_json: ${{ secrets.GCP_SA_KEY }}
    
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v2
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy unlock-reso-mcp \
          --image ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:latest \
          --platform managed \
          --region us-central1 \
          --allow-unauthenticated \
          --set-env-vars "LOG_LEVEL=INFO" \
          --set-secrets "BRIDGE_SERVER_TOKEN=bridge-server-token:latest" \
          --min-instances 1 \
          --max-instances 10 \
          --memory 512Mi \
          --cpu 1

  # Deploy to Azure
  deploy-azure:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Deploy to Azure Container Instances
      uses: azure/aci-deploy@v1
      with:
        resource-group: unlock-reso-rg
        dns-name-label: unlock-reso-mcp
        image: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:latest
        name: unlock-reso-mcp
        location: eastus
        cpu: 1
        memory: 1
        secure-environment-variables: |
          BRIDGE_SERVER_TOKEN=${{ secrets.BRIDGE_SERVER_TOKEN }}
        environment-variables: |
          LOG_LEVEL=INFO
          BRIDGE_MLS_ID=${{ vars.BRIDGE_MLS_ID }}

  # Deploy to AWS
  deploy-aws:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v2
    
    - name: Push to ECR
      run: |
        docker pull ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:latest
        docker tag ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:latest ${{ steps.login-ecr.outputs.registry }}/unlock-reso-mcp:latest
        docker push ${{ steps.login-ecr.outputs.registry }}/unlock-reso-mcp:latest
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service \
          --cluster unlock-reso-cluster \
          --service unlock-reso-mcp-service \
          --force-new-deployment

  # Deploy to Vercel
  deploy-vercel:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v25
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
        vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
        vercel-args: '--prod'

  # Deploy to Netlify
  deploy-netlify:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to Netlify
      uses: nwtgck/actions-netlify@v2
      with:
        publish-dir: '.'
        production-deploy: true
        deploy-message: "Deploy from GitHub Actions"
      env:
        NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
        NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

## 3. Platform-Specific Configurations

### A. Google Cloud Platform (Cloud Run)

Create `scripts/deploy-gcp.sh`:

```bash
#!/bin/bash
set -e

PROJECT_ID="your-gcp-project"
SERVICE_NAME="unlock-reso-mcp"
REGION="us-central1"
IMAGE_URL="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Build and push to GCR
docker build -f Dockerfile.prod -t ${IMAGE_URL} .
docker push ${IMAGE_URL}

# Deploy to Cloud Run
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_URL} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --set-env-vars "LOG_LEVEL=INFO,BRIDGE_MLS_ID=${BRIDGE_MLS_ID}" \
  --set-secrets "BRIDGE_SERVER_TOKEN=bridge-server-token:latest" \
  --min-instances 1 \
  --max-instances 100 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --concurrency 1000
```

### B. Microsoft Azure (Container Instances)

Create `scripts/deploy-azure.sh`:

```bash
#!/bin/bash
set -e

RESOURCE_GROUP="unlock-reso-rg"
CONTAINER_NAME="unlock-reso-mcp"
ACR_NAME="unlockresoacr"
LOCATION="eastus"

# Build and push to ACR
az acr build --registry ${ACR_NAME} --image unlock-reso-mcp:latest -f Dockerfile.prod .

# Deploy to ACI
az container create \
  --resource-group ${RESOURCE_GROUP} \
  --name ${CONTAINER_NAME} \
  --image ${ACR_NAME}.azurecr.io/unlock-reso-mcp:latest \
  --dns-name-label unlock-reso-mcp \
  --ports 8000 \
  --cpu 1 \
  --memory 1 \
  --environment-variables \
    LOG_LEVEL=INFO \
    BRIDGE_MLS_ID=${BRIDGE_MLS_ID} \
  --secure-environment-variables \
    BRIDGE_SERVER_TOKEN=${BRIDGE_SERVER_TOKEN} \
  --registry-login-server ${ACR_NAME}.azurecr.io \
  --registry-username ${ACR_USERNAME} \
  --registry-password ${ACR_PASSWORD}
```

### C. Amazon AWS (ECS Fargate)

Create `scripts/deploy-aws.sh`:

```bash
#!/bin/bash
set -e

CLUSTER_NAME="unlock-reso-cluster"
SERVICE_NAME="unlock-reso-mcp-service"
TASK_FAMILY="unlock-reso-mcp"
ECR_REPO="unlock-reso-mcp"
REGION="us-east-1"

# Get ECR login token
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_URI}

# Build and push to ECR
docker build -f Dockerfile.prod -t ${ECR_REPO} .
docker tag ${ECR_REPO}:latest ${ECR_URI}/${ECR_REPO}:latest
docker push ${ECR_URI}/${ECR_REPO}:latest

# Update ECS service
aws ecs update-service \
  --cluster ${CLUSTER_NAME} \
  --service ${SERVICE_NAME} \
  --force-new-deployment \
  --region ${REGION}
```

Create `aws/task-definition.json`:

```json
{
  "family": "unlock-reso-mcp",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "unlock-reso-mcp",
      "image": "${ECR_URI}/unlock-reso-mcp:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "LOG_LEVEL",
          "value": "INFO"
        }
      ],
      "secrets": [
        {
          "name": "BRIDGE_SERVER_TOKEN",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:bridge-server-token"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "python -c \"import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()\""],
        "interval": 30,
        "timeout": 10,
        "retries": 3,
        "startPeriod": 60
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/unlock-reso-mcp",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### D. Vercel Deployment

Create `vercel.json`:

```json
{
  "functions": {
    "api/index.py": {
      "runtime": "python3.9",
      "maxDuration": 60
    }
  },
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/api/index"
    }
  ],
  "env": {
    "LOG_LEVEL": "INFO"
  }
}
```

Create `api/index.py`:

```python
"""Vercel serverless function adapter for UNLOCK RESO MCP Server."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the MCP server
from src.server import create_handler

# Create the handler
handler = create_handler()

def main(request):
    """Main Vercel function handler."""
    return handler(request)
```

### E. Netlify Deployment

Create `netlify.toml`:

```toml
[build]
  command = "pip install uv && uv sync --no-dev"
  publish = "."

[functions]
  directory = "netlify/functions"
  node_bundler = "esbuild"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/mcp-server"
  status = 200

[context.production.environment]
  LOG_LEVEL = "INFO"
```

Create `netlify/functions/mcp-server.py`:

```python
"""Netlify function adapter for UNLOCK RESO MCP Server."""

import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.server import create_handler

# Create handler
handler = create_handler()

def handler(event, context):
    """Netlify function handler."""
    try:
        # Parse the request
        body = json.loads(event.get('body', '{}'))
        
        # Process with MCP handler
        response = handler(body)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

## 4. Kubernetes Deployment (Optional)

### A. Kubernetes Manifests

Create `kubernetes/namespace.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: unlock-reso
```

Create `kubernetes/secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: unlock-reso-secrets
  namespace: unlock-reso
type: Opaque
stringData:
  BRIDGE_SERVER_TOKEN: "your-server-token"
```

Create `kubernetes/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: unlock-reso-mcp
  namespace: unlock-reso
  labels:
    app: unlock-reso-mcp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: unlock-reso-mcp
  template:
    metadata:
      labels:
        app: unlock-reso-mcp
    spec:
      containers:
      - name: unlock-reso-mcp
        image: ghcr.io/your-org/unlock-reso-mcp:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          protocol: TCP
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: BRIDGE_MLS_ID
          value: "your-mls-id"
        envFrom:
        - secretRef:
            name: unlock-reso-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"
          initialDelaySeconds: 30
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          exec:
            command:
            - python
            - -c
            - "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"
          initialDelaySeconds: 5
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 999
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
```

Create `kubernetes/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: unlock-reso-mcp-service
  namespace: unlock-reso
  labels:
    app: unlock-reso-mcp
spec:
  type: LoadBalancer
  selector:
    app: unlock-reso-mcp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
    name: http
```

Create `kubernetes/hpa.yaml`:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: unlock-reso-mcp-hpa
  namespace: unlock-reso
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: unlock-reso-mcp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 5. Security Best Practices

### A. Container Security

1. **Non-root user**: All containers run as UID 999
2. **Minimal base images**: Using python:3.10-slim
3. **No unnecessary packages**: Production images exclude dev dependencies
4. **Security scanning**: Integrate Trivy or Snyk in CI/CD
5. **Read-only filesystem**: Enable where possible
6. **Resource limits**: CPU and memory constraints defined

### B. Secrets Management

1. **Environment-specific secrets**: Never commit credentials
2. **Platform secret services**:
   - GCP: Secret Manager
   - Azure: Key Vault
   - AWS: Secrets Manager
   - Kubernetes: Secrets with encryption at rest
3. **Rotation policy**: Implement regular credential rotation
4. **Least privilege**: Service accounts with minimal permissions

### C. Network Security

1. **TLS/SSL**: All production deployments use HTTPS
2. **Rate limiting**: Implemented at proxy/ingress level
3. **CORS policies**: Properly configured for API access
4. **Network policies**: Kubernetes network isolation

## 6. Monitoring and Observability

### A. Health Checks

All platforms implement:
- **Liveness probe**: Service is running
- **Readiness probe**: Service is ready to accept traffic
- **Startup probe**: Initial startup validation

### B. Logging

1. **Structured logging**: JSON format for easy parsing
2. **Log aggregation**:
   - GCP: Cloud Logging
   - Azure: Application Insights
   - AWS: CloudWatch
   - Self-hosted: ELK stack or Loki
3. **Log levels**: Environment-specific (DEBUG for dev, INFO for prod)

### C. Metrics

1. **Application metrics**: Response times, error rates
2. **Infrastructure metrics**: CPU, memory, network
3. **Custom metrics**: Business-specific KPIs
4. **Dashboards**: Platform-specific or Grafana

## 7. Local Development with Docker Desktop

### Quick Start Commands

```bash
# Build development image
docker-compose build

# Start development environment
docker-compose up

# Run with hot reloading
docker-compose up --build

# Production mode
docker-compose --profile production up

# View logs
docker-compose logs -f unlock-reso-mcp

# Execute commands in container
docker-compose exec unlock-reso-mcp python -m pytest

# Clean up
docker-compose down -v
```

### Development Tips

1. **Volume mounts**: Source code mounted for hot reloading
2. **Environment variables**: Use .env.docker for local config
3. **Debugging**: Expose additional ports for debuggers
4. **Database**: Add database service to docker-compose if needed
5. **Testing**: Run tests inside containers for consistency

## 8. Troubleshooting

### Common Issues

1. **Container won't start**:
   - Check environment variables
   - Verify credentials are set
   - Review container logs

2. **Health checks failing**:
   - Ensure service is binding to correct port
   - Check startup time requirements
   - Verify health check command

3. **Performance issues**:
   - Monitor resource usage
   - Adjust resource limits
   - Enable caching where appropriate

4. **Deployment failures**:
   - Verify platform credentials
   - Check image registry access
   - Review platform-specific quotas

## 9. Next Steps

1. **Implement CI/CD**: Start with GitHub Actions workflow
2. **Choose platforms**: Select 1-2 platforms for initial deployment
3. **Security audit**: Review and implement security best practices
4. **Monitoring setup**: Configure logging and metrics
5. **Documentation**: Update README with deployment instructions
6. **Testing**: Verify deployments with integration tests

This plan provides a comprehensive foundation for containerizing and deploying the UNLOCK RESO MCP Server across multiple platforms with proper CI/CD automation.