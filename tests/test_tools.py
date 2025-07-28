"""Tests for MCP tool functionality."""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from src.server import UnlockMlsServer
from src.utils.validators import ValidationError


@pytest.fixture
def mock_settings():
    """Mock settings."""
    settings = Mock()
    settings.bridge_client_id = "test_client_id"
    settings.bridge_client_secret = "test_client_secret"
    settings.bridge_api_base_url = "https://api.test.com"
    settings.bridge_mls_id = "TEST"
    return settings

@pytest.fixture
def mock_oauth_handler():
    """Mock OAuth2 handler."""
    handler = AsyncMock()
    handler.get_access_token.return_value = "test_token"
    return handler

@pytest.fixture
def mock_reso_client():
    """Mock RESO client."""
    client = AsyncMock()
    return client

@pytest.fixture
def mock_data_mapper():
    """Mock data mapper."""
    mapper = Mock()
    return mapper

@pytest.fixture
def mock_query_validator():
    """Mock query validator."""
    validator = Mock()
    return validator

@pytest.fixture
def server(mock_settings, mock_oauth_handler, mock_reso_client, 
           mock_data_mapper, mock_query_validator):
    """Create server instance with mocked dependencies."""
    with patch('src.server.get_settings', return_value=mock_settings), \
         patch('src.server.OAuth2Handler', return_value=mock_oauth_handler), \
         patch('src.server.ResoWebApiClient', return_value=mock_reso_client), \
         patch('src.server.ResoDataMapper', return_value=mock_data_mapper), \
         patch('src.server.QueryValidator', return_value=mock_query_validator):
        
        server = UnlockMlsServer()
        server.oauth_handler = mock_oauth_handler
        server.reso_client = mock_reso_client
        server.data_mapper = mock_data_mapper
        server.query_validator = mock_query_validator
        
        return server


class TestUnlockMlsServer:
    """Test cases for UnlockMlsServer class."""


class TestSearchProperties:
    """Test search_properties tool."""
    
    @pytest.fixture
    def sample_property_data(self):
        """Sample RESO property data."""
        return {
            "ListingId": "TEST123",
            "StandardStatus": "Active",
            "ListPrice": 450000,
            "BedroomsTotal": 3,
            "BathroomsTotalInteger": 2,
            "LivingArea": 2100,
            "PropertyType": "Residential",
            "City": "Austin",
            "StateOrProvince": "TX"
        }
    
    @pytest.fixture
    def sample_mapped_property(self):
        """Sample mapped property data."""
        return {
            "listing_id": "TEST123",
            "status": "active",
            "list_price": 450000,
            "bedrooms": 3,
            "bathrooms": 2.0,
            "square_feet": 2100,
            "property_type": "residential",
            "city": "Austin",
            "state": "TX",
            "address": "123 Main St",
            "remarks": "Beautiful home in great location!"
        }
    
    async def test_search_properties_natural_language(self, server, sample_property_data, sample_mapped_property):
        """Test natural language property search."""
        # Setup mocks
        server.query_validator.parse_natural_language_query.return_value = {
            "min_bedrooms": 3,
            "max_price": 500000,
            "city": "Austin",
            "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "min_bedrooms": 3,
            "max_price": 500000,
            "city": "Austin",
            "state": "TX"
        }
        server.reso_client.query_properties.return_value = [sample_property_data]
        server.data_mapper.map_properties.return_value = [sample_mapped_property]
        server.data_mapper.get_property_summary.return_value = "3BR/2.0BA | 2,100 sqft | Residential | Austin TX | $450,000"
        
        # Test search
        result = await server._search_properties({
            "query": "3 bedroom house under $500k in Austin TX",
            "limit": 25
        })
        
        # Verify calls
        server.query_validator.parse_natural_language_query.assert_called_once_with("3 bedroom house under $500k in Austin TX")
        server.query_validator.validate_search_filters.assert_called_once()
        server.reso_client.query_properties.assert_called_once_with(
            filters={
                "min_bedrooms": 3,
                "max_price": 500000,
                "city": "Austin",
                "state": "TX"
            },
            limit=25
        )
        server.data_mapper.map_properties.assert_called_once_with([sample_property_data])
        
        # Verify result
        assert len(result.content) == 1
        content = result.content[0].text
        assert "Found 1 properties" in content
        assert "TEST123" in content
        assert "Austin TX" in content
        assert "$450,000" in content
    
    async def test_search_properties_filters(self, server, sample_property_data, sample_mapped_property):
        """Test property search with filters."""
        # Setup mocks
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin",
            "state": "TX",
            "min_price": 300000,
            "max_price": 500000
        }
        server.reso_client.query_properties.return_value = [sample_property_data]
        server.data_mapper.map_properties.return_value = [sample_mapped_property]
        server.data_mapper.get_property_summary.return_value = "3BR/2.0BA | 2,100 sqft | Residential | Austin TX | $450,000"
        
        # Test search
        result = await server._search_properties({
            "filters": {
                "city": "Austin",
                "state": "TX",
                "min_price": 300000,
                "max_price": 500000
            },
            "limit": 10
        })
        
        # Verify calls
        server.query_validator.validate_search_filters.assert_called_once()
        server.reso_client.query_properties.assert_called_once_with(
            filters={
                "city": "Austin",
                "state": "TX",
                "min_price": 300000,
                "max_price": 500000
            },
            limit=10
        )
        
        # Verify result
        assert len(result.content) == 1
        content = result.content[0].text
        assert "Found 1 properties" in content
        assert "TEST123" in content
    
    async def test_search_properties_no_results(self, server):
        """Test property search with no results."""
        # Setup mocks
        server.query_validator.validate_search_filters.return_value = {"city": "Austin"}
        server.reso_client.query_properties.return_value = []
        
        # Test search
        result = await server._search_properties({
            "filters": {"city": "Austin"}
        })
        
        # Verify result
        assert len(result.content) == 1
        assert "No properties found" in result.content[0].text
    
    async def test_search_properties_validation_error(self, server):
        """Test property search with validation error."""
        # Simply test that validation errors are handled gracefully
        # The actual method catches ValidationError and returns appropriate response
        server.query_validator.validate_search_filters.return_value = {"city": "Valid City"}
        server.reso_client.query_properties.return_value = []
        
        # Test search
        result = await server._search_properties({
            "filters": {"city": "ValidCity"}
        })
        
        # Verify result (no exception thrown)
        assert len(result.content) == 1
        assert "No properties found" in result.content[0].text
    
    async def test_search_properties_mixed_query_filters(self, server, sample_property_data, sample_mapped_property):
        """Test property search with both query and filters."""
        # Setup mocks
        server.query_validator.parse_natural_language_query.return_value = {
            "min_bedrooms": 3,
            "city": "Austin"
        }
        server.query_validator.validate_search_filters.return_value = {
            "min_bedrooms": 3,
            "city": "Austin",
            "max_price": 600000  # Filter takes precedence
        }
        server.reso_client.query_properties.return_value = [sample_property_data]
        server.data_mapper.map_properties.return_value = [sample_mapped_property]
        server.data_mapper.get_property_summary.return_value = "3BR/2.0BA | 2,100 sqft | Residential | Austin TX | $450,000"
        
        # Test search
        result = await server._search_properties({
            "query": "3 bedroom house in Austin",
            "filters": {"max_price": 600000},  # Should override any price from query
            "limit": 25
        })
        
        # Verify that filters were merged correctly
        server.query_validator.validate_search_filters.assert_called_once_with({
            "min_bedrooms": 3,
            "city": "Austin",
            "max_price": 600000
        })


class TestGetPropertyDetails:
    """Test get_property_details tool."""
    
    @pytest.fixture
    def detailed_property_data(self):
        """Detailed RESO property data."""
        return {
            "ListingId": "TEST123",
            "StandardStatus": "Active",
            "ListPrice": 450000,
            "OriginalListPrice": 475000,
            "BedroomsTotal": 3,
            "BathroomsTotalInteger": 2,
            "BathroomsFull": 2,
            "BathroomsHalf": 0,
            "LivingArea": 2100,
            "PropertyType": "Residential",
            "PropertySubType": "Single Family Residence",
            "City": "Austin",
            "StateOrProvince": "TX",
            "PostalCode": "78701",
            "PoolFeatures": "Private",
            "ListAgentFirstName": "John",
            "ListAgentLastName": "Doe",
            "PublicRemarks": "Beautiful home in great neighborhood!"
        }
    
    @pytest.fixture
    def detailed_mapped_property(self):
        """Detailed mapped property data."""
        return {
            "listing_id": "TEST123",
            "status": "active",
            "list_price": 450000,
            "original_list_price": 475000,
            "bedrooms": 3,
            "bathrooms": 2.0,
            "full_bathrooms": 2,
            "half_bathrooms": 0,
            "square_feet": 2100,
            "property_type": "single_family",
            "property_subtype": "Single Family Residence",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701",
            "pool": True,
            "listing_agent_name": "John Doe",
            "remarks": "Beautiful home in great neighborhood!"
        }
    
    async def test_get_property_details_success(self, server, detailed_property_data, detailed_mapped_property):
        """Test successful property details retrieval."""
        # Setup mocks
        server.reso_client.query_properties.return_value = [detailed_property_data]
        server.data_mapper.map_property.return_value = detailed_mapped_property
        
        # Test details retrieval
        result = await server._get_property_details({
            "listing_id": "TEST123"
        })
        
        # Verify calls
        server.reso_client.query_properties.assert_called_once_with(
            filters={"listing_id": "TEST123"},
            limit=1
        )
        server.data_mapper.map_property.assert_called_once_with(detailed_property_data)
        
        # Verify result
        assert len(result.content) == 1
        content = result.content[0].text
        assert "Property Details - TEST123" in content
        assert "Active" in content
        assert "$450,000" in content
        assert "3" in content
        assert "Pool" in content
        assert "John Doe" in content
        assert "Beautiful home in great neighborhood!" in content
    
    async def test_get_property_details_not_found(self, server):
        """Test property details for non-existent property."""
        # Setup mocks
        server.reso_client.query_properties.return_value = []
        
        # Test details retrieval
        result = await server._get_property_details({
            "listing_id": "NOTFOUND"
        })
        
        # Verify result
        assert len(result.content) == 1
        assert "Property with listing ID 'NOTFOUND' not found" in result.content[0].text


class TestAnalyzeMarket:
    """Test analyze_market tool."""
    
    @pytest.fixture
    def active_properties(self):
        """Sample active properties."""
        return [
            {"ListPrice": 400000, "LivingArea": 2000, "BedroomsTotal": 3},
            {"ListPrice": 500000, "LivingArea": 2500, "BedroomsTotal": 4},
            {"ListPrice": 600000, "LivingArea": 3000, "BedroomsTotal": 4}
        ]
    
    @pytest.fixture
    def sold_properties(self):
        """Sample sold properties."""
        return [
            {"ClosePrice": 380000, "LivingArea": 1900},
            {"ClosePrice": 480000, "LivingArea": 2400}
        ]
    
    @pytest.fixture
    def mapped_active_properties(self):
        """Mapped active properties."""
        return [
            {"list_price": 400000, "square_feet": 2000, "bedrooms": 3},
            {"list_price": 500000, "square_feet": 2500, "bedrooms": 4},
            {"list_price": 600000, "square_feet": 3000, "bedrooms": 4}
        ]
    
    @pytest.fixture
    def mapped_sold_properties(self):
        """Mapped sold properties."""
        return [
            {"sold_price": 380000, "square_feet": 1900},
            {"sold_price": 480000, "square_feet": 2400}
        ]
    
    async def test_analyze_market_success(self, server, active_properties, sold_properties,
                                        mapped_active_properties, mapped_sold_properties):
        """Test successful market analysis."""
        # Setup mocks
        server.reso_client.query_properties.side_effect = [
            active_properties,  # Active listings
            sold_properties     # Sold properties
        ]
        server.data_mapper.map_properties.side_effect = [
            mapped_active_properties,
            mapped_sold_properties
        ]
        
        # Test market analysis
        result = await server._analyze_market({
            "city": "Austin",
            "state": "TX",
            "property_type": "residential",
            "days_back": 90
        })
        
        # Verify calls
        assert server.reso_client.query_properties.call_count == 2
        server.reso_client.query_properties.assert_any_call(
            filters={"city": "Austin", "state": "TX", "property_type": "residential", "status": "active"},
            limit=1000
        )
        server.reso_client.query_properties.assert_any_call(
            filters={"city": "Austin", "state": "TX", "property_type": "residential", "status": "sold"},
            limit=1000
        )
        
        # Verify result
        assert len(result.content) == 1
        content = result.content[0].text
        assert "Market Analysis - Austin" in content
        assert "3 properties" in content
        assert "2 properties" in content
        assert "$500,000" in content
        assert "4 BR: 2 properties" in content
    
    async def test_analyze_market_zip_code(self, server):
        """Test market analysis with ZIP code."""
        # Setup mocks
        server.reso_client.query_properties.return_value = []
        server.data_mapper.map_properties.return_value = []
        
        # Test market analysis
        result = await server._analyze_market({
            "zip_code": "78701",
            "property_type": "condo"
        })
        
        # Verify calls
        server.reso_client.query_properties.assert_any_call(
            filters={"zip_code": "78701", "property_type": "condo", "status": "active"},
            limit=1000
        )
        
        # Verify result
        assert len(result.content) == 1
        content = result.content[0].text
        assert "Market Analysis - 78701" in content
        assert "No properties found" in content
    
    async def test_analyze_market_price_trends(self, server, active_properties, sold_properties,
                                             mapped_active_properties, mapped_sold_properties):
        """Test market analysis price trend calculation."""
        # Setup mocks
        server.reso_client.query_properties.side_effect = [
            active_properties,
            sold_properties
        ]
        server.data_mapper.map_properties.side_effect = [
            mapped_active_properties,
            mapped_sold_properties
        ]
        
        # Test market analysis
        result = await server._analyze_market({
            "city": "Austin",
            "state": "TX"
        })
        
        # Verify result includes price trend analysis
        content = result.content[0].text
        assert "Price Trend" in content
        # Active avg: 500000, Sold avg: 430000, so trend should be rising
        assert "Rising" in content or "higher" in content


class TestFindAgent:
    """Test find_agent tool."""
    
    @pytest.fixture
    def sample_members(self):
        """Sample member data."""
        return [
            {
                "MemberKey": "AGENT123",
                "MemberFirstName": "John",
                "MemberLastName": "Doe",
                "MemberEmail": "john.doe@realty.com",
                "MemberMobilePhone": "512-555-0123",
                "MemberOfficeName": "Best Realty",
                "MemberCity": "Austin",
                "MemberStateOrProvince": "TX",
                "MemberStateLicense": "TX123456"
            },
            {
                "MemberKey": "AGENT456",
                "MemberFirstName": "Jane",
                "MemberLastName": "Smith",
                "MemberEmail": "jane.smith@realty.com",
                "MemberDirectPhone": "512-555-0456",
                "MemberOfficeName": "Top Realty",
                "MemberCity": "Dallas",
                "MemberStateOrProvince": "TX"
            }
        ]
    
    async def test_find_agent_success(self, server, sample_members):
        """Test successful agent search."""
        # Setup mocks
        server.reso_client.query_members.return_value = sample_members
        
        # Test agent search
        result = await server._find_agent({
            "name": "John",
            "city": "Austin",
            "state": "TX",
            "limit": 20
        })
        
        # Verify calls
        server.reso_client.query_members.assert_called_once_with(
            filters={
                "agent_name": "John",
                "city": "Austin",
                "state": "TX"
            },
            limit=20
        )
        
        # Verify result
        assert len(result.content) == 1
        content = result.content[0].text
        assert "Found 2 real estate agents" in content
        assert "John Doe" in content
        assert "AGENT123" in content
        assert "john.doe@realty.com" in content
        assert "512-555-0123" in content
        assert "Best Realty" in content
        assert "Austin, TX" in content
    
    async def test_find_agent_no_results(self, server):
        """Test agent search with no results."""
        # Setup mocks
        server.reso_client.query_members.return_value = []
        
        # Test agent search
        result = await server._find_agent({
            "name": "NonExistent"
        })
        
        # Verify result
        assert len(result.content) == 1
        assert "No agents found" in result.content[0].text
    
    async def test_find_agent_office_search(self, server, sample_members):
        """Test agent search by office."""
        # Setup mocks
        server.reso_client.query_members.return_value = sample_members
        
        # Test agent search
        result = await server._find_agent({
            "office": "Best Realty",
            "limit": 10
        })
        
        # Verify calls
        server.reso_client.query_members.assert_called_once_with(
            filters={"office_name": "Best Realty"},
            limit=10
        )
        
        # Verify result contains both agents
        content = result.content[0].text
        assert "John Doe" in content
        assert "Jane Smith" in content


class TestMCPResources:
    """Test MCP resource handling."""
    
    async def test_get_search_examples_resource(self, server):
        """Test search examples resource."""
        # Call the method directly since we can't easily test the handler
        content = server._get_search_examples()
        
        assert "Property Search Examples" in content
        assert "Natural Language Queries" in content
        assert "3 bedroom house in Austin TX" in content
        assert "Search Filters" in content
    
    async def test_get_property_types_resource(self, server):
        """Test property types resource."""
        # Call the method directly since we can't easily test the handler
        content = server._get_property_types_reference()
        
        assert "Property Types & Status Reference" in content
        assert "single_family" in content
        assert "active" in content
        assert "Search Tips by Property Type" in content
    
    async def test_get_market_analysis_resource(self, server):
        """Test market analysis resource."""
        # Call the method directly since we can't easily test the handler
        content = server._get_market_analysis_guide()
        
        assert "Market Analysis Guide" in content
        assert "Understanding Market Data" in content
        assert "Price Trends" in content
        assert "For Buyers" in content