# Claude Code: Implement Unit Tests for ACTRIS MLS MCP Server

I need you to help me create a comprehensive test suite for the ACTRIS MLS MCP Server we're building. The server connects to Bridge Interactive's RESO Web API and provides MCP tools for property search, market analysis, and agent lookup.

## Current Project Structure

```
actris-mls-mcp-server/
├── src/
│   ├── server.py          # MCP server with tools
│   ├── reso_client.py     # RESO API client
│   ├── auth/
│   │   └── oauth2.py      # OAuth2 authentication
│   └── utils/
│       ├── data_mapper.py # Data formatting
│       └── validators.py  # Input validation
└── requirements.txt
```

## Test Framework Setup

First, let's set up the testing framework:

```bash
# Add to requirements.txt:
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
aioresponses>=0.7.4  # For mocking aiohttp
freezegun>=1.2.0     # For datetime mocking
```

## Test Structure to Create

```
tests/
├── __init__.py
├── conftest.py            # Shared fixtures
├── test_oauth2.py         # Auth tests
├── test_reso_client.py    # API client tests
├── test_data_mapper.py    # Data formatting tests
├── test_validators.py     # Validation tests
├── test_tools.py          # MCP tool tests
└── fixtures/
    ├── property_response.json
    └── market_data.json
```

## Phase 1: Test Configuration & Fixtures

### Create `tests/conftest.py`:

```python
import pytest
import json
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, Mock

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_oauth_response():
    """Mock OAuth2 token response"""
    return {
        "access_token": "test_token_123",
        "token_type": "Bearer",
        "expires_in": 3600
    }

@pytest.fixture
def sample_property():
    """Sample property data matching RESO format"""
    return {
        "ListingId": "TEST123",
        "ListingKey": "TEST123",
        "ListPrice": 450000,
        "StandardStatus": "Active",
        "BedroomsTotal": 3,
        "BathroomsTotalInteger": 2,
        "LivingArea": 2100,
        "StreetNumber": "123",
        "StreetDirPrefix": "",
        "StreetName": "Main",
        "StreetSuffix": "Street",
        "City": "Austin",
        "StateOrProvince": "TX",
        "PostalCode": "78701",
        "PropertyType": "Residential",
        "PropertySubType": "Single Family Residence"
    }

@pytest.fixture
def mock_reso_client():
    """Mock RESO client for testing tools"""
    client = AsyncMock()
    client.query_properties = AsyncMock(return_value=[])
    client.get_property = AsyncMock(return_value=None)
    return client
```

## Phase 2: OAuth2 Authentication Tests

### Create `tests/test_oauth2.py`:

```python
import pytest
from datetime import datetime, timedelta
from aioresponses import aioresponses
from src.auth.oauth2 import OAuth2Handler

class TestOAuth2Authentication:
    @pytest.mark.asyncio
    async def test_successful_authentication(self, mock_oauth_response):
        """Test successful OAuth2 token retrieval"""
        # Mock the token endpoint
        # Test token is stored correctly
        # Verify expiration time is calculated
        
    @pytest.mark.asyncio
    async def test_token_refresh_when_expired(self):
        """Test automatic token refresh on expiry"""
        # Set expired token
        # Make request
        # Verify new token is fetched
        
    @pytest.mark.asyncio
    async def test_handle_authentication_error(self):
        """Test handling of 401 responses"""
        # Mock failed auth response
        # Verify error is raised appropriately
```

## Phase 3: RESO Client Tests

### Create `tests/test_reso_client.py`:

```python
import pytest
from aioresponses import aioresponses
from src.reso_client import ResoWebApiClient

class TestResoWebApiClient:
    @pytest.mark.asyncio
    async def test_build_odata_filter(self):
        """Test OData query string building"""
        client = ResoWebApiClient("", "", "", "")
        
        # Test cases for filter building
        filters = client._build_property_query(
            city="Austin",
            min_price=300000,
            max_price=500000,
            bedrooms=3
        )
        
        expected = "$filter=City eq 'Austin' and ListPrice ge 300000 and ListPrice le 500000 and BedroomsTotal ge 3"
        assert filters['$filter'] == expected
    
    @pytest.mark.asyncio
    async def test_query_properties_success(self, sample_property):
        """Test successful property query"""
        with aioresponses() as m:
            # Mock the API response
            m.get(
                "https://api.bridgedataoutput.com/api/v2/OData/actris/Property",
                payload={"value": [sample_property]}
            )
            
            # Test the query
            client = ResoWebApiClient(...)
            results = await client.query_properties({})
            
            assert len(results) == 1
            assert results[0]['ListingId'] == 'TEST123'
```

## Phase 4: Data Mapper Tests

### Create `tests/test_data_mapper.py`:

```python
import pytest
from src.utils.data_mapper import ResoDataMapper

class TestResoDataMapper:
    def test_format_complete_address(self, sample_property):
        """Test formatting address with all components"""
        mapper = ResoDataMapper()
        address = mapper._format_address(sample_property)
        
        assert address == "123 Main Street, Austin, TX 78701"
    
    def test_format_address_missing_components(self):
        """Test address formatting with missing fields"""
        mapper = ResoDataMapper()
        partial_data = {
            "StreetName": "Main",
            "City": "Austin",
            "StateOrProvince": "TX"
        }
        
        address = mapper._format_address(partial_data)
        assert address == "Main, Austin, TX"
    
    def test_map_property_status(self):
        """Test RESO status to friendly name mapping"""
        mapper = ResoDataMapper()
        
        test_cases = [
            ("Active", "Active"),
            ("Pending", "Under Contract"),
            ("Closed", "Sold"),
            ("ComingSoon", "Coming Soon")
        ]
        
        for reso_status, expected in test_cases:
            assert mapper._map_status(reso_status) == expected
    
    def test_format_price(self):
        """Test price formatting"""
        mapper = ResoDataMapper()
        
        # Test various price formats
        assert mapper._format_price(450000) == "$450,000"
        assert mapper._format_price(1250000) == "$1,250,000"
        assert mapper._format_price(0) == "$0"
```

## Phase 5: Validator Tests

### Create `tests/test_validators.py`:

```python
import pytest
from src.utils.validators import QueryValidator

class TestQueryValidator:
    def test_validate_listing_id(self):
        """Test listing ID validation"""
        validator = QueryValidator()
        
        # Valid IDs
        assert validator.validate_listing_id("ABC123")
        assert validator.validate_listing_id("123-456")
        assert validator.validate_listing_id("TEST_ID_789")
        
        # Invalid IDs
        assert not validator.validate_listing_id("")
        assert not validator.validate_listing_id("ID WITH SPACES")
        assert not validator.validate_listing_id("ID#WITH#SPECIAL")
    
    def test_parse_natural_language(self):
        """Test natural language query parsing"""
        validator = QueryValidator()
        
        query = "3 bedroom homes in Austin under 500k"
        params = validator.parse_natural_language(query)
        
        assert params['bedrooms'] == 3
        assert params['city'] == "Austin"
        assert params['max_price'] == 500000
    
    def test_sanitize_input(self):
        """Test input sanitization for OData"""
        validator = QueryValidator()
        
        # Test SQL injection prevention
        malicious = "Austin'; DROP TABLE Properties; --"
        sanitized = validator.sanitize_string(malicious)
        assert "DROP" not in sanitized
        
        # Test quote escaping
        assert validator.sanitize_string("O'Brien") == "O''Brien"
```

## Phase 6: MCP Tool Tests

### Create `tests/test_tools.py`:

```python
import pytest
from unittest.mock import patch, AsyncMock
from src.server import ActrisMlsMcpServer

class TestMCPTools:
    @pytest.mark.asyncio
    async def test_search_properties_tool(self, mock_reso_client, sample_property):
        """Test property search tool"""
        server = ActrisMlsMcpServer()
        server.reso_client = mock_reso_client
        
        # Mock the API response
        mock_reso_client.query_properties.return_value = [sample_property]
        
        # Test the tool
        result = await server.search_properties(
            city="Austin",
            min_price=400000,
            bedrooms=3
        )
        
        assert result['success'] is True
        assert result['count'] == 1
        assert result['properties'][0]['address'] == "123 Main Street, Austin, TX 78701"
    
    @pytest.mark.asyncio
    async def test_search_properties_natural_language(self):
        """Test natural language property search"""
        server = ActrisMlsMcpServer()
        
        result = await server.search_properties(
            query="Find 3 bedroom homes in Austin under 500000"
        )
        
        # Verify query was parsed correctly
        # Check that appropriate filters were applied
    
    @pytest.mark.asyncio
    async def test_property_details_not_found(self, mock_reso_client):
        """Test property details when listing not found"""
        server = ActrisMlsMcpServer()
        server.reso_client = mock_reso_client
        
        mock_reso_client.get_property.return_value = None
        
        result = await server.get_property_details("INVALID123")
        
        assert result['success'] is False
        assert 'not found' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_market_analysis_calculations(self):
        """Test market analysis statistics"""
        server = ActrisMlsMcpServer()
        
        # Mock market data
        market_data = [
            {"ListPrice": 400000, "ClosePrice": 395000},
            {"ListPrice": 450000, "ClosePrice": 445000},
            {"ListPrice": 500000, "ClosePrice": 490000}
        ]
        
        stats = server._calculate_market_analytics(market_data)
        
        assert stats['median_price'] == 445000
        assert stats['average_price'] == 443333.33
        assert stats['total_listings'] == 3
```

## Phase 7: Integration Tests

### Create `tests/test_integration.py`:

```python
import pytest
from src.server import ActrisMlsMcpServer

class TestIntegration:
    @pytest.mark.asyncio
    async def test_end_to_end_property_search(self):
        """Test complete flow from tool call to formatted response"""
        server = ActrisMlsMcpServer()
        await server.initialize()
        
        # Perform actual search (with mocked API)
        result = await server.search_properties(
            city="Austin",
            min_price=300000,
            max_price=500000,
            bedrooms=3
        )
        
        # Verify complete data flow
        assert 'properties' in result
        for prop in result['properties']:
            assert 'address' in prop
            assert 'price' in prop
            assert '$' in prop['price']  # Formatted as currency
```

## Phase 8: Performance and Error Tests

### Add to test files:

```python
@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test handling multiple simultaneous requests"""
    server = ActrisMlsMcpServer()
    
    # Create 10 concurrent requests
    tasks = [
        server.search_properties(city="Austin")
        for _ in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    assert all(r['success'] for r in results)

@pytest.mark.asyncio
async def test_api_timeout_handling():
    """Test timeout handling"""
    with aioresponses() as m:
        # Simulate timeout
        m.get(
            "https://api.bridgedataoutput.com/api/v2/OData/actris/Property",
            exception=asyncio.TimeoutError()
        )
        
        result = await server.search_properties()
        assert result['success'] is False
        assert 'timeout' in result['error'].lower()
```

## Test Execution Commands

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run only async tests
pytest -m asyncio

# Run specific test file
pytest tests/test_reso_client.py -v

# Run tests matching pattern
pytest -k "test_search" -v

# Run with stdout capture disabled (for debugging)
pytest -s
```

## Implementation Priority

Let's implement the tests in this order:

1. **Start with validators** - They're pure functions, easiest to test
2. **Then data mapper** - Also mostly pure functions
3. **OAuth2 tests** - Critical for authentication
4. **RESO client tests** - Core functionality
5. **MCP tool tests** - Integration of all components
6. **Full integration tests** - End-to-end validation

## Key Testing Patterns

1. **Use fixtures for reusable test data**
2. **Mock external API calls with aioresponses**
3. **Test both success and failure paths**
4. **Verify error messages are user-friendly**
5. **Test edge cases (empty results, missing fields)**
6. **Use parametrize for multiple test cases**

Ready to start implementing these tests? Let's begin with the test configuration and work through each module systematically!