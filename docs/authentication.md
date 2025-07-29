# Authentication Documentation

## Overview

The UNLOCK MLS MCP Server implements a dual authentication system supporting both Bearer token authentication (primary) and OAuth2 client credentials flow (secondary). This design provides flexibility while ensuring secure access to Bridge Interactive's RESO Web API.

## Authentication Architecture

### System Design

```
MCP Server Startup → Authentication Configuration → 
Token Validation → API Connection Test → Ready State

API Request → Authentication Check → 
├─ Bearer Token Available → Add Auth Header → Execute Request
└─ No Bearer Token → OAuth2 Flow → Get Token → Retry Request
```

### Authentication Methods

1. **Bearer Token Authentication** (Primary)
   - Direct server token usage
   - Immediate authentication
   - Production recommended method

2. **OAuth2 Client Credentials Flow** (Secondary)
   - Dynamic token acquisition
   - Automatic token refresh
   - Fallback and development method

## Bearer Token Authentication

### Configuration

Bearer token authentication uses a pre-issued server token from Bridge Interactive.

#### Environment Variables

```bash
# Required for Bearer Token Auth
BRIDGE_SERVER_TOKEN=your_server_token_here
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2
BRIDGE_MLS_ID=your_mls_id_here
```

#### Implementation

```python
class ResoWebApiClient:
    def __init__(self, server_token: Optional[str] = None):
        self.server_token = server_token or settings.bridge_server_token
    
    async def _make_request(self, session, method, url, **kwargs):
        headers = kwargs.get('headers', {})
        headers.update({
            'Authorization': f'Bearer {self.server_token}',
            'Accept': 'application/json',
            'User-Agent': 'UNLOCK-MLS-MCP-Server/1.0'
        })
        
        response = await session.request(method, url, **kwargs)
        response.raise_for_status()
        return await response.json()
```

### Advantages

- **Simplicity**: Direct token usage without complex flows
- **Performance**: No additional authentication requests
- **Reliability**: No dependency on token endpoint availability
- **Security**: Reduced attack surface with fewer moving parts

### Use Cases

- **Production Deployments**: Recommended for production environments
- **High-Volume Applications**: Optimal for applications with many requests
- **Server-to-Server**: Direct API access without user interaction
- **CI/CD Pipelines**: Automated testing and deployment scenarios

## OAuth2 Client Credentials Flow

### Configuration

OAuth2 authentication uses client credentials to dynamically obtain access tokens.

#### Environment Variables

```bash
# Required for OAuth2 Flow
BRIDGE_CLIENT_ID=your_client_id_here
BRIDGE_CLIENT_SECRET=your_client_secret_here
BRIDGE_TOKEN_ENDPOINT=https://api.bridgedataoutput.com/oauth2/token
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2
BRIDGE_MLS_ID=your_mls_id_here
```

#### Implementation

```python
class OAuth2Handler:
    def __init__(self, client_id: str, client_secret: str, token_endpoint: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint
        self._access_token: Optional[str] = None
        self._expires_at: Optional[datetime] = None
    
    async def authenticate(self) -> str:
        """Get access token using client credentials flow."""
        if self.is_token_valid:
            return self._access_token
        
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                self.token_endpoint,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            token_data = await response.json()
            self._access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)
            self._expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
            
            return self._access_token
```

### Token Management

#### Token Lifecycle

```
Token Request → Validation → Storage → Usage → 
Expiration Check → Refresh (if needed) → Continue
```

#### Automatic Refresh

```python
@property
def is_token_valid(self) -> bool:
    """Check if current token is valid and not expired."""
    if not self._access_token or not self._expires_at:
        return False
    
    # Add 30 second buffer before expiration
    buffer = timedelta(seconds=30)
    return datetime.utcnow() < (self._expires_at - buffer)

async def get_valid_token(self) -> str:
    """Get a valid access token, refreshing if necessary."""
    async with self._token_lock:
        if not self.is_token_valid:
            await self.authenticate()
        return self._access_token
```

### Advantages

- **Dynamic Token Management**: Automatic token acquisition and refresh
- **Credential Isolation**: Client credentials separate from API tokens
- **Standard Compliance**: RFC 6749 OAuth2 specification compliance
- **Audit Trail**: Token requests can be logged and monitored

### Use Cases

- **Development Environments**: Easier credential management during development
- **Multi-Tenant Applications**: Different credentials per tenant
- **Token Rotation**: Environments requiring regular credential rotation
- **Debugging**: Token flow debugging and troubleshooting

## Security Considerations

### Credential Protection

#### Environment Variable Security

```bash
# Secure environment variable handling
export BRIDGE_SERVER_TOKEN="$(cat /secure/path/server_token.txt)"
export BRIDGE_CLIENT_SECRET="$(cat /secure/path/client_secret.txt)"

# Restrict file permissions
chmod 600 /secure/path/server_token.txt
chmod 600 /secure/path/client_secret.txt
```

#### In-Memory Storage

```python
class SecureCredentialHandler:
    def __init__(self):
        # Store credentials only in memory
        self._credentials = {}
        
    def store_credential(self, key: str, value: str):
        """Store credential in memory only."""
        self._credentials[key] = value
        
    def clear_credentials(self):
        """Clear all stored credentials."""
        for key in self._credentials:
            self._credentials[key] = None
        self._credentials.clear()
```

### Token Security

#### Secure Token Transmission

```python
async def _make_authenticated_request(self, url: str, **kwargs):
    """Make authenticated request with secure token handling."""
    headers = kwargs.get('headers', {})
    
    # Add authorization header securely
    if self.server_token:
        headers['Authorization'] = f'Bearer {self.server_token}'
    elif self.oauth2_handler:
        token = await self.oauth2_handler.get_valid_token()
        headers['Authorization'] = f'Bearer {token}'
    
    # Ensure HTTPS for all requests
    if not url.startswith('https://'):
        raise SecurityError("Only HTTPS connections allowed")
    
    kwargs['headers'] = headers
    kwargs['ssl'] = True  # Enforce SSL verification
    
    return await self._make_request(url, **kwargs)
```

#### Token Logging Protection

```python
import logging

class TokenSafeFormatter(logging.Formatter):
    """Custom formatter that sanitizes tokens from log messages."""
    
    def format(self, record):
        msg = super().format(record)
        # Remove bearer tokens from logs
        msg = re.sub(r'Bearer\s+[A-Za-z0-9\-_\.]+', 'Bearer [REDACTED]', msg)
        # Remove other sensitive patterns
        msg = re.sub(r'"access_token":\s*"[^"]*"', '"access_token": "[REDACTED]"', msg)
        return msg

# Configure safe logging
handler = logging.StreamHandler()
handler.setFormatter(TokenSafeFormatter())
logger.addHandler(handler)
```

### Network Security

#### HTTPS Enforcement

```python
import ssl
import aiohttp

# Configure secure SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Create session with secure defaults
connector = aiohttp.TCPConnector(ssl=ssl_context)
session = aiohttp.ClientSession(connector=connector)
```

#### Certificate Validation

```python
async def validate_api_endpoint(self, endpoint: str):
    """Validate API endpoint certificate and connectivity."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, ssl=True) as response:
                if response.status == 200:
                    logger.info("API endpoint validation successful")
                    return True
    except aiohttp.ClientSSLError as e:
        logger.error("SSL certificate validation failed: %s", e)
        raise AuthenticationError("API endpoint SSL validation failed")
    except Exception as e:
        logger.error("API endpoint validation failed: %s", e)
        raise AuthenticationError("API endpoint not accessible")
```

## Error Handling

### Authentication Errors

#### Error Classification

```python
class AuthenticationError(Exception):
    """Base class for authentication errors."""
    pass

class TokenExpiredError(AuthenticationError):
    """Token has expired and needs refresh."""
    pass

class InvalidCredentialsError(AuthenticationError):
    """Invalid client credentials provided."""
    pass

class TokenEndpointError(AuthenticationError):
    """Token endpoint not accessible."""
    pass
```

#### Error Recovery

```python
async def handle_authentication_error(self, error: Exception) -> bool:
    """Handle authentication errors with appropriate recovery."""
    
    if isinstance(error, TokenExpiredError):
        logger.info("Token expired, attempting refresh")
        try:
            await self.oauth2_handler.authenticate()
            return True  # Retry the request
        except Exception as refresh_error:
            logger.error("Token refresh failed: %s", refresh_error)
            return False
    
    elif isinstance(error, InvalidCredentialsError):
        logger.error("Invalid credentials, manual intervention required")
        return False
    
    elif isinstance(error, TokenEndpointError):
        logger.warning("Token endpoint unavailable, using fallback if available")
        if self.server_token:
            logger.info("Falling back to Bearer token authentication")
            return True
        return False
    
    return False
```

### Rate Limiting

#### Exponential Backoff

```python
import asyncio
import random

class RateLimitHandler:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def handle_rate_limit(self, attempt: int) -> bool:
        """Handle rate limiting with exponential backoff."""
        if attempt >= self.max_retries:
            return False
        
        # Exponential backoff with jitter
        delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
        logger.warning("Rate limited, retrying in %.2f seconds", delay)
        await asyncio.sleep(delay)
        return True
```

## Configuration Management

### Environment Configuration

#### Settings Validation

```python
from pydantic import BaseSettings, validator
from typing import Optional

class AuthSettings(BaseSettings):
    # Bearer Token Configuration
    bridge_server_token: Optional[str] = None
    
    # OAuth2 Configuration
    bridge_client_id: Optional[str] = None
    bridge_client_secret: Optional[str] = None
    bridge_token_endpoint: str = "https://api.bridgedataoutput.com/oauth2/token"
    
    # API Configuration
    bridge_api_base_url: str = "https://api.bridgedataoutput.com/api/v2"
    bridge_mls_id: str
    
    @validator('bridge_mls_id')
    def mls_id_required(cls, v):
        if not v:
            raise ValueError('Bridge MLS ID is required')
        return v
    
    def validate_auth_config(self):
        """Validate that at least one authentication method is configured."""
        has_bearer = bool(self.bridge_server_token)
        has_oauth2 = bool(self.bridge_client_id and self.bridge_client_secret)
        
        if not (has_bearer or has_oauth2):
            raise ValueError(
                "Either Bearer token or OAuth2 credentials must be provided"
            )
        
        return True
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

#### Configuration Loading

```python
def load_auth_config() -> AuthSettings:
    """Load and validate authentication configuration."""
    try:
        settings = AuthSettings()
        settings.validate_auth_config()
        
        # Log configuration (without sensitive values)
        logger.info("Authentication configuration loaded:")
        logger.info("- Bearer token: %s", "configured" if settings.bridge_server_token else "not configured")
        logger.info("- OAuth2 credentials: %s", "configured" if settings.bridge_client_id else "not configured")
        logger.info("- API base URL: %s", settings.bridge_api_base_url)
        logger.info("- MLS ID: %s", settings.bridge_mls_id)
        
        return settings
        
    except Exception as e:
        logger.error("Authentication configuration error: %s", e)
        raise AuthenticationError(f"Configuration error: {e}")
```

## Testing and Validation

### Authentication Testing

#### Unit Tests

```python
import pytest
import aiohttp
from unittest.mock import AsyncMock, patch

class TestAuthentication:
    
    @pytest.mark.asyncio
    async def test_bearer_token_auth(self):
        """Test Bearer token authentication flow."""
        client = ResoWebApiClient(server_token="test_token")
        
        with patch('aiohttp.ClientSession.request') as mock_request:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json.return_value = {"data": "test"}
            mock_request.return_value.__aenter__.return_value = mock_response
            
            result = await client._make_request(
                aiohttp.ClientSession(), 
                "GET", 
                "https://api.example.com/test"
            )
            
            # Verify Bearer token was included
            call_args = mock_request.call_args
            headers = call_args.kwargs['headers']
            assert headers['Authorization'] == 'Bearer test_token'
    
    @pytest.mark.asyncio
    async def test_oauth2_token_refresh(self):
        """Test OAuth2 token refresh functionality."""
        handler = OAuth2Handler("client_id", "client_secret", "https://token.endpoint")
        
        # Mock expired token
        handler._access_token = "expired_token"
        handler._expires_at = datetime.utcnow() - timedelta(minutes=1)
        
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_response = AsyncMock()
            mock_response.json.return_value = {
                "access_token": "new_token",
                "expires_in": 3600
            }
            mock_post.return_value.__aenter__.return_value = mock_response
            
            token = await handler.authenticate()
            
            assert token == "new_token"
            assert handler._access_token == "new_token"
```

#### Integration Tests

```python
@pytest.mark.integration
class TestAuthenticationIntegration:
    
    @pytest.mark.asyncio
    async def test_real_api_authentication(self):
        """Test authentication with real API endpoint."""
        if not os.getenv('BRIDGE_SERVER_TOKEN'):
            pytest.skip("Real API credentials not available")
        
        client = ResoWebApiClient()
        
        # Test connection with real credentials
        try:
            async with aiohttp.ClientSession() as session:
                response = await client._make_request(
                    session,
                    "GET",
                    f"{client.odata_endpoint}/Property?$top=1"
                )
                
                assert response is not None
                logger.info("Authentication test successful")
                
        except Exception as e:
            pytest.fail(f"Authentication failed: {e}")
```

### Security Testing

#### Credential Sanitization Tests

```python
def test_log_sanitization():
    """Test that credentials are properly sanitized in logs."""
    formatter = TokenSafeFormatter()
    
    # Test Bearer token sanitization
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Authorization: Bearer abc123def456",
        args=(),
        exc_info=None
    )
    
    formatted = formatter.format(record)
    assert "Bearer [REDACTED]" in formatted
    assert "abc123def456" not in formatted

def test_environment_variable_protection():
    """Test environment variable access patterns."""
    # Ensure credentials are not accidentally exposed
    import os
    
    # Test that credentials are properly loaded
    token = os.getenv('BRIDGE_SERVER_TOKEN')
    if token:
        # Verify token is not logged or printed
        assert token not in str(logging.getLogger().handlers)
```

## Production Deployment

### Recommended Configuration

#### Production Settings

```bash
# Production environment configuration
BRIDGE_SERVER_TOKEN=your_production_server_token
BRIDGE_MLS_ID=your_production_mls_id
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2

# Security settings
LOG_LEVEL=INFO
API_RATE_LIMIT_PER_MINUTE=60
CACHE_ENABLED=true
CACHE_TTL_SECONDS=300

# Optional OAuth2 fallback
BRIDGE_CLIENT_ID=your_client_id
BRIDGE_CLIENT_SECRET=your_client_secret
```

#### Container Deployment

```dockerfile
# Secure credential handling in containers
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 mcpserver

# Copy application
COPY --chown=mcpserver:mcpserver . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Switch to non-root user
USER mcpserver

# Use secrets for credentials (Docker Swarm/Kubernetes)
# Credentials mounted as files, not environment variables
CMD ["python", "-m", "main"]
```

#### Kubernetes Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: unlock-mls-credentials
type: Opaque
data:
  server-token: <base64-encoded-token>
  client-id: <base64-encoded-client-id>
  client-secret: <base64-encoded-client-secret>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: unlock-mls-server
spec:
  template:
    spec:
      containers:
      - name: server
        image: unlock-mls-server:latest
        env:
        - name: BRIDGE_SERVER_TOKEN
          valueFrom:
            secretKeyRef:
              name: unlock-mls-credentials
              key: server-token
```

### Monitoring and Alerting

#### Authentication Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Metrics for monitoring
auth_requests_total = Counter('auth_requests_total', 'Total authentication requests', ['method', 'status'])
auth_duration = Histogram('auth_duration_seconds', 'Authentication request duration')
token_expires_at = Gauge('token_expires_at', 'Token expiration timestamp')

class MonitoredAuthHandler:
    async def authenticate(self):
        start_time = time.time()
        try:
            token = await self._perform_authentication()
            auth_requests_total.labels(method='oauth2', status='success').inc()
            return token
        except Exception as e:
            auth_requests_total.labels(method='oauth2', status='error').inc()
            raise
        finally:
            auth_duration.observe(time.time() - start_time)
```

#### Health Checks

```python
async def health_check_authentication():
    """Health check for authentication system."""
    health_status = {
        "authentication": {
            "bearer_token": "not_configured",
            "oauth2": "not_configured", 
            "api_connectivity": "unknown"
        }
    }
    
    # Check Bearer token configuration
    if settings.bridge_server_token:
        health_status["authentication"]["bearer_token"] = "configured"
    
    # Check OAuth2 configuration
    if settings.bridge_client_id and settings.bridge_client_secret:
        health_status["authentication"]["oauth2"] = "configured"
    
    # Test API connectivity
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"{settings.bridge_api_base_url}/health",
                timeout=aiohttp.ClientTimeout(total=5)
            )
            if response.status == 200:
                health_status["authentication"]["api_connectivity"] = "healthy"
            else:
                health_status["authentication"]["api_connectivity"] = "degraded"
    except:
        health_status["authentication"]["api_connectivity"] = "unhealthy"
    
    return health_status
```

This comprehensive authentication system provides secure, flexible, and production-ready access to the Bridge Interactive RESO API while maintaining compatibility with various deployment scenarios and security requirements.