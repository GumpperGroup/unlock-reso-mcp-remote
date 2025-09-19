"""Tests for OAuth2 authentication handler."""

import asyncio
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from aioresponses import aioresponses
import aiohttp

from src.auth.oauth2 import OAuth2Handler, OAuth2Error


class TestOAuth2Handler:
    """Test cases for OAuth2Handler class."""

    @pytest.fixture
    def oauth_handler(self):
        """Create OAuth2Handler instance for testing."""
        return OAuth2Handler(
            client_id="test_client_id",
            client_secret="test_client_secret",
            token_endpoint="https://api.test.com/oauth2/token"
        )

    @pytest.fixture
    def mock_token_response(self):
        """Mock OAuth2 token response."""
        return {
            "access_token": "test_access_token_12345",
            "token_type": "Bearer",
            "expires_in": 3600
        }

    def test_initialization(self, oauth_handler):
        """Test OAuth2Handler initialization."""
        assert oauth_handler.client_id == "test_client_id"
        assert oauth_handler.client_secret == "test_client_secret"
        assert oauth_handler.token_endpoint == "https://api.test.com/oauth2/token"
        assert oauth_handler._access_token is None
        assert oauth_handler._expires_at is None
        assert not oauth_handler.is_token_valid

    def test_is_token_valid_no_token(self, oauth_handler):
        """Test is_token_valid when no token is set."""
        assert not oauth_handler.is_token_valid

    def test_is_token_valid_expired_token(self, oauth_handler):
        """Test is_token_valid with expired token."""
        oauth_handler._access_token = "test_token"
        oauth_handler._expires_at = datetime.utcnow() - timedelta(hours=1)
        assert not oauth_handler.is_token_valid

    def test_is_token_valid_valid_token(self, oauth_handler):
        """Test is_token_valid with valid token."""
        oauth_handler._access_token = "test_token"
        oauth_handler._expires_at = datetime.utcnow() + timedelta(hours=1)
        assert oauth_handler.is_token_valid

    def test_authorization_header_no_token(self, oauth_handler):
        """Test authorization_header when no token is available."""
        with pytest.raises(OAuth2Error, match="No access token available"):
            oauth_handler.authorization_header

    def test_authorization_header_with_token(self, oauth_handler):
        """Test authorization_header with valid token."""
        oauth_handler._access_token = "test_token"
        oauth_handler._token_type = "Bearer"
        
        header = oauth_handler.authorization_header
        assert header == {"Authorization": "Bearer test_token"}

    @pytest.mark.asyncio
    async def test_authenticate_success(self, oauth_handler, mock_token_response):
        """Test successful authentication."""
        with aioresponses() as m:
            m.post(
                "https://api.test.com/oauth2/token",
                payload=mock_token_response,
                status=200
            )
            
            token = await oauth_handler.authenticate()
            
            assert token == "test_access_token_12345"
            assert oauth_handler._access_token == "test_access_token_12345"
            assert oauth_handler._token_type == "Bearer"
            assert oauth_handler.is_token_valid

    @pytest.mark.asyncio
    async def test_authenticate_invalid_credentials(self, oauth_handler):
        """Test authentication with invalid credentials."""
        with aioresponses() as m:
            m.post(
                "https://api.test.com/oauth2/token",
                status=401,
                payload={"error": "invalid_client"}
            )
            
            with pytest.raises(OAuth2Error, match="Invalid client credentials"):
                await oauth_handler.authenticate()

    @pytest.mark.asyncio
    async def test_authenticate_rate_limited(self, oauth_handler, mock_token_response):
        """Test authentication with rate limiting."""
        with aioresponses() as m:
            # First request returns 429, second succeeds
            m.post(
                "https://api.test.com/oauth2/token",
                status=429,
                payload={"error": "rate_limit_exceeded"}
            )
            m.post(
                "https://api.test.com/oauth2/token",
                payload=mock_token_response,
                status=200
            )
            
            # Mock sleep to speed up test
            with patch('asyncio.sleep', new_callable=AsyncMock):
                token = await oauth_handler.authenticate()
            
            assert token == "test_access_token_12345"

    @pytest.mark.asyncio
    async def test_authenticate_network_error(self, oauth_handler):
        """Test authentication with network error."""
        with aioresponses() as m:
            m.post(
                "https://api.test.com/oauth2/token",
                exception=aiohttp.ClientConnectorError(
                    connection_key=Mock(),
                    os_error=Mock()
                )
            )
            
            with patch('asyncio.sleep', new_callable=AsyncMock):
                with pytest.raises(OAuth2Error, match="Failed to authenticate"):
                    await oauth_handler.authenticate()

    @pytest.mark.asyncio
    async def test_authenticate_max_retries_exceeded(self, oauth_handler):
        """Test authentication when max retries are exceeded."""
        # Set lower max_retries for faster test
        oauth_handler.max_retries = 2
        
        with aioresponses() as m:
            # All requests fail
            m.post(
                "https://api.test.com/oauth2/token",
                status=500,
                payload={"error": "internal_server_error"}
            )
            
            with patch('asyncio.sleep', new_callable=AsyncMock):
                with pytest.raises(OAuth2Error, match="Failed to authenticate after 2 attempts"):
                    await oauth_handler.authenticate()

    @pytest.mark.asyncio
    async def test_refresh_token(self, oauth_handler, mock_token_response):
        """Test token refresh."""
        with aioresponses() as m:
            m.post(
                "https://api.test.com/oauth2/token",
                payload=mock_token_response,
                status=200
            )
            
            token = await oauth_handler.refresh_token()
            assert token == "test_access_token_12345"

    @pytest.mark.asyncio
    async def test_get_valid_token_existing_valid(self, oauth_handler):
        """Test get_valid_token with existing valid token."""
        oauth_handler._access_token = "existing_token"
        oauth_handler._expires_at = datetime.utcnow() + timedelta(hours=1)
        
        token = await oauth_handler.get_valid_token()
        assert token == "existing_token"

    @pytest.mark.asyncio
    async def test_get_valid_token_refresh_needed(self, oauth_handler, mock_token_response):
        """Test get_valid_token when refresh is needed."""
        oauth_handler._access_token = "expired_token"
        oauth_handler._expires_at = datetime.utcnow() - timedelta(hours=1)
        
        with aioresponses() as m:
            m.post(
                "https://api.test.com/oauth2/token",
                payload=mock_token_response,
                status=200
            )
            
            token = await oauth_handler.get_valid_token()
            assert token == "test_access_token_12345"

    def test_clear_token(self, oauth_handler):
        """Test clearing stored token."""
        oauth_handler._access_token = "test_token"
        oauth_handler._expires_at = datetime.utcnow() + timedelta(hours=1)
        
        oauth_handler.clear_token()
        
        assert oauth_handler._access_token is None
        assert oauth_handler._expires_at is None
        assert not oauth_handler.is_token_valid

    @pytest.mark.asyncio
    async def test_make_authenticated_request_success(self, oauth_handler):
        """Test successful authenticated request."""
        oauth_handler._access_token = "test_token"
        oauth_handler._expires_at = datetime.utcnow() + timedelta(hours=1)
        
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_session.request.return_value = mock_response
        
        response = await oauth_handler.make_authenticated_request(
            mock_session, "GET", "https://api.test.com/data"
        )
        
        assert response == mock_response
        mock_session.request.assert_called_once()
        
        # Check that authorization header was added
        call_args = mock_session.request.call_args
        headers = call_args[1]["headers"]
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test_token"

    @pytest.mark.asyncio
    async def test_make_authenticated_request_401_retry(self, oauth_handler, mock_token_response):
        """Test authenticated request with 401 response and retry."""
        oauth_handler._access_token = "old_token"
        oauth_handler._expires_at = datetime.utcnow() + timedelta(hours=1)
        
        mock_session = AsyncMock()
        
        # First response returns 401, second succeeds
        first_response = AsyncMock()
        first_response.status = 401
        
        second_response = AsyncMock()
        second_response.status = 200
        
        mock_session.request.side_effect = [first_response, second_response]
        
        # Mock the token refresh
        with aioresponses() as m:
            m.post(
                oauth_handler.token_endpoint,
                payload=mock_token_response,
                status=200
            )
            
            response = await oauth_handler.make_authenticated_request(
                mock_session, "GET", "https://api.test.com/data"
            )
        
        assert response == second_response
        assert mock_session.request.call_count == 2
        first_response.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_concurrent_authentication(self, oauth_handler, mock_token_response):
        """Test concurrent authentication requests use same token."""
        with aioresponses() as m:
            m.post(
                "https://api.test.com/oauth2/token",
                payload=mock_token_response,
                status=200
            )
            
            # Start multiple concurrent authentication requests
            tasks = [
                oauth_handler.authenticate(),
                oauth_handler.authenticate(),
                oauth_handler.authenticate()
            ]
            
            tokens = await asyncio.gather(*tasks)
            
            # All should return the same token
            assert all(token == "test_access_token_12345" for token in tokens)
            
            # Should only make one actual HTTP request due to locking
            assert len(m.requests) == 1

    @pytest.mark.asyncio
    async def test_token_expiration_buffer(self, oauth_handler):
        """Test that token is considered invalid 30 seconds before expiration."""
        oauth_handler._access_token = "test_token"
        # Set expiration to 20 seconds from now (less than 30 second buffer)
        oauth_handler._expires_at = datetime.utcnow() + timedelta(seconds=20)
        
        assert not oauth_handler.is_token_valid