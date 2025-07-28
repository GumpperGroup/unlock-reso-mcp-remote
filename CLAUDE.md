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
# or using src.server module:
python -m src.server

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

# Run specific test categories
pytest tests/test_integration.py -v        # Integration tests
pytest tests/test_performance.py -v       # Performance tests
pytest tests/test_error_scenarios.py -v   # Error scenario tests
pytest tests/test_load.py -v              # Load tests
```

## Architecture Overview

### Core Components

1. **MCP Server Framework** (src/server.py)
   - Complete MCP server implementation using mcp.server framework
   - Implements 4 main tools: search_properties, get_property_details, analyze_market, find_agent
   - Uses stdio transport for Claude Desktop integration
   - Includes 8 MCP resources for documentation and examples

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
- Phases 1-7 are complete (Project Setup through Enhanced Testing Suite)
- All core components implemented and tested
- MCP server with 4 tools and 8 resources fully functional
- 195+ tests passing with 89% code coverage
- Enterprise-grade testing capabilities established

### Completed Components
1. ✅ OAuth2 authentication handler (src/auth/oauth2.py)
2. ✅ RESO API client (src/reso_client.py)  
3. ✅ Data mapping utilities (src/utils/data_mapper.py)
4. ✅ Input validation and natural language parsing (src/utils/validators.py)
5. ✅ Complete MCP server implementation (src/server.py)
6. ✅ Comprehensive test suite with 89% coverage
7. ✅ Enhanced testing suite with enterprise-grade capabilities:
   - ✅ Integration tests for end-to-end workflows (tests/test_integration.py)
   - ✅ Performance testing and benchmarks (tests/test_performance.py)
   - ✅ Error scenario testing (tests/test_error_scenarios.py)
   - ✅ Load testing for production readiness (tests/test_load.py)
   - ✅ Test data fixtures and utilities (tests/fixtures/)

### Next Steps (Remaining Phases)
- Phase 8: Optimization and Enhancement
- Phase 9: Deployment and CI/CD
- Phase 10: Final Validation and Success Criteria

### Testing Strategy
- Unit tests for each module with pytest (141 tests)
- Integration tests for end-to-end workflows (10 comprehensive tests)
- Performance testing with benchmarking and scalability validation (15+ tests)
- Error scenario testing with comprehensive error handling validation (24+ tests)
- Load testing for production readiness (5+ tests)
- Mock external API calls using aioresponses
- Realistic test data fixtures for comprehensive testing scenarios
- Current: 89% code coverage achieved (195+ tests passing)

## Important Considerations

1. **RESO Compliance**: All field names and data structures must follow RESO Data Dictionary 2.0
2. **Async Operations**: All I/O operations use async/await for performance
3. **Error Handling**: Graceful handling of API errors with user-friendly messages
4. **Security**: OAuth2 tokens must be handled securely, never logged or exposed
5. **Testing**: Enterprise-grade test suite with 195+ tests covering integration, performance, error scenarios, and load testing
6. **Production Readiness**: Comprehensive validation for production deployment with performance benchmarks and load testing

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