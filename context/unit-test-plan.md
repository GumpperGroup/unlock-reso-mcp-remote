# ACTRIS MLS MCP Server Unit Test Plan

## Test Structure Overview

```
tests/
├── __init__.py
├── test_server.py           # MCP server tests
├── test_reso_client.py      # RESO API client tests
├── test_oauth2.py           # Authentication tests
├── test_data_mapper.py      # Data formatting tests
├── test_validators.py       # Input validation tests
├── test_tools/              # MCP tool tests
│   ├── __init__.py
│   ├── test_search_properties.py
│   ├── test_property_details.py
│   ├── test_market_analysis.py
│   └── test_find_agent.py
├── fixtures/                # Test data
│   ├── __init__.py
│   ├── property_data.json
│   ├── member_data.json
│   └── market_data.json
└── conftest.py             # Pytest configuration
```

## 1. Authentication Tests (`test_oauth2.py`)

### Test Cases:
- ✓ Successful OAuth2 token retrieval
- ✓ Token refresh when expired
- ✓ Handle authentication failures
- ✓ Retry logic for token requests
- ✓ Token storage and expiration tracking

```python
class TestOAuth2Authentication:
    def test_successful_authentication(self):
        """Test successful OAuth2 client credentials flow"""
        
    def test_token_refresh_on_expiry(self):
        """Test automatic token refresh when expired"""
        
    def test_authentication_failure_handling(self):
        """Test handling of invalid credentials"""
        
    def test_token_persistence(self):
        """Test token storage and retrieval"""
```

## 2. RESO Client Tests (`test_reso_client.py`)

### Test Cases:
- ✓ Client initialization
- ✓ Query parameter building
- ✓ API request execution
- ✓ Response parsing
- ✓ Error handling
- ✓ Rate limiting compliance

```python
class TestResoWebApiClient:
    def test_client_initialization(self):
        """Test client setup with credentials"""
        
    def test_odata_query_building(self):
        """Test OData filter string generation"""
        
    def test_property_query_execution(self):
        """Test successful property queries"""
        
    def test_api_error_handling(self):
        """Test handling of API errors (401, 403, 404, 500)"""
        
    def test_response_parsing(self):
        """Test parsing of OData responses"""
```

## 3. Data Mapper Tests (`test_data_mapper.py`)

### Test Cases:
- ✓ Address formatting
- ✓ Price formatting
- ✓ Status mapping
- ✓ Property type mapping
- ✓ Missing field handling
- ✓ Date formatting

```python
class TestResoDataMapper:
    def test_format_address_complete(self):
        """Test formatting complete address"""
        
    def test_format_address_missing_fields(self):
        """Test address formatting with missing components"""
        
    def test_price_formatting(self):
        """Test currency formatting for prices"""
        
    def test_status_mapping(self):
        """Test RESO status to friendly name mapping"""
        
    def test_property_type_mapping(self):
        """Test property type conversions"""
        
    def test_handle_null_values(self):
        """Test handling of null/missing fields"""
```

## 4. Validator Tests (`test_validators.py`)

### Test Cases:
- ✓ Listing ID validation
- ✓ Price validation
- ✓ Property type validation
- ✓ Natural language parsing
- ✓ SQL injection prevention
- ✓ Input sanitization

```python
class TestQueryValidator:
    def test_validate_listing_id_format(self):
        """Test listing ID format validation"""
        
    def test_validate_price_ranges(self):
        """Test price input validation"""
        
    def test_validate_property_types(self):
        """Test property type validation against RESO values"""
        
    def test_sanitize_user_input(self):
        """Test input sanitization for OData queries"""
        
    def test_natural_language_parsing(self):
        """Test parsing of natural language queries"""
```

## 5. MCP Tool Tests

### 5.1 Search Properties Tool (`test_search_properties.py`)

```python
class TestSearchPropertiesTool:
    @pytest.mark.asyncio
    async def test_search_by_city(self):
        """Test property search by city"""
        
    @pytest.mark.asyncio
    async def test_search_by_price_range(self):
        """Test property search with price filters"""
        
    @pytest.mark.asyncio
    async def test_search_with_multiple_criteria(self):
        """Test combining multiple search criteria"""
        
    @pytest.mark.asyncio
    async def test_natural_language_search(self):
        """Test natural language query processing"""
        
    @pytest.mark.asyncio
    async def test_empty_results_handling(self):
        """Test handling when no properties match"""
```

### 5.2 Property Details Tool (`test_property_details.py`)

```python
class TestPropertyDetailsTool:
    @pytest.mark.asyncio
    async def test_get_valid_property(self):
        """Test retrieving existing property details"""
        
    @pytest.mark.asyncio
    async def test_property_not_found(self):
        """Test handling of non-existent property"""
        
    @pytest.mark.asyncio
    async def test_complete_details_mapping(self):
        """Test all fields are properly mapped"""
```

### 5.3 Market Analysis Tool (`test_market_analysis.py`)

```python
class TestMarketAnalysisTool:
    @pytest.mark.asyncio
    async def test_calculate_median_price(self):
        """Test median price calculation"""
        
    @pytest.mark.asyncio
    async def test_calculate_market_trends(self):
        """Test trend analysis calculations"""
        
    @pytest.mark.asyncio
    async def test_timeframe_parsing(self):
        """Test different timeframe options"""
        
    @pytest.mark.asyncio
    async def test_empty_market_data(self):
        """Test handling when no data available"""
```

### 5.4 Find Agent Tool (`test_find_agent.py`)

```python
class TestFindAgentTool:
    @pytest.mark.asyncio
    async def test_search_by_name(self):
        """Test agent search by name"""
        
    @pytest.mark.asyncio
    async def test_search_by_office(self):
        """Test agent search by office"""
        
    @pytest.mark.asyncio
    async def test_format_agent_info(self):
        """Test agent information formatting"""
```

## 6. Integration Tests (`test_integration.py`)

### Test Cases:
- ✓ End-to-end property search flow
- ✓ Authentication to query execution
- ✓ MCP server startup and shutdown
- ✓ Multiple concurrent requests
- ✓ Error propagation through layers

```python
class TestIntegration:
    @pytest.mark.asyncio
    async def test_full_property_search_flow(self):
        """Test complete flow from MCP tool to API response"""
        
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling multiple simultaneous requests"""
        
    @pytest.mark.asyncio
    async def test_server_lifecycle(self):
        """Test MCP server startup, operation, and shutdown"""
```

## 7. Mock Data and Fixtures

### Property Fixture Example:
```json
{
  "ListingId": "TEST123",
  "ListPrice": 450000,
  "BedroomsTotal": 3,
  "BathroomsTotalInteger": 2,
  "LivingArea": 2100,
  "StreetNumber": "123",
  "StreetName": "Main",
  "StreetSuffix": "Street",
  "City": "Austin",
  "StateOrProvince": "TX",
  "PostalCode": "78701",
  "StandardStatus": "Active",
  "PropertyType": "Residential",
  "PropertySubType": "Single Family",
  "ListDate": "2024-01-15",
  "ModificationTimestamp": "2024-01-20T10:30:00Z"
}
```

## 8. Test Configuration (`conftest.py`)

```python
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def mock_reso_client():
    """Mock RESO API client for testing"""
    client = AsyncMock()
    client.query_properties.return_value = []
    return client

@pytest.fixture
def sample_property_data():
    """Load sample property data"""
    with open('tests/fixtures/property_data.json') as f:
        return json.load(f)

@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

## 9. Test Coverage Requirements

### Minimum Coverage Targets:
- Overall: 80%
- Core modules: 90%
- MCP tools: 85%
- Error handling: 100%

### Critical Paths (Must Have 100% Coverage):
1. OAuth2 authentication flow
2. Property search query building
3. Error response handling
4. Data validation and sanitization

## 10. Performance Tests

### Test Cases:
- Response time under 2 seconds
- Handle 100 concurrent requests
- Memory usage stays under 512MB
- Token refresh doesn't block requests

```python
class TestPerformance:
    @pytest.mark.asyncio
    async def test_response_time(self):
        """Test tool response times meet SLA"""
        
    @pytest.mark.asyncio
    async def test_concurrent_load(self):
        """Test server handles concurrent requests"""
        
    def test_memory_usage(self):
        """Test memory consumption stays within limits"""
```

## 11. Error Scenario Tests

### Critical Error Cases:
1. API returns 401 (unauthorized)
2. API returns 429 (rate limited)
3. API returns 500 (server error)
4. Network timeout
5. Invalid JSON response
6. Missing required fields
7. Malformed OAuth token

## 12. Test Execution Strategy

### Local Development:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_reso_client.py

# Run async tests
pytest -m asyncio
```

### CI/CD Pipeline:
```yaml
test:
  script:
    - pytest --cov=src --cov-report=xml
    - coverage report --fail-under=80
```

## Success Criteria

- [ ] All unit tests pass
- [ ] Code coverage > 80%
- [ ] No flaky tests
- [ ] Tests run in < 30 seconds
- [ ] Mock data represents real API responses
- [ ] Error cases are thoroughly tested
- [ ] Performance benchmarks are met