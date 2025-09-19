# Configuration Guide

This document provides comprehensive information about all environment variables and configuration options for the UNLOCK MLS MCP Server.

## Environment Variables

### Required Configuration

#### Bridge Interactive API Settings

These settings are required for the server to authenticate with the Bridge Interactive RESO Web API:

**`BRIDGE_CLIENT_ID`**
- **Type**: String (required)
- **Description**: OAuth2 client ID provided by Bridge Interactive
- **Example**: `your_client_id_here`
- **Notes**: This is provided when you register for Bridge Interactive API access

**`BRIDGE_CLIENT_SECRET`**
- **Type**: String (required)
- **Description**: OAuth2 client secret provided by Bridge Interactive
- **Example**: `your_client_secret_here`
- **Security**: Keep this value secure and never commit to version control

**`BRIDGE_MLS_ID`**
- **Type**: String (required)
- **Description**: MLS identifier for the data source
- **Default**: `UNLOCK`
- **Example**: `UNLOCK`
- **Notes**: For UNLOCK MLS data, this should always be set to "UNLOCK"

### Optional Configuration

#### API Connection Settings

**`BRIDGE_API_BASE_URL`**
- **Type**: String (optional)
- **Description**: Base URL for the Bridge Interactive API
- **Default**: `https://api.bridgedataoutput.com/api/v2`
- **Example**: `https://api.bridgedataoutput.com/api/v2`
- **Notes**: Only change this if Bridge Interactive provides a different endpoint

**`BRIDGE_SERVER_TOKEN`**
- **Type**: String (optional)
- **Description**: Server token for additional authentication (if required)
- **Default**: `None`
- **Example**: `server_token_value`
- **Notes**: Only set if specifically required by your Bridge Interactive configuration

#### MCP Server Configuration

**`MCP_SERVER_NAME`**
- **Type**: String (optional)
- **Description**: Name identifier for the MCP server
- **Default**: `unlock-mls-mcp`
- **Example**: `unlock-mls-mcp`
- **Notes**: Used for server identification in MCP communications

#### Logging Configuration

**`LOG_LEVEL`**
- **Type**: String (optional)
- **Description**: Logging level for the application
- **Default**: `INFO`
- **Valid Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Example**: `INFO`
- **Notes**: 
  - `DEBUG`: Detailed debugging information
  - `INFO`: General information messages
  - `WARNING`: Warning messages only
  - `ERROR`: Error messages only
  - `CRITICAL`: Critical error messages only

#### Performance & Caching Settings

**`API_RATE_LIMIT_PER_MINUTE`**
- **Type**: Integer (optional)
- **Description**: Maximum number of API requests per minute
- **Default**: `60`
- **Range**: `1` to `300`
- **Example**: `60`
- **Notes**: Used to prevent exceeding Bridge Interactive API rate limits

**`CACHE_ENABLED`**
- **Type**: Boolean (optional)
- **Description**: Enable or disable response caching
- **Default**: `false`
- **Valid Values**: `true`, `false`
- **Example**: `false`
- **Notes**: Currently not implemented but reserved for future caching features

**`CACHE_TTL_SECONDS`**
- **Type**: Integer (optional)
- **Description**: Cache time-to-live in seconds
- **Default**: `300`
- **Range**: `60` to `3600`
- **Example**: `300`
- **Notes**: How long cached responses are considered valid

## Configuration File Examples

### Basic Configuration (.env)

```bash
# Required Bridge Interactive API Configuration
BRIDGE_CLIENT_ID=your_client_id_here
BRIDGE_CLIENT_SECRET=your_client_secret_here
BRIDGE_MLS_ID=UNLOCK

# Optional: Use default API base URL
# BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2
```

### Development Configuration (.env)

```bash
# Required Configuration
BRIDGE_CLIENT_ID=dev_client_id
BRIDGE_CLIENT_SECRET=dev_client_secret
BRIDGE_MLS_ID=UNLOCK
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2

# Development Settings
LOG_LEVEL=DEBUG
API_RATE_LIMIT_PER_MINUTE=30
CACHE_ENABLED=false
CACHE_TTL_SECONDS=60
```

### Production Configuration (.env)

```bash
# Required Configuration
BRIDGE_CLIENT_ID=prod_client_id
BRIDGE_CLIENT_SECRET=prod_client_secret
BRIDGE_MLS_ID=UNLOCK
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2

# Production Settings
LOG_LEVEL=INFO
API_RATE_LIMIT_PER_MINUTE=60
CACHE_ENABLED=false
CACHE_TTL_SECONDS=300
MCP_SERVER_NAME=unlock-mls-mcp-prod
```

## Application Settings Class

The application uses a Pydantic `Settings` class that automatically loads configuration from environment variables. Here's the complete configuration schema:

```python
class Settings(BaseSettings):
    # Bridge Interactive API Configuration
    bridge_api_base_url: str = "https://api.bridgedataoutput.com/api/v2"
    bridge_client_id: str  # Required
    bridge_client_secret: str  # Required
    bridge_mls_id: str = "UNLOCK"
    bridge_server_token: Optional[str] = None

    # MCP Server Configuration
    mcp_server_name: str = "unlock-mls-mcp"
    log_level: str = "INFO"

    # Performance Configuration
    api_rate_limit_per_minute: int = 60
    cache_enabled: bool = False
    cache_ttl_seconds: int = 300

    # Computed Properties
    @property
    def odata_endpoint(self) -> str:
        return f"{self.bridge_api_base_url}/OData/{self.bridge_mls_id}"

    @property
    def token_endpoint(self) -> str:
        return f"{self.bridge_api_base_url}/oauth2/token"

    @property
    def log_level_numeric(self) -> int:
        return getattr(logging, self.log_level.upper(), logging.INFO)
```

## Configuration Validation

The application performs automatic validation of configuration values:

### Required Field Validation
- **Bridge Client ID**: Must be provided, non-empty string
- **Bridge Client Secret**: Must be provided, non-empty string

### Format Validation
- **API Base URL**: Must be a valid URL format
- **Log Level**: Must be one of the valid logging levels
- **Rate Limit**: Must be a positive integer
- **Cache TTL**: Must be a positive integer

### Runtime Validation
- **API Connectivity**: Tests connection to Bridge Interactive API at startup
- **Authentication**: Validates OAuth2 credentials can obtain access token
- **MLS Access**: Verifies access to UNLOCK MLS data

## Troubleshooting Configuration Issues

### Common Configuration Problems

#### 1. Missing Required Variables
**Symptoms**: 
- Server fails to start
- "Required field missing" errors

**Solutions**:
- Ensure `.env` file exists in project root
- Verify all required fields are set:
  - `BRIDGE_CLIENT_ID`
  - `BRIDGE_CLIENT_SECRET`

#### 2. Invalid Credentials
**Symptoms**:
- Authentication errors
- "401 Unauthorized" responses

**Solutions**:
- Verify credentials with Bridge Interactive
- Check for typos in client ID and secret
- Ensure credentials are for the correct environment

#### 3. Network Connectivity Issues
**Symptoms**:
- Connection timeouts
- "Unable to connect" errors

**Solutions**:
- Verify internet connectivity
- Check firewall settings
- Confirm `BRIDGE_API_BASE_URL` is correct

#### 4. Rate Limiting Issues
**Symptoms**:
- "Too many requests" errors
- Intermittent failures

**Solutions**:
- Reduce `API_RATE_LIMIT_PER_MINUTE` setting
- Implement request queuing
- Contact Bridge Interactive about rate limits

### Configuration Testing

To test your configuration:

1. **Basic Connectivity Test**:
   ```bash
   python -c "
   from src.config.settings import get_settings
   settings = get_settings()
   print(f'API URL: {settings.bridge_api_base_url}')
   print(f'Token Endpoint: {settings.token_endpoint}')
   print(f'OData Endpoint: {settings.odata_endpoint}')
   "
   ```

2. **Authentication Test**:
   ```bash
   python -c "
   import asyncio
   from src.auth.oauth2 import OAuth2Handler
   from src.config.settings import get_settings
   
   async def test_auth():
       settings = get_settings()
       handler = OAuth2Handler(settings)
       token = await handler.get_access_token()
       print(f'Token obtained: {bool(token)}')
   
   asyncio.run(test_auth())
   "
   ```

3. **Full System Test**:
   ```bash
   python -m src.server --test
   ```

## Security Considerations

### Environment Variable Security

1. **Never commit secrets**: Use `.env` files that are excluded from version control
2. **Use secure storage**: In production, use secure secret management systems
3. **Rotate credentials**: Regularly rotate API credentials
4. **Limit access**: Restrict access to configuration files

### Recommended Security Practices

1. **Development Environment**:
   - Use separate development credentials
   - Enable debug logging for troubleshooting
   - Use lower rate limits to avoid impacting production quotas

2. **Production Environment**:
   - Use environment-specific credentials
   - Set `LOG_LEVEL=INFO` or `WARNING`
   - Enable monitoring and alerting
   - Use secure credential storage (AWS Secrets Manager, Azure Key Vault, etc.)

3. **Credential Management**:
   ```bash
   # Good: Environment variables
   export BRIDGE_CLIENT_SECRET="secret_value"
   
   # Bad: Hardcoded in code
   BRIDGE_CLIENT_SECRET = "secret_value"  # Don't do this!
   ```

## Configuration Monitoring

The server provides configuration status through the API Status resource:

- Access via `api://status/info` MCP resource
- Shows current configuration values (secrets masked)
- Reports authentication status
- Displays system health information

Example output:
```
## System Configuration
- Log Level: INFO
- Rate Limiting: 60 requests/minute
- Cache Enabled: No
- Cache TTL: 300 seconds

## Authentication Status
- OAuth2 Connection: ✅ Connected
- Bridge API: https://api.bridgedataoutput.com/api/v2
- MLS ID: UNLOCK
```

This configuration guide should help you properly set up and troubleshoot the UNLOCK MLS MCP Server for your specific environment and requirements.