"""Tests for RESO Web API client."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from aioresponses import aioresponses
import aiohttp

from src.reso_client import ResoWebApiClient, ResoApiError
from src.auth.oauth2 import OAuth2Handler, OAuth2Error


class TestResoWebApiClient:
    """Test cases for ResoWebApiClient class."""

    @pytest.fixture
    def mock_oauth_handler(self):
        """Create mock OAuth2 handler."""
        handler = AsyncMock(spec=OAuth2Handler)
        handler.get_valid_token.return_value = "test_token"
        handler.make_authenticated_request = AsyncMock()
        return handler

    @pytest.fixture
    def client(self, mock_oauth_handler):
        """Create RESO client instance for testing."""
        return ResoWebApiClient(
            base_url="https://api.test.com/api/v2",
            mls_id="TEST_MLS",
            oauth_handler=mock_oauth_handler
        )

    @pytest.fixture
    def sample_property_response(self):
        """Sample property response from RESO API."""
        return {
            "value": [
                {
                    "ListingId": "TEST123",
                    "ListingKey": "TEST123",
                    "StandardStatus": "Active",
                    "ListPrice": 450000,
                    "BedroomsTotal": 3,
                    "BathroomsTotalInteger": 2,
                    "LivingArea": 2100,
                    "PropertyType": "Residential",
                    "PropertySubType": "Single Family Residence",
                    "City": "Austin",
                    "StateOrProvince": "TX",
                    "PostalCode": "78701",
                    "ModificationTimestamp": "2024-01-15T10:30:00Z"
                }
            ]
        }

    @pytest.fixture
    def sample_member_response(self):
        """Sample member response from RESO API."""
        return {
            "value": [
                {
                    "MemberKey": "MEMBER123",
                    "MemberMlsId": "MEMBER123",
                    "MemberFirstName": "John",
                    "MemberLastName": "Doe",
                    "MemberEmail": "john.doe@example.com",
                    "MemberOfficeKey": "OFFICE123"
                }
            ]
        }

    def test_initialization(self, client):
        """Test client initialization."""
        assert client.base_url == "https://api.test.com/api/v2"
        assert client.mls_id == "TEST_MLS"
        assert client.odata_endpoint == "https://api.test.com/api/v2/OData/TEST_MLS"
        assert "Property" in client.endpoints
        assert "Member" in client.endpoints
        assert "Office" in client.endpoints
        assert "OpenHouse" in client.endpoints
        assert "Lookup" in client.endpoints

    def test_build_odata_query_basic(self, client):
        """Test basic OData query building."""
        query = client._build_odata_query(
            filter="City eq 'Austin'",
            select=["ListingId", "ListPrice"],
            top=10,
            orderby="ModificationTimestamp desc"
        )
        
        assert "$filter=" in query
        assert "$select=" in query
        assert "$top=10" in query
        assert "$orderby=" in query

    def test_build_odata_query_with_list_select(self, client):
        """Test OData query building with list of select fields."""
        query = client._build_odata_query(
            select=["ListingId", "ListPrice", "City"]
        )
        
        assert "$select=ListingId%2CListPrice%2CCity" in query

    def test_build_property_filter_basic(self, client):
        """Test basic property filter building."""
        filter_str = client._build_property_filter(
            city="Austin",
            min_price=300000,
            max_price=500000,
            min_bedrooms=3
        )
        
        assert "StandardStatus eq 'Active'" in filter_str
        assert "City eq 'Austin'" in filter_str
        assert "ListPrice ge 300000" in filter_str
        assert "ListPrice le 500000" in filter_str
        assert "BedroomsTotal ge 3" in filter_str

    def test_build_property_filter_custom_status(self, client):
        """Test property filter with custom status."""
        filter_str = client._build_property_filter(
            status="Pending"
        )
        
        assert "StandardStatus eq 'Pending'" in filter_str
        assert "StandardStatus eq 'Active'" not in filter_str

    def test_build_property_filter_location(self, client):
        """Test property filter with location parameters."""
        filter_str = client._build_property_filter(
            city="Austin",
            state="TX",
            zip_code="78701"
        )
        
        assert "City eq 'Austin'" in filter_str
        assert "StateOrProvince eq 'TX'" in filter_str
        assert "PostalCode eq '78701'" in filter_str

    def test_build_property_filter_property_types(self, client):
        """Test property filter with property types."""
        filter_str = client._build_property_filter(
            property_type="Residential",
            property_subtype="Single Family Residence"
        )
        
        assert "PropertyType eq 'Residential'" in filter_str
        assert "PropertySubType eq 'Single Family Residence'" in filter_str

    def test_build_property_filter_bathrooms(self, client):
        """Test property filter with bathroom criteria."""
        filter_str = client._build_property_filter(
            min_bathrooms=2.0,
            max_bathrooms=4.5
        )
        
        assert "BathroomsTotalInteger ge 2.0" in filter_str
        assert "BathroomsTotalInteger le 4.5" in filter_str

    def test_build_property_filter_square_footage(self, client):
        """Test property filter with square footage."""
        filter_str = client._build_property_filter(
            min_sqft=1500,
            max_sqft=3000
        )
        
        assert "LivingArea ge 1500" in filter_str
        assert "LivingArea le 3000" in filter_str

    def test_build_property_filter_listing_id(self, client):
        """Test property filter with specific listing ID."""
        filter_str = client._build_property_filter(
            listing_id="TEST123"
        )
        
        assert "ListingId eq 'TEST123'" in filter_str

    def test_build_property_filter_kwargs(self, client):
        """Test property filter with additional kwargs."""
        filter_str = client._build_property_filter(
            PoolFeatures="Private",
            ParkingTotal=2
        )
        
        assert "PoolFeatures eq 'Private'" in filter_str
        assert "ParkingTotal eq 2" in filter_str

    @pytest.mark.asyncio
    async def test_make_request_success(self, client, sample_property_response):
        """Test successful API request."""
        mock_response = AsyncMock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = sample_property_response
        
        client.oauth_handler.make_authenticated_request.return_value = mock_response
        
        mock_session = AsyncMock()
        
        result = await client._make_request(
            mock_session, "GET", "https://api.test.com/Property"
        )
        
        assert result == sample_property_response
        client.oauth_handler.make_authenticated_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_make_request_http_error(self, client):
        """Test API request with HTTP error."""
        from aiohttp import ClientResponseError
        
        client.oauth_handler.make_authenticated_request.side_effect = ClientResponseError(
            request_info=Mock(),
            history=(),
            status=404,
            message="Not Found"
        )
        
        mock_session = AsyncMock()
        
        with pytest.raises(ResoApiError, match="Resource not found"):
            await client._make_request(
                mock_session, "GET", "https://api.test.com/Property"
            )

    @pytest.mark.asyncio
    async def test_make_request_auth_error(self, client):
        """Test API request with authentication error."""
        client.oauth_handler.make_authenticated_request.side_effect = OAuth2Error(
            "Authentication failed"
        )
        
        mock_session = AsyncMock()
        
        with pytest.raises(ResoApiError, match="Authentication failed"):
            await client._make_request(
                mock_session, "GET", "https://api.test.com/Property"
            )

    @pytest.mark.asyncio
    async def test_make_request_unexpected_content_type(self, client):
        """Test API request with unexpected content type."""
        mock_response = AsyncMock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {"content-type": "text/html"}
        mock_response.text.return_value = "<html>Error</html>"
        
        client.oauth_handler.make_authenticated_request.return_value = mock_response
        
        mock_session = AsyncMock()
        
        with pytest.raises(ResoApiError, match="Unexpected content type"):
            await client._make_request(
                mock_session, "GET", "https://api.test.com/Property"
            )

    @pytest.mark.asyncio
    async def test_query_properties_success(self, client, sample_property_response):
        """Test successful property query."""
        with patch.object(client, '_make_request', return_value=sample_property_response):
            results = await client.query_properties(
                filters={"city": "Austin", "min_price": 300000},
                limit=10
            )
            
            assert len(results) == 1
            assert results[0]["ListingId"] == "TEST123"
            assert results[0]["City"] == "Austin"

    @pytest.mark.asyncio
    async def test_query_properties_with_select_fields(self, client, sample_property_response):
        """Test property query with select fields."""
        with patch.object(client, '_make_request', return_value=sample_property_response):
            results = await client.query_properties(
                select_fields=["ListingId", "ListPrice", "City"],
                limit=5
            )
            
            assert len(results) == 1

    @pytest.mark.asyncio
    async def test_query_properties_with_ordering(self, client, sample_property_response):
        """Test property query with custom ordering."""
        with patch.object(client, '_make_request', return_value=sample_property_response):
            results = await client.query_properties(
                order_by="ListPrice desc",
                limit=10
            )
            
            assert len(results) == 1

    @pytest.mark.asyncio
    async def test_query_properties_no_results(self, client):
        """Test property query with no results."""
        with patch.object(client, '_make_request', return_value={"value": []}):
            results = await client.query_properties()
            
            assert len(results) == 0

    @pytest.mark.asyncio
    async def test_query_properties_unexpected_format(self, client):
        """Test property query with unexpected response format."""
        with patch.object(client, '_make_request', return_value={"unexpected": "format"}):
            results = await client.query_properties()
            
            assert len(results) == 0

    @pytest.mark.asyncio
    async def test_get_property_found(self, client, sample_property_response):
        """Test getting specific property that exists."""
        with patch.object(client, 'query_properties', return_value=sample_property_response["value"]):
            result = await client.get_property("TEST123")
            
            assert result is not None
            assert result["ListingId"] == "TEST123"

    @pytest.mark.asyncio
    async def test_get_property_not_found(self, client):
        """Test getting specific property that doesn't exist."""
        with patch.object(client, 'query_properties', return_value=[]):
            result = await client.get_property("NONEXISTENT")
            
            assert result is None

    @pytest.mark.asyncio
    async def test_get_property_api_error(self, client):
        """Test getting property with API error."""
        with patch.object(client, 'query_properties', side_effect=ResoApiError("not found")):
            result = await client.get_property("TEST123")
            
            assert result is None

    @pytest.mark.asyncio
    async def test_get_property_other_error(self, client):
        """Test getting property with non-not-found error."""
        with patch.object(client, 'query_properties', side_effect=ResoApiError("Server error")):
            with pytest.raises(ResoApiError, match="Server error"):
                await client.get_property("TEST123")

    @pytest.mark.asyncio
    async def test_query_members(self, client, sample_member_response):
        """Test querying members."""
        with patch.object(client, '_make_request', return_value=sample_member_response):
            results = await client.query_members(
                filters={"MemberFirstName": "John"},
                limit=10
            )
            
            assert len(results) == 1
            assert results[0]["MemberFirstName"] == "John"

    @pytest.mark.asyncio
    async def test_query_offices(self, client):
        """Test querying offices."""
        office_response = {
            "value": [
                {
                    "OfficeKey": "OFFICE123",
                    "OfficeName": "Test Realty",
                    "OfficeCity": "Austin"
                }
            ]
        }
        
        with patch.object(client, '_make_request', return_value=office_response):
            results = await client.query_offices(
                filters={"OfficeCity": "Austin"},
                limit=10
            )
            
            assert len(results) == 1
            assert results[0]["OfficeName"] == "Test Realty"

    @pytest.mark.asyncio
    async def test_query_open_houses(self, client):
        """Test querying open houses."""
        openhouse_response = {
            "value": [
                {
                    "OpenHouseKey": "OH123",
                    "ListingKey": "TEST123",
                    "OpenHouseDate": "2024-02-15",
                    "OpenHouseStartTime": "14:00:00",
                    "OpenHouseEndTime": "16:00:00"
                }
            ]
        }
        
        with patch.object(client, '_make_request', return_value=openhouse_response):
            results = await client.query_open_houses(
                filters={"ListingKey": "TEST123"},
                limit=10
            )
            
            assert len(results) == 1
            assert results[0]["OpenHouseKey"] == "OH123"

    @pytest.mark.asyncio
    async def test_get_lookup_values_all(self, client):
        """Test getting all lookup values."""
        lookup_response = {
            "value": [
                {"LookupName": "PropertyType", "LookupValue": "Residential"},
                {"LookupName": "PropertyType", "LookupValue": "Commercial"}
            ]
        }
        
        with patch.object(client, '_make_request', return_value=lookup_response):
            result = await client.get_lookup_values()
            
            assert "value" in result
            assert len(result["value"]) == 2

    @pytest.mark.asyncio
    async def test_get_lookup_values_specific(self, client):
        """Test getting specific lookup values."""
        lookup_response = {
            "LookupName": "PropertyType",
            "LookupValues": ["Residential", "Commercial"]
        }
        
        with patch.object(client, '_make_request', return_value=lookup_response):
            result = await client.get_lookup_values("PropertyType")
            
            assert result["LookupName"] == "PropertyType"

    @pytest.mark.asyncio
    async def test_health_check_healthy(self, client, sample_property_response):
        """Test successful health check."""
        client.oauth_handler.get_valid_token.return_value = "test_token"
        
        with patch.object(client, 'query_properties', return_value=sample_property_response["value"]):
            result = await client.health_check()
            
            assert result["status"] == "healthy"
            assert result["authentication"] == "ok"
            assert result["api_access"] == "ok"
            assert result["mls_id"] == "TEST_MLS"
            assert result["sample_records"] == 1

    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self, client):
        """Test failed health check."""
        client.oauth_handler.get_valid_token.side_effect = OAuth2Error("Auth failed")
        
        result = await client.health_check()
        
        assert result["status"] == "unhealthy"
        assert "Auth failed" in result["error"]
        assert result["mls_id"] == "TEST_MLS"

    @pytest.mark.asyncio
    async def test_query_limit_enforcement(self, client, sample_property_response):
        """Test that query limits are enforced."""
        with patch.object(client, '_make_request', return_value=sample_property_response) as mock_request:
            await client.query_properties(limit=500)  # Above API maximum
            
            # Should be limited to 200
            mock_request.assert_called_once()
            call_args = mock_request.call_args[0]
            url = call_args[2]
            assert "$top=200" in url

    @pytest.mark.asyncio
    async def test_default_status_filter(self, client, sample_property_response):
        """Test that default status filter is applied."""
        with patch.object(client, '_make_request', return_value=sample_property_response) as mock_request:
            await client.query_properties()
            
            call_args = mock_request.call_args[0]
            url = call_args[2]
            assert "StandardStatus%20eq%20%27Active%27" in url

    @pytest.mark.asyncio
    async def test_default_ordering(self, client, sample_property_response):
        """Test that default ordering is applied."""
        with patch.object(client, '_make_request', return_value=sample_property_response) as mock_request:
            await client.query_properties()
            
            call_args = mock_request.call_args[0]
            url = call_args[2]
            assert "ModificationTimestamp%20desc" in url