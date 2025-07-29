# RESO API Client Documentation

## Overview

The `ResoWebApiClient` provides a comprehensive, async HTTP client for interacting with Bridge Interactive's RESO Web API. It implements OData query building, automatic authentication, error handling, and data retrieval for all supported RESO resources.

## Architecture

### Client Design

```
MCP Server → ResoWebApiClient → OData Query Builder → 
HTTP Client → Bridge Interactive API → RESO Data → 
Response Processing → Structured Data
```

### Key Components

1. **HTTP Transport**: aiohttp-based async client
2. **Authentication**: Bearer token and OAuth2 integration
3. **OData Builder**: RESO-compliant query construction
4. **Error Handling**: Comprehensive error classification and recovery
5. **Resource Management**: Support for all RESO resource types

## Client Implementation

### Initialization

```python
class ResoWebApiClient:
    def __init__(self,
                 base_url: Optional[str] = None,
                 mls_id: Optional[str] = None,
                 server_token: Optional[str] = None):
        """
        Initialize RESO Web API client.
        
        Args:
            base_url: API base URL (defaults to settings)
            mls_id: MLS identifier (defaults to settings)
            server_token: Bearer token (defaults to settings)
        """
        self.base_url = base_url or settings.bridge_api_base_url
        self.mls_id = mls_id or settings.bridge_mls_id
        self.server_token = server_token or settings.bridge_server_token
        
        # Build OData endpoint URL
        self.odata_endpoint = f"{self.base_url}/OData/{self.mls_id}"
        
        # Resource endpoints
        self.endpoints = {
            "Property": f"{self.odata_endpoint}/Property",
            "Member": f"{self.odata_endpoint}/Member", 
            "Office": f"{self.odata_endpoint}/Office",
            "OpenHouse": f"{self.odata_endpoint}/OpenHouse",
            "Media": f"{self.odata_endpoint}/Media",
            "Lookup": f"{self.odata_endpoint}/Lookup"
        }
```

### Connection Configuration

```python
# Default timeout configuration
self.timeout = aiohttp.ClientTimeout(total=30, connect=10)

# Standard headers
headers = {
    'Authorization': f'Bearer {self.server_token}',
    'Accept': 'application/json',
    'User-Agent': 'UNLOCK-MLS-MCP-Server/1.0'
}
```

## RESO Resources

### Supported Resources

#### Property Resource
- **Endpoint**: `/OData/{MLS_ID}/Property`
- **Purpose**: Real estate listings and property details
- **Key Fields**: ListingId, ListPrice, PropertyType, StandardStatus, Address, Features

#### Member Resource  
- **Endpoint**: `/OData/{MLS_ID}/Member`
- **Purpose**: Real estate agent and member information
- **Key Fields**: MemberKey, MemberFullName, MemberEmail, MemberPhone, Office

#### Office Resource
- **Endpoint**: `/OData/{MLS_ID}/Office`
- **Purpose**: Real estate office and brokerage information
- **Key Fields**: OfficeKey, OfficeName, OfficePhone, OfficeAddress

#### OpenHouse Resource
- **Endpoint**: `/OData/{MLS_ID}/OpenHouse`
- **Purpose**: Open house schedules and information
- **Key Fields**: OpenHouseKey, ListingId, OpenHouseDate, OpenHouseStartTime

#### Media Resource
- **Endpoint**: `/OData/{MLS_ID}/Media`
- **Purpose**: Property photos, virtual tours, and media
- **Key Fields**: MediaKey, ResourceRecordKey, MediaURL, MediaType

#### Lookup Resource
- **Endpoint**: `/OData/{MLS_ID}/Lookup`
- **Purpose**: Reference data and metadata
- **Key Fields**: LookupName, LookupValue, StandardLookupValue

## OData Query Building

### Query Builder Architecture

```python
def _build_odata_query(self, **params) -> str:
    """Build OData query parameters."""
    query_parts = []
    
    # Standard OData parameters
    if params.get("filter"):
        query_parts.append(f"$filter={quote(params['filter'])}")
    
    if params.get("select"):
        fields = params["select"]
        if isinstance(fields, list):
            fields = ",".join(fields)
        query_parts.append(f"$select={quote(fields)}")
    
    if params.get("orderby"):
        query_parts.append(f"$orderby={quote(params['orderby'])}")
    
    if params.get("top"):
        query_parts.append(f"$top={params['top']}")
    
    return "&".join(query_parts)
```

### OData Parameters Supported

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `$filter` | Filter results | `City eq 'Austin'` |
| `$select` | Choose fields | `ListingId,ListPrice,City` |
| `$orderby` | Sort results | `ListPrice desc` |
| `$top` | Limit results | `25` |
| `$skip` | Pagination | `50` |
| `$expand` | Include related data | `Media,OpenHouse` |
| `$count` | Include count | `true` |

### Filter Building

#### Property Filters

```python
def _build_property_filter(self,
                         city: Optional[str] = None,
                         state: Optional[str] = None,
                         zip_code: Optional[str] = None,
                         min_price: Optional[float] = None,
                         max_price: Optional[float] = None,
                         min_bedrooms: Optional[int] = None,
                         property_type: Optional[str] = None,
                         status: Optional[str] = None,
                         **kwargs) -> str:
    """Build property-specific filter string."""
    filters = []
    
    # Status filter (default to Active)
    if status:
        filters.append(f"StandardStatus eq '{status}'")
    else:
        filters.append("StandardStatus eq 'Active'")
    
    # Location filters
    if city:
        filters.append(f"City eq '{city}'")
    if state:
        filters.append(f"StateOrProvince eq '{state}'")
    if zip_code:
        filters.append(f"PostalCode eq '{zip_code}'")
    
    # Price range filters
    if min_price is not None:
        filters.append(f"ListPrice ge {min_price}")
    if max_price is not None:
        filters.append(f"ListPrice le {max_price}")
    
    # Bedroom filters
    if min_bedrooms is not None:
        filters.append(f"BedroomsTotal ge {min_bedrooms}")
    
    return " and ".join(filters)
```

#### Filter Examples

```python
# Basic location filter
"City eq 'Austin' and StateOrProvince eq 'TX'"

# Price range filter  
"ListPrice ge 300000 and ListPrice le 500000"

# Complex multi-criteria filter
"City eq 'Austin' and StateOrProvince eq 'TX' and BedroomsTotal ge 3 and ListPrice le 500000 and StandardStatus eq 'Active'"

# Property type filter
"PropertyType eq 'Residential' and PropertySubType eq 'Single Family Residence'"
```

### Query Construction Examples

#### Property Search Query

```python
# Build query for 3+ bedroom homes under $500k in Austin
query_params = {
    "filter": "City eq 'Austin' and StateOrProvince eq 'TX' and BedroomsTotal ge 3 and ListPrice le 500000",
    "select": ["ListingId", "ListPrice", "BedroomsTotal", "BathroomsTotalInteger", "LivingArea", "City", "StateOrProvince"],
    "orderby": "ListPrice asc",
    "top": 25
}

query_string = self._build_odata_query(**query_params)
# Result: $filter=City%20eq%20%27Austin%27%20and%20StateOrProvince%20eq%20%27TX%27&$select=ListingId%2CListPrice&$orderby=ListPrice%20asc&$top=25
```

#### Member Search Query

```python
# Build query for agents in Austin, TX
query_params = {
    "filter": "MemberCity eq 'Austin' and MemberStateOrProvince eq 'TX'",
    "select": ["MemberKey", "MemberFullName", "MemberEmail", "MemberMobilePhone", "MemberOfficeName"],
    "orderby": "MemberFullName asc",
    "top": 20
}
```

## HTTP Client Implementation

### Request Handling

```python
async def _make_request(self,
                      session: aiohttp.ClientSession,
                      method: str,
                      url: str,
                      **kwargs) -> Dict[str, Any]:
    """
    Make an authenticated request to the RESO API.
    
    Args:
        session: aiohttp client session
        method: HTTP method
        url: Request URL
        **kwargs: Additional request parameters
        
    Returns:
        Parsed JSON response
        
    Raises:
        ResoApiError: If request fails
    """
    try:
        # Add Bearer token authentication
        headers = kwargs.get('headers', {})
        headers.update({
            'Authorization': f'Bearer {self.server_token}',
            'Accept': 'application/json',
            'User-Agent': 'UNLOCK-MLS-MCP-Server/1.0'
        })
        kwargs['headers'] = headers
        kwargs['timeout'] = self.timeout
        
        response = await session.request(method, url, **kwargs)
        response.raise_for_status()
        
        # Handle different content types
        content_type = response.headers.get("content-type", "").lower()
        if "application/json" in content_type:
            data = await response.json()
        else:
            text = await response.text()
            raise ResoApiError(f"Unexpected content type: {content_type}")
        
        logger.debug("API request successful: %s %s", method, url)
        return data
        
    except ClientResponseError as e:
        error_msg = self._classify_http_error(e.status, e.message)
        logger.error("API request failed: %s %s - %s", method, url, error_msg)
        raise ResoApiError(error_msg) from e
        
    except ClientError as e:
        logger.error("Network error: %s", str(e))
        raise ResoApiError(f"Network error: {str(e)}") from e
```

### Error Classification

```python
def _classify_http_error(self, status: int, message: str) -> str:
    """Classify HTTP errors into user-friendly messages."""
    error_messages = {
        400: "Bad request - check query parameters",
        401: "Authentication failed - check credentials",
        403: "Forbidden - check permissions for this MLS",
        404: "Resource not found",
        429: "Rate limit exceeded - please wait and retry",
        500: "Server error - try again later",
        502: "Bad gateway - service temporarily unavailable",
        503: "Service unavailable - try again later",
        504: "Gateway timeout - request took too long"
    }
    
    if status in error_messages:
        return error_messages[status]
    elif status >= 500:
        return "Server error - try again later"
    elif status >= 400:
        return f"Client error {status}: {message}"
    else:
        return f"HTTP {status}: {message}"
```

## Resource-Specific Methods

### Property Queries

```python
async def query_properties(self,
                         filters: Optional[Dict[str, Any]] = None,
                         limit: int = 25,
                         fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Query properties with specified filters.
    
    Args:
        filters: Property search filters
        limit: Maximum number of results
        fields: Specific fields to retrieve
        
    Returns:
        List of property records
    """
    if not filters:
        filters = {}
    
    # Build OData filter
    filter_string = self._build_property_filter(**filters)
    
    # Select fields
    select_fields = fields or [
        "ListingId", "ListingKey", "StandardStatus", "ListPrice",
        "BedroomsTotal", "BathroomsTotalInteger", "LivingArea",
        "PropertyType", "PropertySubType", "City", "StateOrProvince",
        "PostalCode", "ModificationTimestamp", "OnMarketDate"
    ]
    
    # Build query parameters
    query_params = {
        "filter": filter_string,
        "select": select_fields,
        "orderby": "ModificationTimestamp desc",
        "top": min(limit, 1000)  # API limit
    }
    
    # Build URL
    query_string = self._build_odata_query(**query_params)
    url = f"{self.endpoints['Property']}?{query_string}"
    
    # Execute request
    async with aiohttp.ClientSession() as session:
        response = await self._make_request(session, "GET", url)
        
        # Extract data from OData response
        if "value" in response:
            return response["value"]
        else:
            return response if isinstance(response, list) else [response]
```

### Member Queries

```python
async def query_members(self,
                       filters: Optional[Dict[str, Any]] = None,
                       limit: int = 20,
                       fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Query members (agents) with specified filters.
    
    Args:
        filters: Member search filters
        limit: Maximum number of results
        fields: Specific fields to retrieve
        
    Returns:
        List of member records
    """
    if not filters:
        filters = {}
    
    # Build member filter
    filter_parts = []
    
    if filters.get("MemberFullName"):
        # Support partial name matching
        name = filters["MemberFullName"]
        filter_parts.append(f"contains(MemberFullName, '{name}')")
    
    if filters.get("MemberCity"):
        filter_parts.append(f"MemberCity eq '{filters['MemberCity']}'")
    
    if filters.get("MemberStateOrProvince"):
        filter_parts.append(f"MemberStateOrProvince eq '{filters['MemberStateOrProvince']}'")
    
    if filters.get("MemberOfficeName"):
        office = filters["MemberOfficeName"]
        filter_parts.append(f"contains(MemberOfficeName, '{office}')")
    
    filter_string = " and ".join(filter_parts) if filter_parts else None
    
    # Select fields
    select_fields = fields or [
        "MemberKey", "MemberFirstName", "MemberLastName", "MemberFullName",
        "MemberEmail", "MemberMobilePhone", "MemberDirectPhone",
        "MemberOfficeName", "MemberCity", "MemberStateOrProvince",
        "MemberStateLicense", "MemberDesignation"
    ]
    
    # Build query
    query_params = {
        "select": select_fields,
        "orderby": "MemberFullName asc",
        "top": min(limit, 500)
    }
    
    if filter_string:
        query_params["filter"] = filter_string
    
    query_string = self._build_odata_query(**query_params)
    url = f"{self.endpoints['Member']}?{query_string}"
    
    # Execute request
    async with aiohttp.ClientSession() as session:
        response = await self._make_request(session, "GET", url)
        return response.get("value", response)
```

### Office Queries

```python
async def query_offices(self,
                       filters: Optional[Dict[str, Any]] = None,
                       limit: int = 50) -> List[Dict[str, Any]]:
    """Query office/brokerage information."""
    
    # Build office filter
    filter_parts = []
    
    if filters and filters.get("OfficeName"):
        office_name = filters["OfficeName"]
        filter_parts.append(f"contains(OfficeName, '{office_name}')")
    
    if filters and filters.get("OfficeCity"):
        filter_parts.append(f"OfficeCity eq '{filters['OfficeCity']}'")
    
    # Execute query similar to members/properties
    # ... implementation continues
```

## Performance Optimization

### Connection Management

```python
class ConnectionManager:
    def __init__(self, max_connections: int = 100):
        self.connector = aiohttp.TCPConnector(
            limit=max_connections,
            limit_per_host=20,
            keepalive_timeout=60
        )
        self.session = None
    
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create persistent session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                connector=self.connector,
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    async def close(self):
        """Clean up connections."""
        if self.session and not self.session.closed:
            await self.session.close()
```

### Caching Strategy

```python
from functools import lru_cache
from datetime import datetime, timedelta

class QueryCache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def _cache_key(self, endpoint: str, params: Dict) -> str:
        """Generate cache key from endpoint and parameters."""
        param_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        return f"{endpoint}?{param_str}"
    
    def get(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """Get cached response if available and fresh."""
        key = self._cache_key(endpoint, params)
        
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.utcnow() - timestamp < timedelta(seconds=self.ttl):
                return data
            else:
                del self.cache[key]
        
        return None
    
    def set(self, endpoint: str, params: Dict, data: Dict):
        """Cache response data."""
        key = self._cache_key(endpoint, params)
        self.cache[key] = (data, datetime.utcnow())
```

### Batch Operations

```python
async def batch_property_queries(self, 
                                query_list: List[Dict[str, Any]]) -> List[List[Dict]]:
    """Execute multiple property queries concurrently."""
    
    async def execute_query(filters):
        try:
            return await self.query_properties(filters)
        except Exception as e:
            logger.error("Batch query failed: %s", e)
            return []
    
    # Execute queries concurrently
    tasks = [execute_query(filters) for filters in query_list]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle results and exceptions
    processed_results = []
    for result in results:
        if isinstance(result, Exception):
            logger.error("Batch query exception: %s", result)
            processed_results.append([])
        else:
            processed_results.append(result)
    
    return processed_results
```

## Error Handling and Recovery

### Error Classification

```python
class ResoApiError(Exception):
    """Base exception for RESO API related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
        self.is_retryable = self._is_retryable_error(status_code)
    
    def _is_retryable_error(self, status_code: Optional[int]) -> bool:
        """Determine if error is retryable."""
        if not status_code:
            return False
        
        # Retryable status codes
        retryable_codes = {429, 500, 502, 503, 504}
        return status_code in retryable_codes

class AuthenticationError(ResoApiError):
    """Authentication-related errors."""
    pass

class RateLimitError(ResoApiError):
    """Rate limiting errors."""
    pass

class ValidationError(ResoApiError):
    """Query validation errors."""
    pass
```

### Retry Logic

```python
import asyncio
import random

async def retry_with_backoff(operation, 
                           max_retries: int = 3,
                           base_delay: float = 1.0,
                           max_delay: float = 60.0):
    """Execute operation with exponential backoff retry."""
    
    for attempt in range(max_retries + 1):
        try:
            return await operation()
        except ResoApiError as e:
            if not e.is_retryable or attempt == max_retries:
                raise
            
            # Calculate delay with jitter
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0.1, 0.3) * delay
            total_delay = delay + jitter
            
            logger.warning(
                "API request failed (attempt %d/%d), retrying in %.2f seconds: %s",
                attempt + 1, max_retries + 1, total_delay, str(e)
            )
            
            await asyncio.sleep(total_delay)
    
    raise ResoApiError(f"Operation failed after {max_retries} retries")
```

## Testing and Validation

### Unit Testing

```python
import pytest
from unittest.mock import AsyncMock, patch

class TestResoWebApiClient:
    
    @pytest.fixture
    def client(self):
        return ResoWebApiClient(
            base_url="https://api.test.com",
            mls_id="test_mls",
            server_token="test_token"
        )
    
    @pytest.mark.asyncio
    async def test_property_query_building(self, client):
        """Test property filter building."""
        filter_string = client._build_property_filter(
            city="Austin",
            state="TX",
            min_price=300000,
            max_price=500000,
            min_bedrooms=3
        )
        
        expected = "StandardStatus eq 'Active' and City eq 'Austin' and StateOrProvince eq 'TX' and ListPrice ge 300000 and ListPrice le 500000 and BedroomsTotal ge 3"
        assert filter_string == expected
    
    @pytest.mark.asyncio
    async def test_odata_query_building(self, client):
        """Test OData query parameter building."""
        query = client._build_odata_query(
            filter="City eq 'Austin'",
            select=["ListingId", "ListPrice"],
            orderby="ListPrice desc",
            top=25
        )
        
        assert "$filter=" in query
        assert "$select=" in query
        assert "$orderby=" in query
        assert "$top=25" in query
    
    @pytest.mark.asyncio
    async def test_error_handling(self, client):
        """Test API error handling."""
        with patch('aiohttp.ClientSession.request') as mock_request:
            mock_request.side_effect = aiohttp.ClientResponseError(
                request_info=None,
                history=(),
                status=404,
                message="Not Found"
            )
            
            with pytest.raises(ResoApiError) as exc_info:
                await client.query_properties()
            
            assert "Resource not found" in str(exc_info.value)
```

### Integration Testing

```python
@pytest.mark.integration
class TestResoApiIntegration:
    
    @pytest.mark.asyncio
    async def test_real_property_query(self):
        """Test with real API credentials."""
        if not os.getenv('BRIDGE_SERVER_TOKEN'):
            pytest.skip("Real API credentials not available")
        
        client = ResoWebApiClient()
        
        # Test basic property query
        properties = await client.query_properties(
            filters={"city": "Austin", "state": "TX"},
            limit=5
        )
        
        assert isinstance(properties, list)
        assert len(properties) <= 5
        
        if properties:
            property_data = properties[0]
            assert "ListingId" in property_data
            assert "ListPrice" in property_data
```

## Configuration and Deployment

### Environment Configuration

```python
# Required environment variables
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2
BRIDGE_MLS_ID=your_mls_id
BRIDGE_SERVER_TOKEN=your_server_token

# Optional performance tuning
API_RATE_LIMIT_PER_MINUTE=60
API_CONNECTION_TIMEOUT=30
API_REQUEST_TIMEOUT=120
CACHE_ENABLED=true
CACHE_TTL_SECONDS=300
```

### Production Monitoring

```python
from prometheus_client import Counter, Histogram, Gauge

# Metrics for monitoring
api_requests_total = Counter('reso_api_requests_total', 'Total API requests', ['endpoint', 'status'])
api_request_duration = Histogram('reso_api_request_duration_seconds', 'API request duration')
api_cache_hits = Counter('reso_api_cache_hits_total', 'API cache hits')
api_cache_misses = Counter('reso_api_cache_misses_total', 'API cache misses')

class MonitoredResoClient(ResoWebApiClient):
    async def _make_request(self, session, method, url, **kwargs):
        start_time = time.time()
        endpoint = url.split('/')[-1].split('?')[0]
        
        try:
            response = await super()._make_request(session, method, url, **kwargs)
            api_requests_total.labels(endpoint=endpoint, status='success').inc()
            return response
        except Exception as e:
            api_requests_total.labels(endpoint=endpoint, status='error').inc()
            raise
        finally:
            api_request_duration.observe(time.time() - start_time)
```

This comprehensive RESO API client provides robust, efficient, and production-ready access to Bridge Interactive's RESO Web API, with full OData support, intelligent error handling, and performance optimization.