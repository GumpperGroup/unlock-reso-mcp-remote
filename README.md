# UNLOCK MLS RESO Reference MCP Server

A Model Context Protocol (MCP) server that provides standardized access to UNLOCK MLS real estate data through Bridge Interactive's RESO Web API. This server enables AI applications like Claude to query, analyze, and interact with real estate listings data.

## Features

### 🏠 **Property Search & Analysis**
- **Natural Language Search**: Use conversational queries like "3 bedroom house under $500k in Austin TX"
- **Location-Based Search**: Find properties near specific locations using Google Maps integration
- **Travel Time Analysis**: Search properties within commute time to work, school, or points of interest
- **Advanced Filtering**: Precise search with price ranges, property types, location, and features
- **Detailed Property Information**: Comprehensive property details including photos, descriptions, and agent information
- **Market Analysis**: Real-time market trends, pricing statistics, and inventory analysis

### 🏘️ **Market Intelligence**
- **Price Trend Analysis**: Understand market direction and pricing patterns
- **Inventory Analysis**: Supply and demand indicators for informed decisions
- **Comparative Market Analysis**: Compare different areas and property types
- **Investment Metrics**: Data for real estate investment decision-making

### 👥 **Agent & Professional Network**
- **Agent Search**: Find qualified real estate professionals by location, specialization, or office
- **Professional Profiles**: Access to agent credentials, contact information, and expertise areas
- **Local Market Experts**: Connect with agents who specialize in specific markets

### 📊 **Comprehensive Resources**
- **Guided Workflows**: Step-by-step guides for common real estate tasks
- **Market Insights**: Educational resources for understanding market data
- **API Status Monitoring**: Real-time system health and connectivity information

**MCP Server Documentation**
- /Users/davidgumpper/Documents/projects/unlock-reso-mcp/docs/README.md

## Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Bridge Interactive API credentials
- Google Maps API key (optional, for location-based searches)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd unlock-reso-mcp
   ```

2. **Install dependencies**:
   ```bash
   uv sync --dev
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Bridge Interactive credentials
   ```

4. **Run the MCP server**:
   ```bash
   python -m main
   ```

### Environment Configuration

Create a `.env` file in the project root with the following variables:

```bash
# Bridge Interactive API Configuration (Required)
BRIDGE_SERVER_TOKEN=your_server_token_here
BRIDGE_CLIENT_ID=your_client_id_here
BRIDGE_CLIENT_SECRET=your_client_secret_here
BRIDGE_MLS_ID=your_mls_id_here
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2

# Optional Configuration
LOG_LEVEL=INFO
API_RATE_LIMIT_PER_MINUTE=60
CACHE_ENABLED=false
CACHE_TTL_SECONDS=300

# Google Maps API Configuration (Optional - for location-based searches)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
GOOGLE_MAPS_CACHE_TTL_HOURS=24
GOOGLE_MAPS_MAX_REQUESTS_PER_DAY=800
GOOGLE_DISTANCE_MATRIX_ENABLED=false
```

### Claude Desktop Integration

Add the following configuration to your Claude Desktop MCP settings:

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

## Usage Examples

### Property Search

**Natural Language Queries**:
```
Find me a 3 bedroom house under $500k in Austin TX
Show me condos with pool downtown Dallas under $400k
Search for single family homes over 2000 sqft in Houston
Find properties within 30-minute drive to downtown Austin
Properties within walking distance of UT campus under $400k
```

**Structured Search**:
```json
{
  "filters": {
    "city": "Austin",
    "state": "TX",
    "min_bedrooms": 3,
    "max_price": 500000,
    "property_type": "single_family"
  },
  "limit": 25
}
```

### Market Analysis

**City-Wide Analysis**:
```json
{
  "city": "Austin",
  "state": "TX",
  "property_type": "residential",
  "days_back": 90
}
```

**ZIP Code Analysis**:
```json
{
  "zip_code": "78701",
  "property_type": "single_family",
  "days_back": 90
}
```

### Agent Search

**Find Local Agents**:
```json
{
  "city": "Austin",
  "state": "TX",
  "limit": 20
}
```

**Search by Specialization**:
```json
{
  "specialization": "luxury homes",
  "city": "Dallas",
  "state": "TX"
}
```

## API Reference

### Tools

#### `search_properties`
Search for properties using natural language or specific criteria.

**Parameters**:
- `query` (string, optional): Natural language search query
- `filters` (object, optional): Structured search filters
- `limit` (integer, optional): Maximum results (default: 25, max: 100)

**Example**:
```json
{
  "query": "3 bedroom house under $500k in Austin TX",
  "limit": 25
}
```

#### `get_property_details`
Get comprehensive details for a specific property.

**Parameters**:
- `listing_id` (string, required): Property listing ID

**Example**:
```json
{
  "listing_id": "LISTING123"
}
```

#### `analyze_market`
Analyze market trends and statistics for a location.

**Parameters**:
- `city` (string): City name
- `state` (string): State abbreviation
- `zip_code` (string): ZIP code (alternative to city/state)
- `property_type` (string, optional): Property type filter
- `days_back` (integer, optional): Analysis period in days (default: 90)

**Example**:
```json
{
  "city": "Austin",
  "state": "TX",
  "property_type": "residential",
  "days_back": 90
}
```

#### `find_agent`
Find real estate agents or members.

**Parameters**:
- `name` (string, optional): Agent name (partial or full)
- `office` (string, optional): Office name
- `city` (string, optional): City
- `state` (string, optional): State abbreviation
- `specialization` (string, optional): Agent specialization
- `limit` (integer, optional): Maximum results (default: 20, max: 50)

**Example**:
```json
{
  "name": "John Smith",
  "city": "Austin",
  "state": "TX",
  "limit": 20
}
```

#### `find_properties_near_location`
Find properties near a specific location using Google Maps integration.

**Parameters**:
- `location` (string, required): Location name, address, or point of interest
- `radius_miles` (number, optional): Search radius in miles (default: 1.0)
- `travel_mode` (string, optional): Travel mode for distance calculations (driving, walking, bicycling, transit)
- `max_travel_time_minutes` (integer, optional): Maximum travel time in minutes
- `use_travel_time` (boolean, optional): Enable travel time calculations (default: false)
- `property_filters` (object, optional): Standard property search filters
- `limit` (integer, optional): Maximum results (default: 25, max: 100)

**Examples**:
```json
{
  "location": "Austin City Hall",
  "radius_miles": 2.0,
  "property_filters": {
    "max_price": 500000,
    "min_bedrooms": 2
  }
}
```

**With Travel Time Analysis**:
```json
{
  "location": "Dell Technologies, Round Rock TX",
  "travel_mode": "driving",
  "max_travel_time_minutes": 30,
  "use_travel_time": true,
  "property_filters": {
    "min_bedrooms": 3,
    "max_price": 600000
  }
}
```

#### `find_distance_to_nearest`
Find the distance between a property address and the nearest location of a specific type.

**Parameters**:
- `property_address` (string, required): Property address to calculate distance from
- `place_type` (string, required): Type of place to find (e.g., 'hospital', 'school', 'restaurant', 'grocery_store', 'park', 'gas_station')
- `radius_miles` (number, optional): Search radius in miles (default: 5.0, max: 25.0)
- `max_results` (integer, optional): Maximum number of nearest places to return (default: 5, max: 20)

**Examples**:
```json
{
  "property_address": "123 Main St, Austin TX",
  "place_type": "hospital",
  "radius_miles": 10.0,
  "max_results": 3
}
```

**Response includes**:
- Distance in miles to each location
- Location name, address, and Google Maps ratings
- Direct Google Maps links for navigation
- Summary of nearest location found

### Resources

The server provides several informational resources:

- **Property Search Examples**: Common search query examples and patterns
- **Property Types Reference**: Guide to property types and status values
- **Market Analysis Guide**: How to interpret market analysis data
- **Agent Search Guide**: Finding and working with real estate agents
- **Common Workflows**: Real estate workflow patterns and best practices
- **Guided Property Search**: Step-by-step property search workflows
- **Guided Market Analysis**: Step-by-step market analysis workflows
- **API Status & Info**: Current system status and configuration

## Development

### Project Structure

```
unlock-reso-mcp/
├── src/
│   ├── auth/                    # OAuth2 authentication
│   ├── config/                  # Configuration and settings
│   ├── utils/                   # Utilities and integrations
│   │   ├── data_mapper.py       # RESO data mapping
│   │   ├── validators.py        # Input validation
│   │   ├── google_places_client.py  # Google Maps API client
│   │   └── location_service.py  # Location-based search service
│   ├── reso_client.py          # RESO API client
│   └── server.py               # Main MCP server implementation
├── tests/                      # Test suite
├── context/                    # API documentation and examples
├── main.py                     # Entry point
└── pyproject.toml             # Project configuration
```

### Development Commands

```bash
# Install development dependencies
uv sync --dev

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run linting
ruff check src tests

# Run type checking
mypy src

# Run a specific test
pytest tests/test_oauth2.py -v

# Run tests matching pattern
pytest -k "test_search" -v
```

### Testing

The project includes enterprise-grade test coverage:

- **Unit Tests**: All modules have dedicated test files (141+ core tests)
- **Integration Tests**: End-to-end workflow testing with real API validation
- **Performance Tests**: Benchmarking with 17,000+ operations/second capacity
- **Error Scenario Tests**: Comprehensive error handling validation (24+ tests)
- **Load Tests**: Production readiness validation with concurrent user simulation
- **Real API Testing**: Validated with live Bridge Interactive RESO Web API
- **Mock Testing**: Comprehensive fixtures for development and CI/CD
- **Coverage**: 85% code coverage with quality validation

### Architecture

The server is built with the following components:

1. **MCP Server Framework**: Uses the standard `mcp.server` framework for MCP compliance
2. **Bearer Token Authentication**: Server token authentication using `BRIDGE_SERVER_TOKEN`
3. **RESO API Client**: Async HTTP client with OData query building capabilities
4. **Google Maps Integration**: Places API and Distance Matrix API for location intelligence
5. **Location Services**: Coordinate-based search with travel time analysis
6. **Data Mapping**: Translates RESO fields to user-friendly formats
7. **Natural Language Processing**: Parses conversational search queries into structured filters
8. **Comprehensive Error Handling**: Graceful degradation with user-friendly error messages

## Bridge Interactive API

This server integrates with Bridge Interactive's RESO Web API to provide access to UNLOCK MLS data. The API follows RESO Data Dictionary 2.0 standards for consistent field naming and data structures.

### API Endpoints Used

- **Authentication**: Bearer token using `BRIDGE_SERVER_TOKEN`
- **Property Data**: `/OData/{MLS_ID}/Property` - Property listings and details
- **Member Data**: `/OData/{MLS_ID}/Member` - Real estate agent information
- **Office Data**: `/OData/{MLS_ID}/Office` - Brokerage office details
- **Lookup Data**: `/OData/{MLS_ID}/Lookup` - Reference data and metadata

### Data Standards

All data returned follows RESO Data Dictionary 2.0 specifications:
- Standardized field names and formats
- Consistent property status values
- Uniform address and contact information structure
- Standardized property types and features

## Troubleshooting

### Common Issues

#### Authentication Errors
- Verify Bridge Interactive API credentials in `.env` file
- Check that `BRIDGE_SERVER_TOKEN` is correct and valid
- Ensure proper `BRIDGE_MLS_ID` is configured for your access
- Ensure network connectivity to `api.bridgedataoutput.com`

#### No Search Results
- Check city name spelling and state abbreviation
- Try broader search criteria (increase price range, reduce requirements)
- Verify the area has MLS coverage through UNLOCK

#### Server Connection Issues
- Ensure Python 3.11+ is installed
- Check that all dependencies are installed with `uv sync --dev`
- Verify the server is running on the correct transport (stdio)

#### Google Maps Integration Issues
- Verify Google Maps API key is correct in `.env` file
- Ensure Places API is enabled in Google Cloud Console
- Check API key restrictions (IP restrictions, referrer restrictions)
- Verify daily quota limits are not exceeded
- Location searches work without travel time if Distance Matrix API is disabled

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
LOG_LEVEL=DEBUG
```

This will provide detailed information about API calls, authentication, and data processing.

### Support

For technical support:
1. Check the troubleshooting section above
2. Review server logs for error details
3. Verify environment configuration
4. Test API connectivity with Bridge Interactive

## License

This project is private and owned by David Gumpper, Gumpper Group LLC.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass and coverage is maintained
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new functionality
- Maintain or improve code coverage
- Update documentation for API changes
- Follow conventional commit message format

## Changelog

### Version 1.1.0 (Current) - PRODUCTION READY + GOOGLE MAPS
- ✅ Complete MCP server implementation with location intelligence
- ✅ **6 main tools**: search_properties, get_property_details, analyze_market, find_agent, find_properties_near_location, find_distance_to_nearest
- ✅ **Google Maps Integration**: Places API and Distance Matrix API support
- ✅ **Location-Based Search**: Natural language location queries with travel time analysis
- ✅ **Multi-Modal Transportation**: Support for driving, walking, bicycling, and transit modes
- ✅ 8 comprehensive resources and guides
- ✅ Natural language query processing
- ✅ **Real API Integration**: Validated with Bridge Interactive RESO Web API
- ✅ **Bearer Token Authentication**: Server token authentication working
- ✅ RESO Data Dictionary 2.0 compliance
- ✅ **Enterprise Testing**: 141+ tests with 85% coverage
- ✅ **Performance Validated**: 17,000+ operations/second capacity
- ✅ Comprehensive documentation with Google Maps integration guide

## Roadmap

### ✅ Phase 7: Enhanced Testing Suite (Completed)
- ✅ Integration tests for end-to-end workflows
- ✅ Performance testing and benchmarks
- ✅ Error scenario testing
- ✅ Load testing for production readiness
- ✅ Test data fixtures and utilities

### ✅ Phase 8: Google Maps Integration (Completed)
- ✅ Google Places API integration for location resolution
- ✅ Distance Matrix API for travel time calculations
- ✅ Location-based property search with `find_properties_near_location` tool
- ✅ Multi-modal transportation support (driving, walking, bicycling, transit)
- ✅ Cost-optimized hybrid distance calculation strategy
- ✅ Comprehensive integration documentation

### Phase 9: Deployment & CI/CD
- Docker containerization
- GitHub Actions workflow
- Deployment documentation

### Phase 10: Enhanced Features
- Real-time traffic integration
- Advanced route optimization
- School district integration
- Public transit schedules