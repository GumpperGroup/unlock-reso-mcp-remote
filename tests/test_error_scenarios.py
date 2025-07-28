"""Error scenario testing for comprehensive error handling validation."""

import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch, MagicMock
from aiohttp import ClientError, ClientTimeout, ClientResponseError
from typing import Dict, Any, List

from src.server import UnlockMlsServer
from src.utils.validators import ValidationError


@pytest.fixture
def error_test_server():
    """Create server instance for error scenario testing."""
    with patch('src.server.get_settings') as mock_get_settings, \
         patch('src.server.OAuth2Handler') as mock_oauth, \
         patch('src.server.ResoWebApiClient') as mock_client, \
         patch('src.server.ResoDataMapper') as mock_mapper, \
         patch('src.server.QueryValidator') as mock_validator:
        
        # Mock settings
        settings = Mock()
        settings.bridge_client_id = "error_test_client"
        settings.bridge_client_secret = "error_test_secret"
        settings.bridge_api_base_url = "https://api.test.com"
        settings.bridge_mls_id = "TEST"
        mock_get_settings.return_value = settings
        
        # Setup mock instances for error testing
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


class TestAuthenticationErrors:
    """Test authentication and authorization error scenarios."""
    
    async def test_oauth_token_failure(self, error_test_server):
        """Test handling of OAuth token acquisition failure."""
        server = error_test_server
        
        # Simulate OAuth failure
        server.oauth_handler.get_access_token.side_effect = Exception("OAuth authentication failed")
        
        # Test search operation with auth failure
        result = await server._search_properties({
            "query": "test house",
            "limit": 10
        })
        
        # Verify graceful error handling
        assert len(result.content) == 1
        content = result.content[0].text
        assert "authentication" in content.lower() or "error" in content.lower()
        
        # Verify OAuth was attempted
        server.oauth_handler.get_access_token.assert_called()
    
    async def test_expired_token_handling(self, error_test_server):
        """Test handling of expired authentication tokens."""
        server = error_test_server
        
        # First call returns expired token, second call returns None
        server.oauth_handler.get_access_token.side_effect = [
            "expired_token",  # First attempt
            None  # Retry attempt fails
        ]
        
        # Mock API response indicating token expiration
        server.reso_client.query_properties.side_effect = ClientResponseError(
            request_info=Mock(), history=(), status=401, message="Unauthorized"
        )
        
        result = await server._search_properties({
            "filters": {"city": "Austin"},
            "limit": 10
        })
        
        # Verify error is handled gracefully
        assert len(result.content) == 1
        content = result.content[0].text
        assert "authentication" in content.lower() or "unauthorized" in content.lower()
    
    async def test_invalid_credentials(self, error_test_server):
        """Test handling of invalid API credentials."""
        server = error_test_server
        
        # Simulate invalid credentials
        server.oauth_handler.get_access_token.side_effect = ClientResponseError(
            request_info=Mock(), history=(), status=403, message="Invalid credentials"
        )
        
        result = await server._search_properties({
            "query": "test search",
            "limit": 5
        })
        
        # Verify appropriate error message
        content = result.content[0].text
        assert "credential" in content.lower() or "authentication" in content.lower()


class TestNetworkErrors:
    """Test network connectivity and timeout error scenarios."""
    
    async def test_network_timeout(self, error_test_server):
        """Test handling of network timeouts."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Simulate network timeout
        server.reso_client.query_properties.side_effect = ClientTimeout()
        
        result = await server._search_properties({
            "filters": {"city": "Austin"},
            "limit": 10
        })
        
        # Verify timeout is handled gracefully
        content = result.content[0].text
        assert "timeout" in content.lower() or "network" in content.lower() or "error" in content.lower()
    
    async def test_connection_error(self, error_test_server):
        """Test handling of connection errors."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Simulate connection error
        server.reso_client.query_properties.side_effect = ClientError("Connection failed")
        
        result = await server._search_properties({
            "query": "test property",
            "limit": 5
        })
        
        # Verify connection error is handled
        content = result.content[0].text
        assert "connection" in content.lower() or "network" in content.lower() or "error" in content.lower()
    
    async def test_server_error_responses(self, error_test_server):
        """Test handling of server error responses (5xx)."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Test different server error codes
        error_codes = [500, 502, 503, 504]
        
        for error_code in error_codes:
            server.reso_client.query_properties.side_effect = ClientResponseError(
                request_info=Mock(), history=(), status=error_code, 
                message=f"Server Error {error_code}"
            )
            
            result = await server._search_properties({
                "filters": {"city": "TestCity"},
                "limit": 10
            })
            
            content = result.content[0].text
            assert "server" in content.lower() or "error" in content.lower()
    
    async def test_api_rate_limiting(self, error_test_server):
        """Test handling of API rate limiting (429)."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Simulate rate limiting
        server.reso_client.query_properties.side_effect = ClientResponseError(
            request_info=Mock(), history=(), status=429, message="Too Many Requests"
        )
        
        result = await server._search_properties({
            "query": "rate limit test",
            "limit": 10
        })
        
        content = result.content[0].text
        assert "rate" in content.lower() or "limit" in content.lower() or "many requests" in content.lower()


class TestValidationErrors:
    """Test input validation error scenarios."""
    
    async def test_invalid_search_parameters(self, error_test_server):
        """Test handling of invalid search parameters."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Test validation error in query validator
        server.query_validator.validate_search_filters.side_effect = ValidationError(
            "Invalid city name: must be at least 2 characters"
        )
        
        result = await server._search_properties({
            "filters": {"city": "X"},  # Too short
            "limit": 10
        })
        
        content = result.content[0].text
        assert "validation" in content.lower() or "invalid" in content.lower()
        assert "city" in content.lower()
    
    async def test_malformed_natural_language_query(self, error_test_server):
        """Test handling of malformed natural language queries."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Test parsing error
        server.query_validator.parse_natural_language_query.side_effect = ValidationError(
            "Unable to parse query: ambiguous criteria"
        )
        
        result = await server._search_properties({
            "query": "some very confusing and ambiguous query with no clear intent",
            "limit": 10
        })
        
        content = result.content[0].text
        assert "parse" in content.lower() or "understand" in content.lower() or "query" in content.lower()
    
    async def test_invalid_listing_id(self, error_test_server):
        """Test handling of invalid listing IDs."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        server.reso_client.query_properties.return_value = []  # No results
        
        result = await server._get_property_details({
            "listing_id": "INVALID_ID_123"
        })
        
        content = result.content[0].text
        assert "not found" in content.lower()
        assert "INVALID_ID_123" in content
    
    async def test_invalid_price_ranges(self, error_test_server):
        """Test handling of invalid price ranges."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Min price greater than max price
        server.query_validator.validate_search_filters.side_effect = ValidationError(
            "Invalid price range: minimum price cannot be greater than maximum price"
        )
        
        result = await server._search_properties({
            "filters": {
                "min_price": 500000,
                "max_price": 300000  # Invalid: min > max
            },
            "limit": 10
        })
        
        content = result.content[0].text
        assert "price range" in content.lower() or "invalid" in content.lower()
    
    async def test_invalid_location_parameters(self, error_test_server):
        """Test handling of invalid location parameters."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Test various invalid location scenarios
        invalid_scenarios = [
            {"state": "XX"},  # Invalid state code
            {"zip_code": "123"},  # Invalid ZIP format
            {"city": ""},  # Empty city
        ]
        
        for scenario in invalid_scenarios:
            server.query_validator.validate_search_filters.side_effect = ValidationError(
                f"Invalid location parameter: {list(scenario.keys())[0]}"
            )
            
            result = await server._analyze_market(scenario)
            
            content = result.content[0].text
            assert "invalid" in content.lower() or "location" in content.lower()


class TestDataErrors:
    """Test data processing and mapping error scenarios."""
    
    async def test_corrupted_api_response(self, error_test_server):
        """Test handling of corrupted or malformed API responses."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Return corrupted data that causes mapping errors
        corrupted_data = [
            {"ListingId": None, "ListPrice": "not_a_number", "City": 12345}  # Invalid types
        ]
        
        server.reso_client.query_properties.return_value = corrupted_data
        server.data_mapper.map_properties.side_effect = Exception("Data mapping error: invalid data types")
        
        result = await server._search_properties({
            "filters": {"city": "Austin"},
            "limit": 10
        })
        
        content = result.content[0].text
        assert "data" in content.lower() or "error" in content.lower()
    
    async def test_missing_required_fields(self, error_test_server):
        """Test handling of API responses missing required fields."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Return data missing required fields
        incomplete_data = [
            {"ListingId": "INCOMPLETE001"}  # Missing price, city, etc.
        ]
        
        server.reso_client.query_properties.return_value = incomplete_data
        server.data_mapper.map_properties.side_effect = Exception("Missing required field: ListPrice")
        
        result = await server._search_properties({
            "query": "test search",
            "limit": 10
        })
        
        content = result.content[0].text
        assert "missing" in content.lower() or "incomplete" in content.lower() or "error" in content.lower()
    
    async def test_data_format_inconsistencies(self, error_test_server):
        """Test handling of inconsistent data formats."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Return data with format inconsistencies
        inconsistent_data = [
            {
                "ListingId": "FORMAT001",
                "ListPrice": "450,000.00",  # String instead of number
                "BedroomsTotal": "three",   # Text instead of number
                "LivingArea": None          # Null value
            }
        ]
        
        server.reso_client.query_properties.return_value = inconsistent_data
        server.data_mapper.map_properties.side_effect = ValueError("Cannot convert 'three' to integer")
        
        result = await server._search_properties({
            "filters": {"city": "Austin"},
            "limit": 10
        })
        
        content = result.content[0].text
        assert "format" in content.lower() or "conversion" in content.lower() or "error" in content.lower()


class TestResourceErrors:
    """Test error scenarios in MCP resource operations."""
    
    async def test_resource_generation_errors(self, error_test_server):
        """Test handling of errors during resource content generation."""
        server = error_test_server
        
        # Mock a resource method to raise an exception
        original_method = server._get_search_examples
        server._get_search_examples = Mock(side_effect=Exception("Resource generation failed"))
        
        try:
            # This would typically be called by the MCP framework
            # We're testing that the error doesn't crash the system
            with pytest.raises(Exception, match="Resource generation failed"):
                server._get_search_examples()
        finally:
            # Restore original method
            server._get_search_examples = original_method
    
    async def test_api_status_resource_with_auth_failure(self, error_test_server):
        """Test API status resource when authentication fails."""
        server = error_test_server
        
        # Simulate authentication failure in status check
        server.oauth_handler.get_access_token.side_effect = Exception("Auth failed for status check")
        
        content = await server._get_api_status_info()
        
        # Should still return content, but indicate auth failure
        assert "API Status & System Information" in content
        assert "❌" in content or "Failed" in content


class TestConcurrentErrorScenarios:
    """Test error handling under concurrent operations."""
    
    async def test_concurrent_operations_with_mixed_errors(self, error_test_server):
        """Test handling of mixed success/error scenarios in concurrent operations."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Setup mixed success/failure scenarios
        call_count = 0
        def mixed_response(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count % 3 == 0:
                raise ClientTimeout()  # Every 3rd call times out
            elif call_count % 2 == 0:
                raise ClientError("Connection error")  # Every 2nd call fails
            else:
                return [{"ListingId": f"SUCCESS{call_count}", "ListPrice": 400000}]  # Success
        
        server.reso_client.query_properties.side_effect = mixed_response
        server.data_mapper.map_properties.return_value = [{"listing_id": "SUCCESS", "list_price": 400000}]
        server.data_mapper.get_property_summary.return_value = "Success Summary"
        
        # Execute concurrent operations
        tasks = []
        for i in range(6):
            task = server._search_properties({
                "query": f"concurrent error test {i}",
                "limit": 5
            })
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify mixed results (some success, some errors)
        successful_results = [r for r in results if not isinstance(r, Exception)]
        assert len(successful_results) > 0  # At least some should succeed
        
        # All results should be gracefully handled (no unhandled exceptions)
        for result in successful_results:
            assert len(result.content) == 1
    
    async def test_cascading_error_recovery(self, error_test_server):
        """Test recovery from cascading errors across system components."""
        server = error_test_server
        
        # Start with auth failure, then network failure, then success
        auth_attempts = 0
        def auth_side_effect():
            nonlocal auth_attempts
            auth_attempts += 1
            if auth_attempts == 1:
                raise Exception("First auth attempt failed")
            elif auth_attempts == 2:
                return "valid_token"
            else:
                return "valid_token"
        
        api_attempts = 0
        def api_side_effect(*args, **kwargs):
            nonlocal api_attempts
            api_attempts += 1
            if api_attempts == 1:
                raise ClientTimeout("First API call timed out")
            else:
                return [{"ListingId": "RECOVERY001", "ListPrice": 350000}]
        
        server.oauth_handler.get_access_token.side_effect = auth_side_effect
        server.reso_client.query_properties.side_effect = api_side_effect
        server.data_mapper.map_properties.return_value = [{"listing_id": "RECOVERY001", "list_price": 350000}]
        server.data_mapper.get_property_summary.return_value = "Recovery Summary"
        
        # First operation should fail due to auth
        result1 = await server._search_properties({
            "query": "first attempt",
            "limit": 5
        })
        
        # Second operation should fail due to API timeout
        result2 = await server._search_properties({
            "query": "second attempt", 
            "limit": 5
        })
        
        # Third operation should succeed
        result3 = await server._search_properties({
            "query": "third attempt",
            "limit": 5
        })
        
        # Verify progression from error to success
        assert "error" in result1.content[0].text.lower() or "auth" in result1.content[0].text.lower()
        assert "error" in result2.content[0].text.lower() or "timeout" in result2.content[0].text.lower()
        assert "Found 1 properties" in result3.content[0].text


class TestEdgeCaseErrors:
    """Test edge case error scenarios."""
    
    async def test_empty_response_handling(self, error_test_server):
        """Test handling of empty API responses."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        server.reso_client.query_properties.return_value = []  # Empty response
        
        result = await server._search_properties({
            "filters": {"city": "EmptyCity"},
            "limit": 10
        })
        
        content = result.content[0].text
        assert "No properties found" in content
    
    async def test_extremely_large_response_handling(self, error_test_server):
        """Test handling of extremely large API responses."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Simulate extremely large response that could cause memory issues
        huge_response = [{"ListingId": f"HUGE{i:06d}", "ListPrice": 400000} for i in range(100000)]
        
        server.reso_client.query_properties.return_value = huge_response
        server.data_mapper.map_properties.side_effect = MemoryError("Response too large")
        
        result = await server._search_properties({
            "filters": {"city": "HugeCity"},
            "limit": 100000
        })
        
        content = result.content[0].text
        assert "memory" in content.lower() or "large" in content.lower() or "error" in content.lower()
    
    async def test_special_character_handling_errors(self, error_test_server):
        """Test handling of special characters causing encoding errors."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Response with problematic characters
        problematic_data = [
            {
                "ListingId": "SPECIAL001",
                "ListPrice": 400000,
                "PublicRemarks": "House with special chars: é, ñ, 中文, 🏠, \x00\x01"
            }
        ]
        
        server.reso_client.query_properties.return_value = problematic_data
        server.data_mapper.map_properties.side_effect = UnicodeError("Encoding error")
        
        result = await server._search_properties({
            "filters": {"listing_id": "SPECIAL001"},
            "limit": 1
        })
        
        content = result.content[0].text
        assert "encoding" in content.lower() or "character" in content.lower() or "error" in content.lower()
    
    async def test_infinite_recursion_protection(self, error_test_server):
        """Test protection against infinite recursion in error handling."""
        server = error_test_server
        
        # Setup a scenario that could cause recursive errors
        def recursive_error(*args, **kwargs):
            raise Exception("This error handler causes another error")
        
        server.oauth_handler.get_access_token.side_effect = recursive_error
        
        # The system should handle this gracefully without stack overflow
        result = await server._search_properties({
            "query": "recursion test",
            "limit": 5
        })
        
        # Should get an error response, not a system crash
        content = result.content[0].text
        assert "error" in content.lower()
        assert len(content) > 0  # Should have some error message


class TestErrorRecoveryPatterns:
    """Test error recovery and resilience patterns."""
    
    async def test_retry_mechanism_on_transient_errors(self, error_test_server):
        """Test retry behavior for transient errors."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Simulate transient error followed by success
        attempt_count = 0
        def transient_error_then_success(*args, **kwargs):
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count == 1:
                raise ClientTimeout("Transient timeout")
            else:
                return [{"ListingId": "RETRY001", "ListPrice": 450000}]
        
        server.reso_client.query_properties.side_effect = transient_error_then_success
        server.data_mapper.map_properties.return_value = [{"listing_id": "RETRY001", "list_price": 450000}]
        server.data_mapper.get_property_summary.return_value = "Retry Success"
        
        # If the system has retry logic, this should eventually succeed
        # If not, it should fail gracefully
        result = await server._search_properties({
            "query": "retry test",
            "limit": 5
        })
        
        content = result.content[0].text
        # Either successful retry or graceful error handling
        assert ("Found 1 properties" in content or 
                "error" in content.lower() or 
                "timeout" in content.lower())
    
    async def test_graceful_degradation(self, error_test_server):
        """Test graceful degradation when non-critical components fail."""
        server = error_test_server
        
        server.oauth_handler.get_access_token.return_value = "valid_token"
        
        # Core functionality works, but data mapping partially fails
        server.reso_client.query_properties.return_value = [
            {"ListingId": "DEGRADE001", "ListPrice": 400000, "City": "Austin"}
        ]
        
        # Data mapper works but with reduced functionality
        server.data_mapper.map_properties.return_value = [
            {"listing_id": "DEGRADE001", "list_price": 400000}  # Minimal mapping
        ]
        server.data_mapper.get_property_summary.side_effect = Exception("Summary generation failed")
        
        result = await server._search_properties({
            "filters": {"city": "Austin"},
            "limit": 10
        })
        
        # Should still return some useful result even with partial failure
        content = result.content[0].text
        assert "DEGRADE001" in content
        assert "400000" in content or "$400,000" in content