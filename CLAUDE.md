# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server implementation that is being evolved from a basic example server into a comprehensive ACTRIS MLS real estate data integration server. The goal is to provide RESO Web API compliant access to ACTRIS MLS data.

## Development Commands

### Setup and Installation
```bash
# Install dependencies using UV package manager
uv pip install -e .

# Run the MCP server
python -m main
# Or after installation:
unlock-reso-mcp
```

### Project Structure

The codebase follows a simple structure with the main server implementation in `main.py`. The server uses Python's asyncio for handling concurrent operations and the MCP framework for protocol implementation.

Key architectural patterns:
- **Async/await pattern**: All server methods use async/await for non-blocking operations
- **MCP protocol handlers**: Implements `list_tools()`, `call_tool()`, `list_resources()`, `read_resource()`, `list_prompts()`, and `get_prompt()` methods
- **Error handling**: Uses MCP's `McpError` for protocol-specific errors

## Current State vs. Target Architecture

### Current Implementation
The server currently provides example implementations of:
- Tools (calculate, get_weather)
- Resources (config, sample data)
- Prompts (code analysis, summarization)

### Target Architecture (ACTRIS MLS Integration)
Based on `context/claude-code-development-prompt.md`, the server should evolve to:

1. **Authentication Module**: OAuth2 integration with ACTRIS MLS
2. **RESO Web API Client**: Compliant data fetching and mapping
3. **Real Estate Tools**:
   - `search_properties`: Property search with RESO-compliant filters
   - `get_property_details`: Detailed property information
   - `get_market_analytics`: Market statistics and trends
   - `search_agents`: Real estate agent lookup

4. **Data Mapping**: Transform ACTRIS MLS data to standardized RESO format

## Development Context

The `context/` directory contains critical development prompts and plans:
- `claude-code-development-prompt.md`: Detailed requirements for ACTRIS MLS integration
- `unit-test-plan.md`: Testing strategy for the MCP server
- `docker-deployment.md`: Containerization approach

When implementing new features, refer to these documents for requirements and architectural decisions.

## RESO Web API Integration Notes

When working on RESO integration:
1. Follow RESO Web API 2.0.0 specification for data models
2. Implement proper OAuth2 flow for ACTRIS MLS authentication
3. Map ACTRIS-specific fields to RESO standard fields
4. Handle pagination for large result sets
5. Implement proper error handling for API failures

## MCP Server Development

When modifying the MCP server:
1. All methods must be async
2. Use appropriate MCP error types (McpError)
3. Follow the MCP protocol for tool/resource/prompt definitions
4. Maintain backward compatibility with the MCP client interface