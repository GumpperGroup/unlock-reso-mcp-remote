"""OAuth2 authentication handler for Bridge Interactive RESO API."""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

import aiohttp
from aiohttp import ClientError, ClientResponseError

from ..config.settings import settings
from ..config.logging_config import setup_logging

logger = setup_logging(__name__)


class OAuth2Error(Exception):
    """Base exception for OAuth2 related errors."""
    pass


class OAuth2Handler:
    """Handles OAuth2 authentication using client credentials flow."""
    
    def __init__(self, 
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 token_endpoint: Optional[str] = None):
        """
        Initialize OAuth2 handler.
        
        Args:
            client_id: OAuth2 client ID (defaults to settings)
            client_secret: OAuth2 client secret (defaults to settings)
            token_endpoint: Token endpoint URL (defaults to settings)
        """
        self.client_id = client_id or settings.bridge_client_id
        self.client_secret = client_secret or settings.bridge_client_secret
        self.token_endpoint = token_endpoint or settings.token_endpoint
        
        # Token storage
        self._access_token: Optional[str] = None
        self._token_type: str = "Bearer"
        self._expires_at: Optional[datetime] = None
        
        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 1.0  # seconds
        
        # Lock for thread-safe token refresh
        self._token_lock = asyncio.Lock()
        
        logger.info("OAuth2Handler initialized for endpoint: %s", self.token_endpoint)
    
    @property
    def is_token_valid(self) -> bool:
        """Check if the current token is valid and not expired."""
        if not self._access_token or not self._expires_at:
            return False
        
        # Add 30 second buffer before expiration
        buffer = timedelta(seconds=30)
        return datetime.utcnow() < (self._expires_at - buffer)
    
    @property
    def authorization_header(self) -> Dict[str, str]:
        """Get the authorization header for API requests."""
        if not self._access_token:
            raise OAuth2Error("No access token available. Call authenticate() first.")
        
        return {"Authorization": f"{self._token_type} {self._access_token}"}
    
    async def authenticate(self) -> str:
        """
        Authenticate and get access token using client credentials flow.
        
        Returns:
            Access token string
            
        Raises:
            OAuth2Error: If authentication fails
        """
        async with self._token_lock:
            # Check if current token is still valid
            if self.is_token_valid:
                logger.debug("Using existing valid token")
                return self._access_token
            
            logger.info("Requesting new access token")
            
            # Prepare request data
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }
            
            # Attempt authentication with retries
            last_error = None
            for attempt in range(self.max_retries):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            self.token_endpoint,
                            data=data,
                            headers=headers,
                            timeout=aiohttp.ClientTimeout(total=30)
                        ) as response:
                            response.raise_for_status()
                            token_data = await response.json()
                            
                            # Store token information
                            self._access_token = token_data["access_token"]
                            self._token_type = token_data.get("token_type", "Bearer")
                            
                            # Calculate expiration time
                            expires_in = token_data.get("expires_in", 3600)  # Default 1 hour
                            self._expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                            
                            logger.info("Successfully obtained access token (expires in %d seconds)", expires_in)
                            return self._access_token
                            
                except ClientResponseError as e:
                    last_error = e
                    if e.status == 401:
                        logger.error("Authentication failed: Invalid client credentials")
                        raise OAuth2Error("Invalid client credentials") from e
                    elif e.status == 429:
                        # Rate limited - wait longer
                        wait_time = self.retry_delay * (2 ** attempt)
                        logger.warning("Rate limited. Waiting %f seconds before retry", wait_time)
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error("HTTP error during authentication: %s", str(e))
                        
                except ClientError as e:
                    last_error = e
                    logger.error("Network error during authentication: %s", str(e))
                    
                except Exception as e:
                    last_error = e
                    logger.error("Unexpected error during authentication: %s", str(e))
                
                # Wait before retry (except for last attempt)
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (attempt + 1)
                    logger.info("Retrying authentication in %f seconds (attempt %d/%d)", 
                               wait_time, attempt + 2, self.max_retries)
                    await asyncio.sleep(wait_time)
            
            # All retries failed
            error_msg = f"Failed to authenticate after {self.max_retries} attempts"
            if last_error:
                error_msg += f": {str(last_error)}"
            
            logger.error(error_msg)
            raise OAuth2Error(error_msg) from last_error
    
    async def refresh_token(self) -> str:
        """
        Refresh the access token.
        
        For client credentials flow, this is the same as authenticate().
        
        Returns:
            New access token
        """
        logger.info("Refreshing access token")
        return await self.authenticate()
    
    async def get_valid_token(self) -> str:
        """
        Get a valid access token, refreshing if necessary.
        
        Returns:
            Valid access token
            
        Raises:
            OAuth2Error: If unable to get valid token
        """
        if self.is_token_valid:
            return self._access_token
        
        return await self.authenticate()
    
    def clear_token(self) -> None:
        """Clear the stored access token."""
        self._access_token = None
        self._expires_at = None
        logger.info("Access token cleared")
    
    async def make_authenticated_request(self,
                                       session: aiohttp.ClientSession,
                                       method: str,
                                       url: str,
                                       **kwargs) -> aiohttp.ClientResponse:
        """
        Make an authenticated HTTP request with automatic token refresh.
        
        Args:
            session: aiohttp client session
            method: HTTP method
            url: Request URL
            **kwargs: Additional arguments for the request
            
        Returns:
            Client response
            
        Raises:
            OAuth2Error: If authentication fails
            ClientError: If request fails
        """
        # Ensure we have a valid token
        await self.get_valid_token()
        
        # Add authorization header
        headers = kwargs.get("headers", {})
        headers.update(self.authorization_header)
        kwargs["headers"] = headers
        
        # Make the request
        try:
            response = await session.request(method, url, **kwargs)
            
            # Check for 401 and retry once with refreshed token
            if response.status == 401:
                logger.warning("Received 401, refreshing token and retrying")
                await self.refresh_token()
                headers.update(self.authorization_header)
                response.close()
                response = await session.request(method, url, **kwargs)
            
            return response
            
        except Exception as e:
            logger.error("Error making authenticated request: %s", str(e))
            raise