# Docker Deployment Guide

This guide covers comprehensive Docker deployment strategies for the ACTRIS MLS MCP Server.

## Quick Start

### Development Setup

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd actris-mls-mcp-server
   cp .env.docker .env
   # Edit .env with your Bridge Interactive API credentials
   ```

2. **Start with Docker Compose**:
   ```bash
   docker-compose up
   ```

3. **Access the server**:
   - API: http://localhost:8000
   - Health: http://localhost:8000/health

## Production Deployment

### Option 1: Docker Compose (Recommended)

1. **Production environment**:
   ```bash
   # Copy and configure environment
   cp .env.docker .env.production
   # Edit with production credentials and settings
   
   # Start production stack
   docker-compose --profile production --env-file .env.production up -d
   ```

2. **Features included**:
   - NGINX reverse proxy with rate limiting
   - SSL/TLS termination (configure certificates)
   - Health checks and automatic restarts
   - Security headers and hardening

### Option 2: Standalone Container

1. **Build production image**:
   ```bash
   docker build -f Dockerfile.prod -t actris-mls-mcp:prod .
   ```

2. **Run production container**:
   ```bash
   docker run -d \
     --name actris-mls-mcp-prod \
     --restart unless-stopped \
     -p 8000:8000 \
     -e BRIDGE_CLIENT_ID=your_client_id \
     -e BRIDGE_CLIENT_SECRET=your_client_secret \
     -e BRIDGE_MLS_ID=actris-ref \
     -e LOG_LEVEL=INFO \
     --memory=512m \
     --cpus=1.0 \
     actris-mls-mcp:prod
   ```

### Option 3: Docker Swarm

1. **Initialize swarm**:
   ```bash
   docker swarm init
   ```

2. **Deploy stack**:
   ```bash
   docker stack deploy -c docker-compose.yml actris-mls
   ```

3. **Scale services**:
   ```bash
   docker service scale actris-mls_actris-mls-mcp=3
   ```

## Kubernetes Deployment

### Basic Deployment

1. **Create namespace**:
   ```yaml
   apiVersion: v1
   kind: Namespace
   metadata:
     name: actris-mls
   ```

2. **Secret for credentials**:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: actris-mls-secrets
     namespace: actris-mls
   type: Opaque
   stringData:
     BRIDGE_CLIENT_ID: "your_client_id"
     BRIDGE_CLIENT_SECRET: "your_client_secret"
   ```

3. **Deployment**:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: actris-mls-mcp
     namespace: actris-mls
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: actris-mls-mcp
     template:
       metadata:
         labels:
           app: actris-mls-mcp
       spec:
         containers:
         - name: actris-mls-mcp
           image: actris-mls-mcp:prod
           ports:
           - containerPort: 8000
           envFrom:
           - secretRef:
               name: actris-mls-secrets
           env:
           - name: BRIDGE_MLS_ID
             value: "actris-ref"
           - name: MCP_TRANSPORT
             value: "http"
           resources:
             requests:
               memory: "256Mi"
               cpu: "250m"
             limits:
               memory: "512Mi"
               cpu: "500m"
           livenessProbe:
             httpGet:
               path: /health
               port: 8000
             initialDelaySeconds: 30
             periodSeconds: 30
           readinessProbe:
             httpGet:
               path: /health
               port: 8000
             initialDelaySeconds: 5
             periodSeconds: 10
   ```

4. **Service**:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: actris-mls-mcp-service
     namespace: actris-mls
   spec:
     selector:
       app: actris-mls-mcp
     ports:
     - protocol: TCP
       port: 80
       targetPort: 8000
     type: LoadBalancer
   ```

## Environment Configuration

### Development (.env)
```bash
# API Credentials
BRIDGE_CLIENT_ID=your_dev_client_id
BRIDGE_CLIENT_SECRET=your_dev_client_secret
BRIDGE_MLS_ID=actris-ref

# Debug settings
LOG_LEVEL=DEBUG
CACHE_TTL=60
```

### Production (.env.production)
```bash
# API Credentials
BRIDGE_CLIENT_ID=your_prod_client_id
BRIDGE_CLIENT_SECRET=your_prod_client_secret
BRIDGE_MLS_ID=actris-ref

# Production settings
LOG_LEVEL=INFO
CACHE_TTL=300
RATE_LIMIT_REQUESTS=50
RATE_LIMIT_WINDOW=60
```

## Monitoring and Logging

### Health Checks

The container includes built-in health checks:

```bash
# Check container health
docker ps
docker inspect --format='{{json .State.Health}}' actris-mls-mcp

# Manual health check (socket connection test)
python -c "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close(); print('Server is running')"
```

### Logging

```bash
# View container logs
docker logs actris-mls-mcp

# Follow logs
docker logs -f actris-mls-mcp

# With Docker Compose
docker-compose logs actris-mls-mcp
```

### Metrics Collection

Example Prometheus configuration for monitoring:

```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Security Considerations

### Container Security

1. **Non-root user**: Containers run as non-root user (UID 999)
2. **Read-only filesystem**: Consider mounting filesystem as read-only
3. **Resource limits**: Set appropriate CPU and memory limits
4. **Network policies**: Implement Kubernetes network policies

### NGINX Security (Production)

1. **SSL/TLS**: Configure proper SSL certificates
2. **Rate limiting**: Implemented in nginx.conf
3. **Security headers**: Added in nginx configuration
4. **Access logs**: Monitor for suspicious activity

### Secrets Management

1. **Environment variables**: Use Docker secrets or Kubernetes secrets
2. **Credential rotation**: Implement regular credential rotation
3. **Least privilege**: Use dedicated service accounts

## Backup and Recovery

### Data Backup

Since this is a stateless service, backup focus should be on:
1. Configuration files
2. SSL certificates
3. Deployment manifests

### Disaster Recovery

1. **Image registry**: Ensure images are stored in reliable registry
2. **Configuration**: Version control all configuration files
3. **Monitoring**: Set up alerts for service availability

## Troubleshooting

### Common Issues

1. **Container won't start**:
   ```bash
   docker logs actris-mls-mcp
   # Check environment variables and credentials
   ```

2. **Health check failing**:
   ```bash
   # Check if service is responding
   curl http://localhost:8000/health
   
   # Verify container resources
   docker stats actris-mls-mcp
   ```

3. **High memory usage**:
   ```bash
   # Check container stats
   docker stats
   
   # Restart container if needed
   docker restart actris-mls-mcp
   ```

### Performance Tuning

1. **Resource allocation**:
   ```yaml
   resources:
     requests:
       memory: "256Mi"
       cpu: "250m"
     limits:
       memory: "512Mi"
       cpu: "500m"
   ```

2. **Scaling**:
   ```bash
   # Docker Compose
   docker-compose up --scale actris-mls-mcp=3
   
   # Kubernetes
   kubectl scale deployment actris-mls-mcp --replicas=3
   ```

## Best Practices

1. **Image tagging**: Use semantic versioning for images
2. **Multi-stage builds**: Optimize image size with multi-stage builds
3. **Health checks**: Always include health checks
4. **Resource limits**: Set appropriate resource constraints
5. **Secrets management**: Never hardcode secrets in images
6. **Logging**: Centralize log collection and analysis
7. **Monitoring**: Implement comprehensive monitoring and alerting
8. **Updates**: Regular security updates and dependency updates