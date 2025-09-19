# Deployment and Configuration Guide

## Overview

This guide provides comprehensive instructions for deploying and configuring the UNLOCK MLS MCP Server in various environments, from local development to production-scale deployments.

## Prerequisites

### System Requirements

- **Python**: 3.11 or higher
- **Memory**: Minimum 512MB RAM, recommended 2GB+ for production
- **CPU**: 1+ cores, recommended 2+ cores for production
- **Storage**: Minimum 1GB available space
- **Network**: HTTPS access to `api.bridgedataoutput.com`

### Dependencies

- **Package Manager**: [uv](https://github.com/astral-sh/uv) (recommended) or pip
- **Runtime**: uvloop for optimal async performance (installed automatically)
- **Optional**: Docker for containerized deployment

## Environment Configuration

### Environment Variables

Create a `.env` file in the project root with the following configuration:

```bash
# Bridge Interactive API Configuration (Required)
BRIDGE_SERVER_TOKEN=your_server_token_here
BRIDGE_CLIENT_ID=your_client_id_here
BRIDGE_CLIENT_SECRET=your_client_secret_here
BRIDGE_MLS_ID=your_mls_id_here
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2

# OAuth2 Configuration (Optional - if using OAuth2 flow)
BRIDGE_TOKEN_ENDPOINT=https://api.bridgedataoutput.com/oauth2/token

# Server Configuration
MCP_SERVER_NAME=unlock-mls-mcp
LOG_LEVEL=INFO

# Performance Tuning (Optional)
API_RATE_LIMIT_PER_MINUTE=60
API_CONNECTION_TIMEOUT=30
API_REQUEST_TIMEOUT=120

# Caching Configuration (Optional)
CACHE_ENABLED=false
CACHE_TTL_SECONDS=300

# Development/Debug (Optional)
DEBUG_MODE=false
VERBOSE_LOGGING=false
```

### Configuration Validation

The server validates configuration on startup:

```python
# Example configuration validation
from src.config.settings import get_settings

def validate_deployment_config():
    """Validate deployment configuration."""
    try:
        settings = get_settings()
        
        # Check required fields
        required_fields = [
            'bridge_mls_id',
            'bridge_api_base_url'
        ]
        
        for field in required_fields:
            if not getattr(settings, field):
                raise ValueError(f"Required field missing: {field}")
        
        # Check authentication
        has_bearer = bool(settings.bridge_server_token)
        has_oauth2 = bool(settings.bridge_client_id and settings.bridge_client_secret)
        
        if not (has_bearer or has_oauth2):
            raise ValueError("Either Bearer token or OAuth2 credentials required")
        
        print("✅ Configuration validation successful")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

if __name__ == "__main__":
    validate_deployment_config()
```

## Development Deployment

### Local Development Setup

1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd unlock-reso-mcp
   ```

2. **Install Dependencies**:
   ```bash
   # Using uv (recommended)
   uv sync --dev
   
   # Or using pip
   pip install -e ".[dev]"
   ```

3. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Bridge Interactive credentials
   ```

4. **Run Server**:
   ```bash
   # Direct execution
   python -m main
   
   # Or using the module
   python -m src.server
   
   # With debug logging
   LOG_LEVEL=DEBUG python -m main
   ```

### Development Tools

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Type checking
mypy src

# Linting and formatting
ruff check src tests
ruff format src tests

# Run specific test categories
pytest tests/test_integration.py -v
pytest tests/test_performance.py -v
pytest tests/test_error_scenarios.py -v
```

### Claude Desktop Integration

Add to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "unlock-mls-mcp": {
      "command": "python",
      "args": ["-m", "main"],
      "cwd": "/path/to/unlock-reso-mcp",
      "env": {
        "BRIDGE_SERVER_TOKEN": "your_token_here",
        "BRIDGE_MLS_ID": "your_mls_id",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Production Deployment

### Production Environment Setup

1. **System Preparation**:
   ```bash
   # Create dedicated user
   sudo useradd -m -s /bin/bash mcpserver
   sudo mkdir -p /opt/unlock-mls-mcp
   sudo chown mcpserver:mcpserver /opt/unlock-mls-mcp
   ```

2. **Application Deployment**:
   ```bash
   # Switch to service user
   sudo su - mcpserver
   
   # Deploy application
   cd /opt/unlock-mls-mcp
   git clone <repository-url> .
   
   # Install dependencies
   uv sync --no-dev
   
   # Create production environment file
   cp .env.example .env
   # Configure with production credentials
   ```

3. **Security Configuration**:
   ```bash
   # Secure environment file
   chmod 600 .env
   chown mcpserver:mcpserver .env
   
   # Create secure credentials directory
   sudo mkdir -p /etc/unlock-mls-mcp
   sudo chown root:mcpserver /etc/unlock-mls-mcp
   sudo chmod 750 /etc/unlock-mls-mcp
   
   # Store credentials securely
   echo "your_server_token" | sudo tee /etc/unlock-mls-mcp/server_token
   sudo chmod 640 /etc/unlock-mls-mcp/server_token
   ```

### Systemd Service Configuration

Create `/etc/systemd/system/unlock-mls-mcp.service`:

```ini
[Unit]
Description=UNLOCK MLS MCP Server
Documentation=https://github.com/your-org/unlock-reso-mcp
After=network.target
Wants=network.target

[Service]
Type=simple
User=mcpserver
Group=mcpserver
WorkingDirectory=/opt/unlock-mls-mcp
ExecStart=/opt/unlock-mls-mcp/.venv/bin/python -m main
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
Restart=always
RestartSec=5
TimeoutStopSec=30

# Environment configuration
Environment=PYTHONPATH=/opt/unlock-mls-mcp
EnvironmentFile=/opt/unlock-mls-mcp/.env

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=strict
ReadWritePaths=/opt/unlock-mls-mcp
CapabilityBoundingSet=
SystemCallArchitectures=native
SystemCallFilter=@system-service
RestrictNamespaces=true
LockPersonality=true
MemoryDenyWriteExecute=true
RestrictRealtime=true
RestrictSUIDSGID=true
RemoveIPC=true

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable unlock-mls-mcp
sudo systemctl start unlock-mls-mcp
sudo systemctl status unlock-mls-mcp
```

### Production Environment Variables

```bash
# Production .env configuration
BRIDGE_SERVER_TOKEN_FILE=/etc/unlock-mls-mcp/server_token
BRIDGE_CLIENT_SECRET_FILE=/etc/unlock-mls-mcp/client_secret
BRIDGE_MLS_ID=your_production_mls_id
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2

# Production settings
LOG_LEVEL=INFO
MCP_SERVER_NAME=unlock-mls-mcp-prod

# Performance optimization
API_RATE_LIMIT_PER_MINUTE=120
API_CONNECTION_TIMEOUT=30
API_REQUEST_TIMEOUT=120
CACHE_ENABLED=true
CACHE_TTL_SECONDS=300

# Security
DEBUG_MODE=false
VERBOSE_LOGGING=false
```

## Container Deployment

### Docker Configuration

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 mcpserver

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --no-dev

# Copy application code
COPY --chown=mcpserver:mcpserver . .

# Switch to non-root user
USER mcpserver

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import aiohttp; import asyncio; asyncio.run(aiohttp.ClientSession().get('http://localhost:8080/health'))" || exit 1

# Run application
CMD ["python", "-m", "main"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  unlock-mls-mcp:
    build: .
    container_name: unlock-mls-mcp
    restart: unless-stopped
    
    environment:
      - BRIDGE_SERVER_TOKEN=${BRIDGE_SERVER_TOKEN}
      - BRIDGE_MLS_ID=${BRIDGE_MLS_ID}
      - BRIDGE_API_BASE_URL=${BRIDGE_API_BASE_URL}
      - LOG_LEVEL=INFO
      - CACHE_ENABLED=true
    
    # Security
    read_only: true
    tmpfs:
      - /tmp
    
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    
    # Health check
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    # Logging
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

# Production network
networks:
  default:
    driver: bridge
```

### Kubernetes Deployment

Create Kubernetes manifests:

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: unlock-mls-config
  namespace: mcp-servers
data:
  BRIDGE_API_BASE_URL: "https://api.bridgedataoutput.com/api/v2"
  LOG_LEVEL: "INFO"
  CACHE_ENABLED: "true"
  CACHE_TTL_SECONDS: "300"

---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: unlock-mls-secrets
  namespace: mcp-servers
type: Opaque
data:
  BRIDGE_SERVER_TOKEN: <base64-encoded-token>
  BRIDGE_MLS_ID: <base64-encoded-mls-id>
  BRIDGE_CLIENT_SECRET: <base64-encoded-secret>

---
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: unlock-mls-mcp
  namespace: mcp-servers
  labels:
    app: unlock-mls-mcp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: unlock-mls-mcp
  template:
    metadata:
      labels:
        app: unlock-mls-mcp
    spec:
      serviceAccountName: unlock-mls-mcp
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      
      containers:
      - name: mcp-server
        image: unlock-mls-mcp:latest
        imagePullPolicy: Always
        
        ports:
        - containerPort: 8080
          name: http
        
        envFrom:
        - configMapRef:
            name: unlock-mls-config
        - secretRef:
            name: unlock-mls-secrets
        
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: unlock-mls-mcp-service
  namespace: mcp-servers
spec:
  selector:
    app: unlock-mls-mcp
  ports:
  - name: http
    port: 80
    targetPort: 8080
  type: ClusterIP
```

Deploy to Kubernetes:

```bash
# Create namespace
kubectl create namespace mcp-servers

# Apply manifests
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml

# Check deployment status
kubectl get pods -n mcp-servers
kubectl logs -f deployment/unlock-mls-mcp -n mcp-servers
```

## Monitoring and Observability

### Logging Configuration

```python
# Production logging configuration
import logging
import json
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    """Structured logging formatter for production."""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

# Configure structured logging
def setup_production_logging():
    """Configure production logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    handler.setFormatter(StructuredFormatter())
    logger.addHandler(handler)
    
    return logger
```

### Health Checks

```python
# Health check endpoints
from fastapi import FastAPI
import aiohttp
import asyncio

app = FastAPI()

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/ready")
async def readiness_check():
    """Readiness check with dependency validation."""
    checks = {
        "bridge_api": False,
        "configuration": False
    }
    
    # Check Bridge API connectivity
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.bridge_api_base_url}/health",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                checks["bridge_api"] = response.status == 200
    except:
        pass
    
    # Check configuration
    try:
        from src.config.settings import get_settings
        settings = get_settings()
        checks["configuration"] = bool(settings.bridge_mls_id)
    except:
        pass
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return JSONResponse(
        content={
            "status": "ready" if all_healthy else "not_ready",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat()
        },
        status_code=status_code
    )
```

### Metrics Collection

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Define metrics
request_count = Counter('mcp_requests_total', 'Total MCP requests', ['tool', 'status'])
request_duration = Histogram('mcp_request_duration_seconds', 'Request duration')
active_connections = Gauge('mcp_active_connections', 'Active connections')

# Metrics middleware
class MetricsMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            # Track active connections
            active_connections.inc()
            
            try:
                await self.app(scope, receive, send)
                request_count.labels(tool="unknown", status="success").inc()
            except Exception as e:
                request_count.labels(tool="unknown", status="error").inc()
                raise
            finally:
                request_duration.observe(time.time() - start_time)
                active_connections.dec()
        else:
            await self.app(scope, receive, send)

# Start metrics server
start_http_server(8081)
```

## Performance Tuning

### Production Optimizations

```python
# Performance configuration
import asyncio
import uvloop

# Use uvloop for better async performance
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Connection pool configuration
async def create_optimized_client():
    """Create optimized HTTP client for production."""
    connector = aiohttp.TCPConnector(
        limit=100,  # Total connection pool size
        limit_per_host=20,  # Connections per host
        keepalive_timeout=60,  # Keep connections alive
        enable_cleanup_closed=True,
        use_dns_cache=True,
        ttl_dns_cache=300
    )
    
    timeout = aiohttp.ClientTimeout(
        total=30,  # Total timeout
        connect=10,  # Connection timeout
        sock_read=20  # Socket read timeout
    )
    
    return aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
        headers={
            'User-Agent': 'UNLOCK-MLS-MCP-Server/1.0'
        }
    )
```

### Caching Strategy

```python
# Redis caching for production
import redis.asyncio as redis
import json
from typing import Optional

class RedisCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
    
    async def get(self, key: str) -> Optional[dict]:
        """Get cached data."""
        try:
            data = await self.redis.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.warning("Cache get failed: %s", e)
            return None
    
    async def set(self, key: str, data: dict, ttl: int = 300):
        """Set cached data with TTL."""
        try:
            await self.redis.setex(key, ttl, json.dumps(data))
        except Exception as e:
            logger.warning("Cache set failed: %s", e)
    
    async def delete(self, key: str):
        """Delete cached data."""
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.warning("Cache delete failed: %s", e)
```

## Security Hardening

### Production Security Checklist

- [ ] **Environment Variables**: Store sensitive data in secure environment variables or secrets management
- [ ] **TLS/HTTPS**: All API communication over HTTPS with certificate validation
- [ ] **Input Validation**: All user inputs validated and sanitized
- [ ] **Rate Limiting**: Implement rate limiting to prevent abuse
- [ ] **Access Control**: Run with minimal privileges, non-root user
- [ ] **Network Security**: Firewall rules, network segmentation
- [ ] **Monitoring**: Security event monitoring and alerting
- [ ] **Updates**: Regular security updates and dependency scanning
- [ ] **Backup**: Secure backup and recovery procedures
- [ ] **Incident Response**: Security incident response plan

### Security Configuration

```python
# Security middleware
class SecurityHeadersMiddleware:
    """Add security headers to responses."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))
                    
                    # Security headers
                    security_headers = {
                        b"x-content-type-options": b"nosniff",
                        b"x-frame-options": b"DENY",
                        b"x-xss-protection": b"1; mode=block",
                        b"strict-transport-security": b"max-age=31536000; includeSubDomains",
                        b"content-security-policy": b"default-src 'self'",
                        b"referrer-policy": b"strict-origin-when-cross-origin"
                    }
                    
                    headers.update(security_headers)
                    message["headers"] = list(headers.items())
                
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)
```

## Troubleshooting

### Common Deployment Issues

#### Configuration Problems

```bash
# Check configuration
python -c "from src.config.settings import get_settings; print(get_settings())"

# Validate environment
python -c "
import os
required = ['BRIDGE_MLS_ID', 'BRIDGE_API_BASE_URL']
missing = [k for k in required if not os.getenv(k)]
print('Missing:', missing) if missing else print('✅ All required vars present')
"
```

#### Connection Issues

```bash
# Test API connectivity
curl -H "Authorization: Bearer $BRIDGE_SERVER_TOKEN" \
  "$BRIDGE_API_BASE_URL/OData/$BRIDGE_MLS_ID/Property?\$top=1"

# Check DNS resolution
nslookup api.bridgedataoutput.com

# Test network connectivity
nc -zv api.bridgedataoutput.com 443
```

#### Service Issues

```bash
# Check service status
systemctl status unlock-mls-mcp

# View logs
journalctl -u unlock-mls-mcp -f

# Check process
ps aux | grep python | grep main

# Check listening ports
netstat -tlnp | grep python
```

### Performance Monitoring

```bash
# Monitor resource usage
top -p $(pgrep -f "python.*main")

# Memory usage
ps -o pid,rss,vsz,comm -p $(pgrep -f "python.*main")

# Network connections
ss -tupln | grep python

# Check file descriptors
lsof -p $(pgrep -f "python.*main") | wc -l
```

This comprehensive deployment guide covers all aspects of deploying the UNLOCK MLS MCP Server from development to production environments with proper security, monitoring, and performance considerations.