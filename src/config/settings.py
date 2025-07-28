"""Configuration settings for UnlockRESO MCP Server."""

import logging
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Bridge Interactive API Configuration
    bridge_api_base_url: str = "https://api.bridgedataoutput.com/api/v2"
    bridge_client_id: str
    bridge_client_secret: str
    bridge_mls_id: str = "UNLOCK"
    bridge_server_token: Optional[str] = None

    # MCP Server Configuration
    mcp_server_name: str = "unlock-mls-mcp"
    log_level: str = "INFO"

    # Optional configurations
    api_rate_limit_per_minute: int = 60
    cache_enabled: bool = False
    cache_ttl_seconds: int = 300

    @property
    def odata_endpoint(self) -> str:
        """Get the OData endpoint URL for the configured MLS."""
        return f"{self.bridge_api_base_url}/OData/{self.bridge_mls_id}"

    @property
    def token_endpoint(self) -> str:
        """Get the OAuth2 token endpoint URL."""
        return f"{self.bridge_api_base_url}/oauth2/token"

    @property
    def log_level_numeric(self) -> int:
        """Convert log level string to numeric value."""
        return getattr(logging, self.log_level.upper(), logging.INFO)


# Create a singleton instance
settings = Settings()