"""Integration tests for end-to-end MCP server workflows."""

import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch
from typing import Dict, Any, List

from src.server import UnlockMlsServer


@pytest.fixture
def mock_settings():
    """Mock settings for integration tests."""
    settings = Mock()
    settings.bridge_client_id = "test_client_id"
    settings.bridge_client_secret = "test_client_secret"
    settings.bridge_api_base_url = "https://api.test.com"
    settings.bridge_mls_id = "TEST"
    settings.log_level = "INFO"
    settings.api_rate_limit_per_minute = 60
    return settings


@pytest.fixture
def integration_server(mock_settings):
    """Create server instance for integration testing."""
    with patch('src.server.get_settings', return_value=mock_settings), \
         patch('src.server.OAuth2Handler') as mock_oauth, \
         patch('src.server.ResoWebApiClient') as mock_client, \
         patch('src.server.ResoDataMapper') as mock_mapper, \
         patch('src.server.QueryValidator') as mock_validator:
        
        # Setup mock instances
        oauth_handler = AsyncMock()
        reso_client = AsyncMock()
        data_mapper = Mock()
        query_validator = Mock()
        
        mock_oauth.return_value = oauth_handler
        mock_client.return_value = reso_client
        mock_mapper.return_value = data_mapper
        mock_validator.return_value = query_validator
        
        server = UnlockMlsServer()
        server.oauth_handler = oauth_handler
        server.reso_client = reso_client
        server.data_mapper = data_mapper
        server.query_validator = query_validator
        
        return server


@pytest.fixture
def sample_property_data():
    """Sample property data for integration tests."""
    return {
        "ListingId": "INT001",
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
        "UnparsedAddress": "123 Integration Test St",
        "ListAgentFirstName": "John",
        "ListAgentLastName": "Doe",
        "ListOfficeName": "Test Realty",
        "PublicRemarks": "Beautiful home for integration testing"
    }


@pytest.fixture
def sample_mapped_property():
    """Sample mapped property data."""
    return {
        "listing_id": "INT001",
        "status": "active",
        "list_price": 450000,
        "bedrooms": 3,
        "bathrooms": 2.0,
        "square_feet": 2100,
        "property_type": "single_family",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701",
        "address": "123 Integration Test St",
        "listing_agent_name": "John Doe",
        "listing_office": "Test Realty",
        "remarks": "Beautiful home for integration testing"
    }


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""
    
    async def test_complete_property_search_workflow(self, integration_server, 
                                                   sample_property_data, sample_mapped_property):
        """Test complete property search workflow from query to results."""
        server = integration_server
        
        # Setup workflow chain
        server.oauth_handler.get_access_token.return_value = "test_token"
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
        server.data_mapper.get_property_summary.return_value = "3BR/2.0BA | 2,100 sqft | Single Family | Austin TX | $450,000"
        
        # Execute workflow
        result = await server._search_properties({
            "query": "3 bedroom house under $500k in Austin TX",
            "limit": 25
        })
        
        # Verify complete workflow execution
        server.oauth_handler.get_access_token.assert_called_once()
        server.query_validator.parse_natural_language_query.assert_called_once()
        server.query_validator.validate_search_filters.assert_called_once()
        server.reso_client.query_properties.assert_called_once()
        server.data_mapper.map_properties.assert_called_once()
        server.data_mapper.get_property_summary.assert_called_once()
        
        # Verify result quality
        assert len(result.content) == 1
        content = result.content[0].text
        assert "Found 1 properties" in content
        assert "INT001" in content
        assert "$450,000" in content
        assert "Austin TX" in content
    
    async def test_property_details_to_analysis_workflow(self, integration_server,
                                                       sample_property_data, sample_mapped_property):
        """Test workflow from property details to market analysis."""
        server = integration_server
        
        # Step 1: Get property details
        server.oauth_handler.get_access_token.return_value = "test_token"
        server.reso_client.query_properties.return_value = [sample_property_data]
        server.data_mapper.map_property.return_value = sample_mapped_property
        
        details_result = await server._get_property_details({
            "listing_id": "INT001"
        })
        
        # Step 2: Use property location for market analysis
        market_properties = [
            {"ListPrice": 400000, "LivingArea": 2000, "BedroomsTotal": 3},
            {"ListPrice": 500000, "LivingArea": 2500, "BedroomsTotal": 4},
            sample_property_data
        ]
        sold_properties = [
            {"ClosePrice": 380000, "LivingArea": 1900},
            {"ClosePrice": 480000, "LivingArea": 2400}
        ]
        
        server.reso_client.query_properties.side_effect = [
            market_properties,  # Active listings
            sold_properties     # Sold properties
        ]
        server.data_mapper.map_properties.side_effect = [
            [{"list_price": p["ListPrice"], "square_feet": p["LivingArea"], 
              "bedrooms": p["BedroomsTotal"]} for p in market_properties],
            [{"sold_price": p["ClosePrice"], "square_feet": p["LivingArea"]} 
             for p in sold_properties]
        ]
        
        analysis_result = await server._analyze_market({
            "city": "Austin",
            "state": "TX",
            "property_type": "residential",
            "days_back": 90
        })
        
        # Verify workflow connection
        assert "Property Details - INT001" in details_result.content[0].text
        assert "Market Analysis - Austin" in analysis_result.content[0].text
        assert "3 properties" in analysis_result.content[0].text
    
    async def test_agent_search_to_contact_workflow(self, integration_server):
        """Test workflow from agent search to contact information extraction."""
        server = integration_server
        
        sample_agents = [
            {
                "MemberKey": "AGENT001",
                "MemberFirstName": "Jane",
                "MemberLastName": "Smith",
                "MemberEmail": "jane.smith@testrealty.com",
                "MemberMobilePhone": "512-555-0123",
                "MemberOfficeName": "Test Realty",
                "MemberCity": "Austin",
                "MemberStateOrProvince": "TX",
                "MemberStateLicense": "TX123456"
            },
            {
                "MemberKey": "AGENT002", 
                "MemberFirstName": "Bob",
                "MemberLastName": "Johnson",
                "MemberEmail": "bob.johnson@testrealty.com",
                "MemberDirectPhone": "512-555-0456",
                "MemberOfficeName": "Test Realty",
                "MemberCity": "Austin",
                "MemberStateOrProvince": "TX"
            }
        ]
        
        server.oauth_handler.get_access_token.return_value = "test_token"
        server.reso_client.query_members.return_value = sample_agents
        
        # Execute agent search
        result = await server._find_agent({
            "city": "Austin",
            "state": "TX",
            "office": "Test Realty",
            "limit": 20
        })
        
        # Verify comprehensive agent information
        content = result.content[0].text
        assert "Found 2 real estate agents" in content
        assert "Jane Smith" in content
        assert "Bob Johnson" in content
        assert "jane.smith@testrealty.com" in content
        assert "512-555-0123" in content
        assert "Test Realty" in content
        assert "TX123456" in content
    
    async def test_comprehensive_real_estate_research_workflow(self, integration_server,
                                                             sample_property_data, sample_mapped_property):
        """Test comprehensive workflow combining all tools."""
        server = integration_server
        
        # Authentication setup
        server.oauth_handler.get_access_token.return_value = "test_token"
        
        # Phase 1: Market Analysis
        market_data = [
            {"ListPrice": 400000, "LivingArea": 2000, "BedroomsTotal": 3},
            {"ListPrice": 500000, "LivingArea": 2500, "BedroomsTotal": 4},
            {"ListPrice": 600000, "LivingArea": 3000, "BedroomsTotal": 4}
        ]
        sold_data = [
            {"ClosePrice": 380000, "LivingArea": 1900},
            {"ClosePrice": 480000, "LivingArea": 2400}
        ]
        
        server.reso_client.query_properties.side_effect = [
            market_data, sold_data,  # Market analysis calls
            [sample_property_data],  # Property search call
            [sample_property_data]   # Property details call
        ]
        
        mapped_market = [{"list_price": p["ListPrice"], "square_feet": p["LivingArea"], 
                         "bedrooms": p["BedroomsTotal"]} for p in market_data]
        mapped_sold = [{"sold_price": p["ClosePrice"], "square_feet": p["LivingArea"]} 
                       for p in sold_data]
        
        server.data_mapper.map_properties.side_effect = [
            mapped_market, mapped_sold,  # Market analysis mapping
            [sample_mapped_property]     # Property search mapping
        ]
        server.data_mapper.map_property.return_value = sample_mapped_property
        server.data_mapper.get_property_summary.return_value = "3BR/2.0BA | 2,100 sqft | Single Family | Austin TX | $450,000"
        
        # Query validator setup
        server.query_validator.parse_natural_language_query.return_value = {
            "min_bedrooms": 3, "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "min_bedrooms": 3, "city": "Austin", "state": "TX"
        }
        
        # Phase 1: Market Analysis
        market_result = await server._analyze_market({
            "city": "Austin",
            "state": "TX",
            "property_type": "residential"
        })
        
        # Phase 2: Property Search
        search_result = await server._search_properties({
            "query": "3 bedroom house in Austin TX",
            "limit": 25
        })
        
        # Phase 3: Property Details
        details_result = await server._get_property_details({
            "listing_id": "INT001"
        })
        
        # Phase 4: Agent Search
        agent_data = [{
            "MemberKey": "AGENT001",
            "MemberFirstName": "Alice",
            "MemberLastName": "Wilson",
            "MemberEmail": "alice.wilson@testrealty.com",
            "MemberMobilePhone": "512-555-7890",
            "MemberOfficeName": "Premium Realty",
            "MemberCity": "Austin",
            "MemberStateOrProvince": "TX"
        }]
        
        server.reso_client.query_members.return_value = agent_data
        
        agent_result = await server._find_agent({
            "city": "Austin",
            "state": "TX",
            "limit": 10
        })
        
        # Verify comprehensive workflow results
        market_content = market_result.content[0].text
        search_content = search_result.content[0].text
        details_content = details_result.content[0].text
        agent_content = agent_result.content[0].text
        
        assert "Market Analysis - Austin" in market_content
        assert "$500,000" in market_content  # Average price
        assert "Found 1 properties" in search_content
        assert "INT001" in search_content
        assert "Property Details - INT001" in details_content
        assert "Beautiful home for integration testing" in details_content
        assert "Alice Wilson" in agent_content
        assert "Premium Realty" in agent_content
        
        # Verify all major API calls were made
        assert server.reso_client.query_properties.call_count == 4
        assert server.reso_client.query_members.call_count == 1
        assert server.oauth_handler.get_access_token.call_count >= 4


class TestMCPResourceIntegration:
    """Test MCP resource integration and content quality."""
    
    async def test_all_resources_accessible(self, integration_server):
        """Test that all MCP resources are accessible and return content."""
        server = integration_server
        
        # Test all resource methods
        resources_tests = [
            (server._get_search_examples, "Property Search Examples"),
            (server._get_property_types_reference, "Property Types & Status Reference"),
            (server._get_market_analysis_guide, "Market Analysis Guide"),
            (server._get_agent_search_guide, "Agent Search Guide"),
            (server._get_common_workflows, "Common Real Estate Workflows"),
            (server._get_guided_search_prompts, "Guided Property Search Workflows"),
            (server._get_guided_analysis_prompts, "Guided Market Analysis Workflows")
        ]
        
        for resource_method, expected_title in resources_tests:
            content = resource_method()
            assert expected_title in content
            assert len(content) > 1000  # Ensure substantial content
            assert "##" in content  # Ensure proper markdown formatting
    
    async def test_api_status_resource_integration(self, integration_server):
        """Test API status resource with real system information."""
        server = integration_server
        
        # Setup authentication status
        server.oauth_handler.get_access_token.return_value = "test_token_12345"
        
        content = await server._get_api_status_info()
        
        # Verify comprehensive status information
        assert "API Status & System Information" in content
        assert "✅ Connected" in content
        assert "search_properties" in content
        assert "get_property_details" in content
        assert "analyze_market" in content
        assert "find_agent" in content
        
        # Verify resource listing
        assert "Property Search Examples" in content
        assert "Market Analysis Guide" in content
        assert "Agent Search Guide" in content


class TestConcurrentOperations:
    """Test concurrent operations and race conditions."""
    
    async def test_concurrent_property_searches(self, integration_server,
                                              sample_property_data, sample_mapped_property):
        """Test multiple concurrent property searches."""
        server = integration_server
        
        # Setup mocks for concurrent operations
        server.oauth_handler.get_access_token.return_value = "test_token"
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.reso_client.query_properties.return_value = [sample_property_data]
        server.data_mapper.map_properties.return_value = [sample_mapped_property]
        server.data_mapper.get_property_summary.return_value = "Test Summary"
        
        # Execute concurrent searches
        search_tasks = []
        for i in range(5):
            task = server._search_properties({
                "query": f"house in Austin TX search {i}",
                "limit": 10
            })
            search_tasks.append(task)
        
        results = await asyncio.gather(*search_tasks)
        
        # Verify all searches completed successfully
        assert len(results) == 5
        for result in results:
            assert len(result.content) == 1
            assert "Found 1 properties" in result.content[0].text
        
        # Verify reasonable number of API calls (should be optimized)
        assert server.reso_client.query_properties.call_count == 5
    
    async def test_mixed_concurrent_operations(self, integration_server,
                                             sample_property_data, sample_mapped_property):
        """Test concurrent operations of different types."""
        server = integration_server
        
        # Setup comprehensive mocks
        server.oauth_handler.get_access_token.return_value = "test_token"
        
        # Property operations setup
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.reso_client.query_properties.side_effect = [
            [sample_property_data],  # Search
            [sample_property_data],  # Details
            [sample_property_data],  # Market active
            []  # Market sold
        ]
        server.data_mapper.map_properties.side_effect = [
            [sample_mapped_property],  # Search mapping
            [sample_mapped_property],  # Market active mapping
            []  # Market sold mapping
        ]
        server.data_mapper.map_property.return_value = sample_mapped_property
        server.data_mapper.get_property_summary.return_value = "Test Summary"
        
        # Agent operations setup
        agent_data = [{
            "MemberKey": "AGENT001",
            "MemberFirstName": "Test",
            "MemberLastName": "Agent",
            "MemberEmail": "test@agent.com",
            "MemberCity": "Austin",
            "MemberStateOrProvince": "TX"
        }]
        server.reso_client.query_members.return_value = agent_data
        
        # Execute mixed concurrent operations
        tasks = [
            server._search_properties({"query": "house in Austin", "limit": 10}),
            server._get_property_details({"listing_id": "INT001"}),
            server._analyze_market({"city": "Austin", "state": "TX"}),
            server._find_agent({"city": "Austin", "state": "TX", "limit": 10})
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Verify all operations completed successfully
        assert len(results) == 4
        
        search_result, details_result, market_result, agent_result = results
        
        assert "Found 1 properties" in search_result.content[0].text
        assert "Property Details - INT001" in details_result.content[0].text
        assert "Market Analysis - Austin" in market_result.content[0].text
        assert "Test Agent" in agent_result.content[0].text


class TestDataConsistency:
    """Test data consistency across different operations."""
    
    async def test_property_data_consistency(self, integration_server,
                                           sample_property_data, sample_mapped_property):
        """Test that property data remains consistent across search and details."""
        server = integration_server
        
        server.oauth_handler.get_access_token.return_value = "test_token"
        server.query_validator.parse_natural_language_query.return_value = {
            "listing_id": "INT001"
        }
        server.query_validator.validate_search_filters.return_value = {
            "listing_id": "INT001"
        }
        
        # Same property data for both operations
        server.reso_client.query_properties.return_value = [sample_property_data]
        server.data_mapper.map_properties.return_value = [sample_mapped_property]
        server.data_mapper.map_property.return_value = sample_mapped_property
        server.data_mapper.get_property_summary.return_value = "3BR/2.0BA | 2,100 sqft | Single Family | Austin TX | $450,000"
        
        # Execute both operations
        search_result = await server._search_properties({
            "filters": {"listing_id": "INT001"},
            "limit": 1
        })
        
        details_result = await server._get_property_details({
            "listing_id": "INT001"
        })
        
        # Verify consistent data across operations
        search_content = search_result.content[0].text
        details_content = details_result.content[0].text
        
        # Both should contain the same key information
        assert "INT001" in search_content
        assert "INT001" in details_content
        assert "$450,000" in search_content
        assert "$450,000" in details_content
        assert "Austin" in search_content
        assert "Austin" in details_content
    
    async def test_market_analysis_data_integrity(self, integration_server):
        """Test market analysis data integrity and calculations."""
        server = integration_server
        
        server.oauth_handler.get_access_token.return_value = "test_token"
        
        # Controlled market data for predictable analysis
        active_properties = [
            {"ListPrice": 400000, "LivingArea": 2000, "BedroomsTotal": 3},
            {"ListPrice": 500000, "LivingArea": 2500, "BedroomsTotal": 3},
            {"ListPrice": 600000, "LivingArea": 3000, "BedroomsTotal": 4}
        ]
        sold_properties = [
            {"ClosePrice": 380000, "LivingArea": 1900},
            {"ClosePrice": 420000, "LivingArea": 2100}
        ]
        
        server.reso_client.query_properties.side_effect = [active_properties, sold_properties]
        
        mapped_active = [
            {"list_price": 400000, "square_feet": 2000, "bedrooms": 3},
            {"list_price": 500000, "square_feet": 2500, "bedrooms": 3},
            {"list_price": 600000, "square_feet": 3000, "bedrooms": 4}
        ]
        mapped_sold = [
            {"sold_price": 380000, "square_feet": 1900},
            {"sold_price": 420000, "square_feet": 2100}
        ]
        
        server.data_mapper.map_properties.side_effect = [mapped_active, mapped_sold]
        
        result = await server._analyze_market({
            "city": "Austin",
            "state": "TX",
            "property_type": "residential"
        })
        
        content = result.content[0].text
        
        # Verify calculated statistics are present and reasonable
        assert "3 properties" in content  # Active count
        assert "2 properties" in content  # Sold count
        assert "$500,000" in content  # Average should be 500k for active
        assert "3 BR: 2 properties" in content  # Bedroom distribution
        assert "4 BR: 1 properties" in content
        
        # Verify price trend calculation (500k active avg vs 400k sold avg = rising)
        assert ("Rising" in content or "higher" in content.lower() or 
                "increase" in content.lower())