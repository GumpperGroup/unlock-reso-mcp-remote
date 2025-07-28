# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides standardized access to UNLOCK MLS real estate data through Bridge Interactive's RESO Web API. The server enables AI applications to query, analyze, and interact with real estate listings data.

## Key Development Commands

```bash
# Install dependencies (including dev dependencies)
uv sync --dev

# Run the MCP server
python -m main
# or after installation:
unlock-reso-mcp

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run linting
ruff check src tests

# Run type checking
mypy src

# Run a single test file
pytest tests/test_oauth2.py -v

# Run tests matching a pattern
pytest -k "test_search" -v
```

## Architecture Overview

### Core Components

1. **MCP Server Framework**
   - Currently using basic MCP server (main.py) - needs migration to FastMCP
   - Will implement 4 main tools: search_properties, get_property_details, analyze_market, find_agent
   - Uses stdio transport for Claude Desktop integration

2. **Authentication Layer** (src/auth/)
   - OAuth2 client credentials flow for Bridge Interactive API
   - Token management with automatic refresh
   - Support for Google Workspace and Microsoft 365 IdP

3. **RESO API Client** (src/reso_client.py)
   - Async HTTP client using aiohttp
   - OData query builder for RESO endpoints
   - Handles Property, Member, Office, OpenHouse, and Lookup resources

4. **Data Layer** (src/utils/)
   - ResoDataMapper: Translates RESO fields to user-friendly formats
   - QueryValidator: Input validation and natural language parsing
   - Address formatting, price formatting, status mapping

### Bridge Interactive API Integration

The project includes comprehensive documentation for Bridge Interactive's RESO API in the `context/` directory:
- API authentication and general documentation
- Property, Member, Office, OpenHouse, and Lookup endpoint specifications
- RESO Data Dictionary 2.0 compliance requirements

### Key API Endpoints

- Base URL: `https://api.bridgedataoutput.com/api/v2`
- OAuth2 Token: `/oauth2/token`
- OData Endpoints: `/OData/UNLOCK/{Resource}`
  - Property, Member, Office, OpenHouse, Media, Lookup

### Environment Configuration

Required environment variables (see .env.example):
- `BRIDGE_CLIENT_ID`: OAuth2 client ID
- `BRIDGE_CLIENT_SECRET`: OAuth2 client secret
- `BRIDGE_MLS_ID`: Set to "UNLOCK"
- `BRIDGE_API_BASE_URL`: API base URL
- `LOG_LEVEL`: Logging level (default: INFO)

## Development Workflow

### Current State
- Phase 1 (Project Setup) is complete
- Main.py contains a basic MCP server implementation with example tools
- Need to implement RESO-specific functionality starting with Phase 2 (OAuth2)

### Next Steps
1. Implement OAuth2 authentication handler (src/auth/oauth2.py)
2. Create RESO API client (src/reso_client.py)
3. Build data mapping utilities
4. Replace example tools in main.py with real estate tools

### Testing Strategy
- Unit tests for each module with pytest
- Mock external API calls using aioresponses
- Integration tests for end-to-end flows
- Minimum 80% code coverage target

## Important Considerations

1. **RESO Compliance**: All field names and data structures must follow RESO Data Dictionary 2.0
2. **Async Operations**: All I/O operations use async/await for performance
3. **Error Handling**: Graceful handling of API errors with user-friendly messages
4. **Security**: OAuth2 tokens must be handled securely, never logged or exposed

## MCP Server Configuration

For Claude Desktop integration, users need to add this to their config:
```json
{
  "mcpServers": {
    "unlock-mls-mcp": {
      "command": "python",
      "args": ["-m", "main"],
      "cwd": "/path/to/unlock-reso-mcp"
    }
  }
}
```