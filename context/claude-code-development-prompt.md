# Claude Code Prompt: Build UNLOCK MLS MCP Server

## Project Overview
I need you to develop a Model Context Protocol (MCP) server that provides standardized access to UNLOCK MLS real estate data through Bridge Interactive's RESO Web API. This server will enable AI applications to query, analyze, and interact with real estate listings data.

## Technical Requirements

### Core Technologies
- **Language**: Python 3.10+
- **Python Package Management**: uv 
- **MCP Framework**: FastMCP (mcp[cli]>=1.4.0)
- **HTTP Client**: aiohttp for async RESO API calls
- **Authentication**: OAuth2 client credentials flow
- **Data Standards**: RESO Data Dictionary 2.0 compliance
- **Unlock MLS**: Unlock MLS RESO Compliant Data API
- **Transport Protocol**: Streaming HTTP for remote server access
- **Authentication/Authorization**: Outh2 - IdP-Google Workspace and Microsoft 365.

### Bridge Interactive Documents for Inclusion into the MCP Server
- API Documentation - /Users/davidgumpper/Documents/projects/unlock-reso-mcp/context/bridge-interactive-unlock-api-documentation.md
- Property Resource Endpoint Documentation - /Users/davidgumpper/Documents/projects/unlock-reso-mcp/context/bridge-interactive-property-api-endpoint.md
- Member Resource Endpoint Documentation - /Users/davidgumpper/Documents/projects/unlock-reso-mcp/context/bridge-interactive-member-api-endpoint.md
- Office Resource Endpoint Documentation - /Users/davidgumpper/Documents/projects/unlock-reso-mcp/context/bridge-interactive-office-api-endpoint.md
- OpenHouse Resource Endpoint Documentation - /Users/davidgumpper/Documents/projects/unlock-reso-mcp/context/bridge-interactive-openhouse-api-endpoint.md
- Lookup Values Endpoint Documentation - /Users/davidgumpper/Documents/projects/unlock-reso-mcp/context/bridge-interactive-lookup-api-endpoint.md

### Project Structure
```
UNLOCK-mls-mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py              # Main MCP server
│   ├── reso_client.py         # RESO Web API client
│   ├── auth/
│   │   └── oauth2.py          # OAuth2 handler
│   ├── utils/
│   │   ├── data_mapper.py     # RESO field mapping
│   │   └── validators.py      # Input validation
│   └── config/
│       └── settings.py        # Configuration
├── tests/
├── pyproject.toml
├── .env.example
└── README.md
```

## MCP Tools to Implement

### 1. Property Search Tool
```python
@mcp.tool(
    name="search_properties",
    description="Search properties using natural language or criteria"
)
async def search_properties(
    query: Optional[str] = None,
    city: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    property_type: Optional[str] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[float] = None,
    min_sqft: Optional[int] = None,
    max_results: int = 10
) -> Dict[str, Any]
```

**Requirements:**
- Convert parameters to RESO OData queries
- Always filter by StandardStatus = 'Active'
- Return user-friendly formatted results
- Handle natural language queries

### 2. Property Details Tool
```python
@mcp.tool(
    name="get_property_details",
    description="Get comprehensive property information"
)
async def get_property_details(listing_id: str) -> Dict[str, Any]
```

**Requirements:**
- Fetch all available property fields
- Include nested data (features, location, financial)
- Format addresses properly
- Return media/photos if available

### 3. Market Analytics Tool
```python
@mcp.tool(
    name="analyze_market",
    description="Analyze market trends for an area"
)
async def analyze_market(
    location: str,
    timeframe: str = "6months",
    property_type: Optional[str] = None
) -> Dict[str, Any]
```

**Requirements:**
- Calculate median/average prices
- Show price trends
- Count active vs sold listings
- Support ZIP codes and city names

### 4. Agent Lookup Tool
```python
@mcp.tool(
    name="find_agent",
    description="Find real estate agents"
)
async def find_agent(
    name: Optional[str] = None,
    office: Optional[str] = None,
    area: Optional[str] = None
) -> Dict[str, Any]
```

## RESO API Client Implementation

### OAuth2 Authentication
```python
class ResoWebApiClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str, mls_id: str):
        self.base_url = base_url
        self.odata_endpoint = f"{base_url}/OData/{mls_id}"
        self.token_endpoint = f"{base_url}/oauth2/token"
    
    async def _authenticate(self):
        # Implement OAuth2 client credentials flow
        # Store access_token and handle expiration
```

### Key RESO Endpoints
- **Property**: `/OData/UNLOCK/Property`
- **Member**: `/OData/UNLOCK/Member`
- **Office**: `/OData/UNLOCK/Office`
- **Media**: `/OData/UNLOCK/Media`
- **Lookup**: `/OData/UNLOCK/Lookup`

## RESO Field Mappings

### Critical Property Fields
```python
RESO_PROPERTY_FIELDS = {
    'ListingId': 'Unique identifier',
    'ListingKey': 'MLS number',
    'StandardStatus': 'Active, Pending, Closed',
    'ListPrice': 'Current price',
    'BedroomsTotal': 'Number of bedrooms',
    'BathroomsTotalInteger': 'Number of bathrooms',
    'LivingArea': 'Square footage',
    'PropertyType': 'Residential, Commercial, etc',
    'PropertySubType': 'Single Family, Condo, etc',
    'StreetAddress': 'Street components',
    'City': 'City name',
    'StateOrProvince': 'State code',
    'PostalCode': 'ZIP code',
    'ModificationTimestamp': 'Last updated'
}
```

## Data Mapping Requirements

### Address Formatting
```python
def format_address(property_data: Dict) -> str:
    # Combine: StreetNumber, StreetDirPrefix, StreetName, 
    # StreetSuffix, StreetDirSuffix, UnitNumber
    # Format: "123 N Main St #4, Austin, TX 78701"
```

### Status Mapping
```python
STATUS_MAP = {
    'Active': 'Active',
    'Pending': 'Under Contract',
    'Closed': 'Sold',
    'ComingSoon': 'Coming Soon',
    'Withdrawn': 'Withdrawn',
    'Expired': 'Expired'
}
```

## Environment Configuration
```bash
# .env file structure
BRIDGE_API_BASE_URL=https://api.bridgedataoutput.com/api/v2
BRIDGE_CLIENT_ID=your_client_id
BRIDGE_CLIENT_SECRET=your_client_secret
BRIDGE_MLS_ID=UNLOCK
MCP_SERVER_NAME=UNLOCK-mls-mcp
LOG_LEVEL=INFO
```

## Implementation Priorities

### Phase 1: Core Functionality
1. Set up project structure
2. Implement OAuth2 authentication
3. Create basic property search tool
4. Implement data mapping utilities

### Phase 2: Enhanced Features
1. Add property details tool
2. Implement market analytics
3. Add agent lookup
4. Create MCP resources and prompts

### Phase 3: Optimization
1. Add caching layer
2. Implement rate limiting
3. Enhance error handling
4. Add comprehensive logging

## Testing Requirements
Please review the /Users/davidgumpper/Documents/projects/unlock-reso-mcp/context/claude-code-test-prompt.md to build out the testing todos

### Unit Tests
- Test OAuth2 authentication flow
- Test OData query builders
- Test data mapping functions
- Validate field transformation
- Review the /Users/davidgumpper/Documents/projects/unlock-reso-mcp/context/test-prompt-concise.md and /Users/davidgumpper/Documents/projects/unlock-reso-mcp/context/unit-test-plan.md

### Integration Tests
- Test full property search flow
- Verify MCP tool execution
- Test error scenarios

### Example Test Queries
```python
# Test natural language search
"Find 3-bedroom homes in Austin under $500,000"

# Test specific criteria
{
    "city": "Austin",
    "min_price": 300000,
    "max_price": 500000,
    "property_type": "Residential",
    "bedrooms": 3
}

# Test market analysis
{
    "location": "78701",
    "timeframe": "6months"
}
```

## Success Criteria
1. **Authentication**: Successfully authenticate with Bridge Interactive API
2. **Data Retrieval**: Query and retrieve UNLOCK MLS data
3. **RESO Compliance**: Use standard RESO field names and mappings
4. **MCP Integration**: Tools work with Claude Desktop and MCP Inspector
5. **Performance**: Async operations with <2s response times
6. **Error Handling**: Graceful handling of API errors and invalid inputs

## Code Quality Standards
- Use type hints throughout
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Implement proper logging
- Handle exceptions gracefully
- Use async/await for all I/O operations

## Deliverables
1. Complete MCP server implementation
2. All four tools functioning correctly
3. Proper RESO field mapping
4. Environment configuration template
5. Basic test suite
6. README with usage instructions

## Additional Context
- Bridge Interactive API Docs: https://bridgedataoutput.com/docs/platform/API/reso-web-api
- RESO Data Dictionary 2.0: https://ddwiki.reso.org/display/DDW20/
- MCP Documentation: https://modelcontextprotocol.io/

Please implement this MCP server following the specifications above, ensuring it's production-ready and follows Python best practices. Start with the core structure and authentication, then build out each tool incrementally.