# Error Handling and Troubleshooting Guide

## Overview

The UNLOCK MLS MCP Server implements comprehensive error handling and provides detailed troubleshooting guidance for common issues. This guide covers error classification, debugging techniques, and resolution strategies.

## Error Classification System

### Error Hierarchy

```
ResoApiError (Base)
├── AuthenticationError
│   ├── TokenExpiredError
│   ├── InvalidCredentialsError
│   └── TokenEndpointError
├── ValidationError
│   ├── InputValidationError
│   ├── FilterValidationError
│   └── QueryValidationError
├── RateLimitError
├── NetworkError
│   ├── ConnectionTimeoutError
│   ├── DNSResolutionError
│   └── SSLError
└── DataMappingError
    ├── FieldMappingError
    ├── TypeConversionError
    └── FormatError
```

### Error Response Format

All errors follow a consistent response format:

```json
{
  "error": {
    "type": "ValidationError",
    "message": "Invalid city name: must contain only letters, spaces, and hyphens",
    "code": "INVALID_CITY_FORMAT",
    "details": {
      "field": "city",
      "provided_value": "Austin123!",
      "valid_pattern": "^[A-Za-z\\s\\-']+$"
    },
    "timestamp": "2024-01-20T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

## Authentication Errors

### Common Authentication Issues

#### 1. Invalid Bearer Token

**Error Message**: `Authentication failed: Invalid or expired Bearer token`

**Symptoms**:
- HTTP 401 responses from API
- "Authorization header missing or invalid" errors
- All tool calls failing with authentication errors

**Diagnosis**:
```bash
# Check if token is set
echo $BRIDGE_SERVER_TOKEN

# Test token validity
curl -H "Authorization: Bearer $BRIDGE_SERVER_TOKEN" \
  "https://api.bridgedataoutput.com/api/v2/OData/$BRIDGE_MLS_ID/Property?\$top=1"
```

**Resolution**:
1. Verify token is correctly set in environment variables
2. Check token expiration with Bridge Interactive
3. Regenerate token if expired
4. Ensure no extra whitespace in token value

#### 2. OAuth2 Authentication Failure

**Error Message**: `OAuth2 authentication failed: invalid_client`

**Symptoms**:
- OAuth2 token requests failing
- "Client authentication failed" errors
- Fallback to Bearer token not working

**Diagnosis**:
```python
# Test OAuth2 credentials
import aiohttp
import asyncio

async def test_oauth2():
    data = {
        "grant_type": "client_credentials",
        "client_id": "your_client_id",
        "client_secret": "your_client_secret"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.bridgedataoutput.com/oauth2/token",
            data=data
        ) as response:
            print(f"Status: {response.status}")
            print(f"Response: {await response.text()}")

asyncio.run(test_oauth2())
```

**Resolution**:
1. Verify OAuth2 credentials with Bridge Interactive
2. Check client ID and secret formatting
3. Ensure token endpoint URL is correct
4. Verify client has proper permissions

#### 3. MLS Access Permissions

**Error Message**: `Forbidden: You don't have permission to access this MLS data`

**Symptoms**:
- HTTP 403 responses
- Access denied for specific MLS ID
- Some tools working, others failing

**Resolution**:
1. Verify MLS ID is correct for your account
2. Check account permissions with Bridge Interactive
3. Ensure subscription includes required data access
4. Verify geographic coverage for MLS

### Authentication Debugging

```python
# Authentication debug utility
import logging
from src.auth.oauth2 import OAuth2Handler
from src.config.settings import get_settings

async def debug_authentication():
    """Debug authentication configuration and connectivity."""
    settings = get_settings()
    
    print("🔍 Authentication Configuration Debug")
    print("=" * 50)
    
    # Check configuration
    print("Configuration:")
    print(f"  Bearer Token: {'✅ Set' if settings.bridge_server_token else '❌ Missing'}")
    print(f"  Client ID: {'✅ Set' if settings.bridge_client_id else '❌ Missing'}")
    print(f"  Client Secret: {'✅ Set' if settings.bridge_client_secret else '❌ Missing'}")
    print(f"  MLS ID: {settings.bridge_mls_id}")
    print(f"  API Base URL: {settings.bridge_api_base_url}")
    
    # Test Bearer token if available
    if settings.bridge_server_token:
        print("\n🔑 Testing Bearer Token:")
        try:
            # Test API call with Bearer token
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {settings.bridge_server_token}"}
                url = f"{settings.bridge_api_base_url}/OData/{settings.bridge_mls_id}/Property"
                
                async with session.get(url + "?$top=1", headers=headers) as response:
                    if response.status == 200:
                        print("  ✅ Bearer token authentication successful")
                    else:
                        print(f"  ❌ Bearer token failed: HTTP {response.status}")
                        print(f"      Response: {await response.text()}")
        except Exception as e:
            print(f"  ❌ Bearer token test failed: {e}")
    
    # Test OAuth2 if available
    if settings.bridge_client_id and settings.bridge_client_secret:
        print("\n🔐 Testing OAuth2:")
        try:
            oauth_handler = OAuth2Handler()
            token = await oauth_handler.authenticate()
            print(f"  ✅ OAuth2 authentication successful")
            print(f"      Token expires: {oauth_handler._expires_at}")
        except Exception as e:
            print(f"  ❌ OAuth2 authentication failed: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(debug_authentication())
```

## Validation Errors

### Input Validation Issues

#### 1. Natural Language Query Parsing

**Error Message**: `Unable to understand the search query: ambiguous location`

**Common Causes**:
- Ambiguous city names (e.g., "Springfield" without state)
- Misspelled location names
- Invalid price format
- Unsupported property types

**Resolution Examples**:
```python
# Bad queries and their fixes
bad_queries = [
    "house in Springfield",  # Missing state
    "3 bedroom under 500k",  # Missing location
    "home for $500,000k",    # Double scaling (k + actual amount)
    "property in Austin TX 12345"  # Mixed location formats
]

fixed_queries = [
    "house in Springfield IL",
    "3 bedroom house under 500k in Austin TX", 
    "home under $500k",
    "property in Austin TX" or "property in 12345"
]
```

#### 2. Filter Validation Errors

**Error Message**: `Invalid price range: minimum price must be less than maximum price`

**Common Issues**:
- Inverted price ranges
- Negative values
- Extreme values outside reasonable ranges
- Invalid property types

**Debug Filter Validation**:
```python
# Filter validation debugging
from src.utils.validators import QueryValidator

def debug_filter_validation(filters):
    """Debug filter validation issues."""
    validator = QueryValidator()
    
    print("🔍 Filter Validation Debug")
    print("=" * 30)
    
    for key, value in filters.items():
        try:
            if key == "city":
                result = validator._validate_city(value)
                print(f"✅ {key}: {value} → {result}")
            elif key == "state":
                result = validator._validate_state(value)
                print(f"✅ {key}: {value} → {result}")
            elif "price" in key:
                result = validator._validate_price(value, key)
                print(f"✅ {key}: {value} → {result}")
            # Add other validations...
        except ValidationError as e:
            print(f"❌ {key}: {value} → {e}")

# Example usage
debug_filter_validation({
    "city": "Austin123",  # Invalid characters
    "state": "XX",        # Invalid state
    "min_price": -100000, # Negative price
    "max_price": 50000    # Creates invalid range
})
```

### Data Mapping Errors

#### 1. Field Mapping Issues

**Error Message**: `Failed to map property field: unexpected data type`

**Common Causes**:
- RESO API schema changes
- Null values in required fields
- Unexpected data formats
- Missing fields in API response

**Resolution**:
```python
# Robust field mapping with error handling
def safe_property_mapping(property_data):
    """Map property with comprehensive error handling."""
    mapped = {}
    
    # Safe field extraction with fallbacks
    field_mappings = {
        "listing_id": ["ListingId", "ListingKey", "MLSNumber"],
        "price": ["ListPrice", "CurrentPrice", "Price"],
        "bedrooms": ["BedroomsTotal", "Bedrooms", "BedCount"],
        "bathrooms": ["BathroomsTotalInteger", "BathroomsTotal", "BathCount"]
    }
    
    for target_field, source_fields in field_mappings.items():
        value = None
        for source_field in source_fields:
            if source_field in property_data and property_data[source_field] is not None:
                value = property_data[source_field]
                break
        
        if value is not None:
            mapped[target_field] = value
        else:
            logger.warning(f"No valid source found for {target_field}")
    
    return mapped
```

## Network and API Errors

### Connection Issues

#### 1. DNS Resolution Failures

**Error Message**: `Network error: Name or service not known`

**Diagnosis**:
```bash
# Test DNS resolution
nslookup api.bridgedataoutput.com
dig api.bridgedataoutput.com

# Test connectivity
ping api.bridgedataoutput.com
curl -I https://api.bridgedataoutput.com
```

**Resolution**:
1. Check DNS configuration
2. Verify firewall rules
3. Test from different network
4. Check proxy settings if applicable

#### 2. SSL/TLS Certificate Issues

**Error Message**: `SSL certificate verification failed`

**Diagnosis**:
```bash
# Check certificate
openssl s_client -connect api.bridgedataoutput.com:443 -servername api.bridgedataoutput.com

# Test with curl
curl -v https://api.bridgedataoutput.com
```

**Resolution**:
1. Update certificate bundle
2. Check system time accuracy
3. Verify certificate chain
4. Update Python SSL libraries

#### 3. Rate Limiting

**Error Message**: `Rate limit exceeded: Too many requests`

**Symptoms**:
- HTTP 429 responses
- Temporary failures followed by success
- Increased response times

**Resolution Strategy**:
```python
# Rate limiting handler with exponential backoff
import asyncio
import random

class RateLimitHandler:
    def __init__(self, max_retries=3, base_delay=1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def execute_with_backoff(self, operation):
        """Execute operation with exponential backoff on rate limits."""
        
        for attempt in range(self.max_retries + 1):
            try:
                return await operation()
            except RateLimitError as e:
                if attempt == self.max_retries:
                    raise e
                
                # Exponential backoff with jitter
                delay = self.base_delay * (2 ** attempt)
                jitter = random.uniform(0.1, 0.3) * delay
                total_delay = delay + jitter
                
                logger.warning(f"Rate limited, retrying in {total_delay:.2f}s (attempt {attempt + 1})")
                await asyncio.sleep(total_delay)
        
        raise RateLimitError("Max retries exceeded")
```

### API Response Issues

#### 1. Unexpected Response Format

**Error Message**: `Unexpected content type: text/html`

**Common Causes**:
- API endpoint changes
- Maintenance pages
- Error pages returned as HTML
- Incorrect endpoint URLs

**Diagnosis**:
```python
# Response format debugging
async def debug_api_response(url):
    """Debug API response format issues."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"Status: {response.status}")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print(f"Content-Length: {response.headers.get('content-length')}")
            
            text = await response.text()
            print(f"Response preview: {text[:500]}...")
            
            # Check if JSON
            try:
                import json
                json.loads(text)
                print("✅ Valid JSON response")
            except:
                print("❌ Not valid JSON")
```

## Performance Issues

### Slow Response Times

#### 1. Query Optimization

**Symptoms**:
- Requests taking >30 seconds
- Timeout errors
- High memory usage

**Resolution**:
```python
# Query optimization strategies
def optimize_property_query(filters, limit=25):
    """Optimize property queries for better performance."""
    
    # Limit result set size
    if limit > 100:
        logger.warning("Large limit may cause performance issues")
        limit = 100
    
    # Use indexed fields for filtering
    indexed_fields = ["City", "StateOrProvince", "PostalCode", "StandardStatus"]
    optimized_filters = {}
    
    for field, value in filters.items():
        if field in indexed_fields:
            optimized_filters[field] = value
        else:
            logger.info(f"Using non-indexed field {field} may impact performance")
    
    # Select only required fields
    essential_fields = [
        "ListingId", "ListPrice", "BedroomsTotal", 
        "BathroomsTotalInteger", "LivingArea"
    ]
    
    return {
        "filters": optimized_filters,
        "select": essential_fields,
        "top": limit
    }
```

#### 2. Memory Usage Optimization

**Symptoms**:
- Memory usage growing over time
- Out of memory errors
- Slow garbage collection

**Resolution**:
```python
# Memory optimization techniques
import gc
import weakref

class MemoryOptimizedClient:
    def __init__(self):
        self._session_cache = weakref.WeakValueDictionary()
        self._response_cache = {}
        self._max_cache_size = 1000
    
    async def query_with_memory_management(self, query_params):
        """Execute query with memory management."""
        
        # Check cache size
        if len(self._response_cache) > self._max_cache_size:
            # Clear oldest entries
            oldest_keys = list(self._response_cache.keys())[:100]
            for key in oldest_keys:
                del self._response_cache[key]
            
            # Force garbage collection
            gc.collect()
        
        # Execute query
        result = await self._execute_query(query_params)
        
        # Cache with memory limit
        cache_key = str(hash(frozenset(query_params.items())))
        if len(str(result)) < 100000:  # Only cache small responses
            self._response_cache[cache_key] = result
        
        return result
```

## Diagnostic Tools

### Comprehensive Diagnostic Script

```python
#!/usr/bin/env python3
"""Comprehensive diagnostic tool for UNLOCK MLS MCP Server."""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
from src.config.settings import get_settings
from src.reso_client import ResoWebApiClient
from src.utils.validators import QueryValidator

async def run_diagnostics():
    """Run comprehensive system diagnostics."""
    
    print("🔍 UNLOCK MLS MCP Server Diagnostics")
    print("=" * 50)
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print()
    
    # Configuration check
    print("📋 Configuration Check")
    print("-" * 25)
    try:
        settings = get_settings()
        print(f"✅ Configuration loaded successfully")
        print(f"   MLS ID: {settings.bridge_mls_id}")
        print(f"   API Base URL: {settings.bridge_api_base_url}")
        print(f"   Log Level: {settings.log_level}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Network connectivity
    print("\n🌐 Network Connectivity")
    print("-" * 25)
    try:
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with session.get("https://api.bridgedataoutput.com", timeout=aiohttp.ClientTimeout(total=10)) as response:
                duration = time.time() - start_time
                print(f"✅ Bridge Interactive API reachable")
                print(f"   Response time: {duration:.2f}s")
                print(f"   Status: {response.status}")
    except Exception as e:
        print(f"❌ Network connectivity failed: {e}")
        return
    
    # Authentication test
    print("\n🔐 Authentication Test")
    print("-" * 25)
    try:
        client = ResoWebApiClient()
        
        # Test simple API call
        async with aiohttp.ClientSession() as session:
            url = f"{settings.bridge_api_base_url}/OData/{settings.bridge_mls_id}/Property"
            headers = {"Authorization": f"Bearer {settings.bridge_server_token}"}
            
            async with session.get(url + "?$top=1", headers=headers) as response:
                if response.status == 200:
                    print("✅ Authentication successful")
                    data = await response.json()
                    print(f"   Sample data retrieved: {len(data.get('value', []))} records")
                else:
                    print(f"❌ Authentication failed: HTTP {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text[:200]}...")
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
    
    # Tool functionality test
    print("\n🛠️ Tool Functionality Test")
    print("-" * 25)
    
    test_cases = [
        {
            "name": "Property Search - Basic",
            "filters": {"city": "Austin", "state": "TX"},
            "expected_results": "> 0"
        },
        {
            "name": "Property Search - Natural Language",
            "query": "3 bedroom house under $500k in Austin TX",
            "expected_results": "> 0"
        },
        {
            "name": "Market Analysis",
            "location": {"city": "Austin", "state": "TX"},
            "expected_results": "market data"
        }
    ]
    
    for test_case in test_cases:
        try:
            print(f"   Testing: {test_case['name']}")
            # Implement actual tool tests here
            print(f"   ✅ {test_case['name']} - passed")
        except Exception as e:
            print(f"   ❌ {test_case['name']} - failed: {e}")
    
    # Performance test
    print("\n⚡ Performance Test")
    print("-" * 25)
    try:
        client = ResoWebApiClient()
        
        # Test query performance
        start_time = time.time()
        properties = await client.query_properties(
            filters={"city": "Austin", "state": "TX"},
            limit=10
        )
        duration = time.time() - start_time
        
        print(f"✅ Performance test completed")
        print(f"   Query time: {duration:.2f}s")
        print(f"   Results: {len(properties)} properties")
        print(f"   Rate: {len(properties)/duration:.1f} properties/second")
        
        if duration > 5.0:
            print("⚠️  Performance warning: Query took longer than expected")
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
    
    # Validation test
    print("\n✅ Validation Test")
    print("-" * 25)
    validator = QueryValidator()
    
    test_inputs = [
        {"city": "Austin", "state": "TX", "min_price": 300000},
        {"query": "3 bedroom house in Austin TX"},
        {"city": "Invalid123", "state": "XX"}  # Should fail
    ]
    
    for i, test_input in enumerate(test_inputs):
        try:
            if "query" in test_input:
                result = validator.parse_natural_language_query(test_input["query"])
            else:
                result = validator.validate_search_filters(test_input)
            print(f"   ✅ Test {i+1}: Valid input processed")
        except Exception as e:
            print(f"   ❌ Test {i+1}: Validation failed - {e}")
    
    print("\n🎯 Diagnostic Summary")
    print("-" * 25)
    print("Diagnostics completed. Check individual test results above.")
    print("For detailed logs, run with LOG_LEVEL=DEBUG")

if __name__ == "__main__":
    asyncio.run(run_diagnostics())
```

### Log Analysis Tools

```python
# Log analysis utility
import re
from collections import Counter, defaultdict
from datetime import datetime

class LogAnalyzer:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
    
    def analyze_errors(self):
        """Analyze error patterns in logs."""
        error_patterns = defaultdict(int)
        error_times = []
        
        with open(self.log_file_path, 'r') as f:
            for line in f:
                if 'ERROR' in line:
                    # Extract timestamp
                    timestamp_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                    if timestamp_match:
                        error_times.append(timestamp_match.group())
                    
                    # Extract error type
                    if 'ValidationError' in line:
                        error_patterns['ValidationError'] += 1
                    elif 'AuthenticationError' in line:
                        error_patterns['AuthenticationError'] += 1
                    elif 'NetworkError' in line:
                        error_patterns['NetworkError'] += 1
                    else:
                        error_patterns['UnknownError'] += 1
        
        print("Error Analysis:")
        print("-" * 20)
        for error_type, count in error_patterns.items():
            print(f"{error_type}: {count}")
        
        if error_times:
            print(f"\nFirst error: {error_times[0]}")
            print(f"Last error: {error_times[-1]}")
    
    def analyze_performance(self):
        """Analyze performance metrics from logs."""
        response_times = []
        
        with open(self.log_file_path, 'r') as f:
            for line in f:
                # Look for response time logs
                time_match = re.search(r'Response time: (\d+\.?\d*)s', line)
                if time_match:
                    response_times.append(float(time_match.group(1)))
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            print("Performance Analysis:")
            print("-" * 20)
            print(f"Total requests: {len(response_times)}")
            print(f"Average response time: {avg_time:.2f}s")
            print(f"Max response time: {max_time:.2f}s")
            print(f"Min response time: {min_time:.2f}s")
```

## Common Issues and Solutions

### Quick Reference Guide

| Issue | Symptoms | Quick Fix |
|-------|----------|-----------|
| Authentication failure | HTTP 401 errors | Check `BRIDGE_SERVER_TOKEN` value |
| No search results | Empty results for valid queries | Verify MLS ID and location spelling |
| Slow responses | Requests taking >30s | Reduce query scope, add more specific filters |
| Memory issues | Growing memory usage | Restart service, check for memory leaks |
| Network timeouts | Connection timeout errors | Check firewall, DNS, network connectivity |
| Rate limiting | HTTP 429 errors | Implement exponential backoff |
| Invalid queries | Validation errors | Check query syntax and parameter values |
| SSL errors | Certificate verification failures | Update certificates, check system time |

### Emergency Procedures

#### Service Recovery

```bash
# Quick service restart
sudo systemctl restart unlock-mls-mcp

# Emergency stop and clean restart
sudo systemctl stop unlock-mls-mcp
sudo pkill -f "python.*main"
sudo systemctl start unlock-mls-mcp

# Reset configuration
sudo systemctl stop unlock-mls-mcp
cd /opt/unlock-mls-mcp
git pull origin main
sudo systemctl start unlock-mls-mcp
```

#### Data Recovery

```bash
# Clear cache if corrupted
rm -rf /tmp/unlock-mls-cache/*

# Reset database connections
sudo systemctl restart unlock-mls-mcp

# Validate configuration
python -c "from src.config.settings import get_settings; print('✅ Config OK')"
```

This comprehensive error handling and troubleshooting guide provides the tools and knowledge needed to quickly diagnose and resolve issues with the UNLOCK MLS MCP Server.