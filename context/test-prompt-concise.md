# Claude Code: Add Unit Tests to ACTRIS MLS MCP Server

I need to add comprehensive unit tests to our ACTRIS MLS MCP Server. The server connects to Bridge Interactive's RESO API for real estate data.

## Quick Setup

Add to `requirements.txt`:
```
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
aioresponses>=0.7.4
```

## Test Structure Needed
```
tests/
├── conftest.py         # Shared fixtures
├── test_validators.py  # Start here - pure functions
├── test_data_mapper.py # Format testing
├── test_oauth2.py      # Auth testing
├── test_reso_client.py # API client tests
└── test_tools.py       # MCP tool tests
```

## Let's Start with Validators

Create `tests/test_validators.py`:

```python
import pytest
from src.utils.validators import QueryValidator

class TestQueryValidator:
    def test_validate_listing_id(self):
        """Test listing ID validation"""
        validator = QueryValidator()
        
        # Valid cases
        assert validator.validate_listing_id("ABC123") is True
        assert validator.validate_listing_id("123-456") is True
        
        # Invalid cases
        assert validator.validate_listing_id("") is False
        assert validator.validate_listing_id("ID WITH SPACES") is False
```

## Key Test Fixtures (conftest.py)

```python
@pytest.fixture
def sample_property():
    """RESO format property data"""
    return {
        "ListingId": "TEST123",
        "ListPrice": 450000,
        "BedroomsTotal": 3,
        "City": "Austin",
        "StateOrProvince": "TX",
        "StandardStatus": "Active"
    }

@pytest.fixture
def mock_oauth_response():
    return {
        "access_token": "test_token",
        "expires_in": 3600
    }
```

## Testing Priorities

1. **Validators** - Input validation and parsing
2. **Data Mapper** - Address formatting, status mapping
3. **OAuth2** - Token management
4. **RESO Client** - API calls and OData queries
5. **MCP Tools** - End-to-end tool testing

## Example Test Patterns

### Testing Async Functions:
```python
@pytest.mark.asyncio
async def test_search_properties():
    result = await search_properties(city="Austin")
    assert result['success'] is True
```

### Mocking API Calls:
```python
from aioresponses import aioresponses

@pytest.mark.asyncio
async def test_api_call():
    with aioresponses() as m:
        m.get('https://api.url/endpoint', payload={"data": "test"})
        result = await make_request()
```

### Testing Error Cases:
```python
def test_handle_missing_fields():
    data = {"City": "Austin"}  # Missing other fields
    result = format_address(data)
    assert result  # Should not crash
```

Let's build the test suite incrementally. Which component should we test first?