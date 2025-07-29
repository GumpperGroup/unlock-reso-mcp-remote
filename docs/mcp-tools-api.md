# MCP Tools API Documentation

## Overview

The UNLOCK MLS MCP Server provides 4 main tools that enable comprehensive real estate data access and analysis. Each tool follows MCP protocol standards and provides both natural language and structured query capabilities.

## Tool Architecture

### Request Flow
```
MCP Client → Tool Call → Input Validation → RESO API Query → 
Data Mapping → Response Formatting → MCP Response
```

### Error Handling
All tools implement consistent error handling with user-friendly messages:
- Input validation errors
- Authentication failures  
- API connectivity issues
- Data formatting problems
- Rate limiting responses

## Tools Reference

### 1. search_properties

Search for properties using natural language queries or structured filters.

#### Tool Schema

```json
{
  "name": "search_properties",
  "description": "Search for properties using natural language or specific criteria",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Natural language search query (e.g., '3 bedroom house under $500k in Austin TX')"
      },
      "filters": {
        "type": "object",
        "description": "Specific search criteria filters",
        "properties": {
          "city": {"type": "string", "description": "City name"},
          "state": {"type": "string", "description": "State abbreviation (e.g., TX, CA)"},
          "zip_code": {"type": "string", "description": "ZIP code"},
          "min_price": {"type": "integer", "description": "Minimum price"},
          "max_price": {"type": "integer", "description": "Maximum price"},
          "min_bedrooms": {"type": "integer", "description": "Minimum bedrooms"},
          "max_bedrooms": {"type": "integer", "description": "Maximum bedrooms"},
          "min_bathrooms": {"type": "number", "description": "Minimum bathrooms"},
          "max_bathrooms": {"type": "number", "description": "Maximum bathrooms"},
          "min_sqft": {"type": "integer", "description": "Minimum square footage"},
          "max_sqft": {"type": "integer", "description": "Maximum square footage"},
          "property_type": {
            "type": "string",
            "enum": ["residential", "condo", "townhouse", "single_family", 
                    "multi_family", "manufactured", "land", "commercial", "business"],
            "description": "Property type"
          },
          "status": {
            "type": "string",
            "enum": ["active", "under_contract", "pending", "sold", "closed",
                    "expired", "withdrawn", "cancelled", "hold"],
            "description": "Property status"
          }
        }
      },
      "limit": {
        "type": "integer",
        "default": 25,
        "minimum": 1,
        "maximum": 100,
        "description": "Maximum number of results to return"
      }
    },
    "oneOf": [
      {"required": ["query"]},
      {"required": ["filters"]}
    ]
  }
}
```

#### Usage Examples

##### Natural Language Search
```json
{
  "name": "search_properties",
  "arguments": {
    "query": "3 bedroom house under $500k in Austin TX",
    "limit": 25
  }
}
```

##### Structured Filter Search
```json
{
  "name": "search_properties", 
  "arguments": {
    "filters": {
      "city": "Austin",
      "state": "TX",
      "min_bedrooms": 3,
      "max_price": 500000,
      "property_type": "single_family",
      "status": "active"
    },
    "limit": 25
  }
}
```

##### Complex Natural Language Query
```json
{
  "name": "search_properties",
  "arguments": {
    "query": "luxury condo with pool downtown Dallas under $400k with 2+ bedrooms and garage"
  }
}
```

#### Response Format

```markdown
Found 15 properties:

1. **LISTING123** - $449,000 | 3 BR, 2 BA | 1,850 sq ft | Single Family
   📍 123 Main Street, Austin, TX 78701
   💬 Beautiful home with updated kitchen and hardwood floors...

2. **LISTING124** - $475,000 | 4 BR, 3 BA | 2,200 sq ft | Single Family
   📍 456 Oak Avenue, Austin, TX 78704
   💬 Spacious family home in desirable neighborhood...

**Search Summary:**
- Query: 3 bedroom house under $500k in Austin TX
- Filters: min bedrooms: 3, max price: 500,000, city: Austin, state: TX
- Results: 15 properties
```

#### Natural Language Processing

The tool automatically parses natural language queries into structured filters:

| Query Pattern | Extracted Filters |
|---------------|---------------------------------------------------------|
| "3 bedroom house" | `{min_bedrooms: 3, property_type: "single_family"}` |
| "under $500k" | `{max_price: 500000}` |
| "in Austin TX" | `{city: "Austin", state: "TX"}` |
| "with pool" | `{amenities: ["pool"]}` |
| "2+ bathrooms" | `{min_bathrooms: 2}` |
| "over 2000 sqft" | `{min_sqft: 2000}` |

---

### 2. get_property_details

Get comprehensive details for a specific property by listing ID.

#### Tool Schema

```json
{
  "name": "get_property_details",
  "description": "Get comprehensive details for a specific property",
  "inputSchema": {
    "type": "object",
    "properties": {
      "listing_id": {
        "type": "string",
        "description": "Property listing ID"
      }
    },
    "required": ["listing_id"]
  }
}
```

#### Usage Example

```json
{
  "name": "get_property_details",
  "arguments": {
    "listing_id": "LISTING123"
  }
}
```

#### Response Format

```markdown
# Property Details - LISTING123

## Basic Information
- **Status**: Active
- **Property Type**: Single Family
- **Property Subtype**: Detached

## Pricing
- **List Price**: $449,000
- **Original List Price**: $459,000

## Property Details
- **Bedrooms**: 3
- **Bathrooms**: 2
- **Full/Half Baths**: 2/0
- **Living Area**: 1,850 sq ft
- **Lot Size**: 0.25 acres
- **Year Built**: 2010
- **Stories**: 1
- **Garage Spaces**: 2

## Location
- **Address**: 123 Main Street
- **City**: Austin
- **State**: TX
- **ZIP Code**: 78701
- **County**: Travis County
- **Subdivision**: Oak Hills

## Features
- Pool, Fireplace

## Schools
- Elementary: Oak Elementary School
- Middle: Austin Middle School
- High: Austin High School

## Important Dates
- **Listed**: 2024-01-15
- **Last Modified**: 2024-01-20

## Listing Information
- **Listing Agent**: John Smith
- **Listing Office**: ABC Realty
- **Phone**: (512) 555-0123
- **Email**: john.smith@abcrealty.com

## Description
Beautiful single-family home in desirable Oak Hills neighborhood. 
Features include updated kitchen with granite countertops, hardwood 
floors throughout, and a private backyard with pool...

## Showing Instructions
Call listing agent for appointments. 24-hour notice preferred.
```

---

### 3. analyze_market

Analyze market trends and statistics for a specific location.

#### Tool Schema

```json
{
  "name": "analyze_market",
  "description": "Analyze market trends and statistics for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "city": {"type": "string", "description": "City name"},
      "state": {"type": "string", "description": "State abbreviation"},
      "zip_code": {"type": "string", "description": "ZIP code"},
      "property_type": {
        "type": "string",
        "enum": ["residential", "condo", "townhouse", "single_family"],
        "description": "Property type for analysis"
      },
      "days_back": {
        "type": "integer",
        "default": 90,
        "minimum": 30,
        "maximum": 365,
        "description": "Number of days to analyze"
      }
    },
    "anyOf": [
      {"required": ["city", "state"]},
      {"required": ["zip_code"]}
    ]
  }
}
```

#### Usage Examples

##### City-Wide Analysis
```json
{
  "name": "analyze_market",
  "arguments": {
    "city": "Austin",
    "state": "TX",
    "property_type": "residential",
    "days_back": 90
  }
}
```

##### ZIP Code Analysis
```json
{
  "name": "analyze_market",
  "arguments": {
    "zip_code": "78701",
    "property_type": "single_family",
    "days_back": 60
  }
}
```

#### Response Format

```markdown
# Market Analysis - Austin, TX

**Property Type**: Residential
**Analysis Period**: Last 90 days

## Active Listings
- **Total Active**: 245 properties
- **Average Price**: $485,000
- **Median Price**: $425,000
- **Price Range**: $195,000 - $1,250,000
- **Average Price/SqFt**: $165.50
- **Bedroom Distribution**:
  - 2 BR: 45 properties
  - 3 BR: 120 properties
  - 4 BR: 65 properties
  - 5 BR: 15 properties

## Recently Sold Properties
- **Total Sold**: 180 properties
- **Average Sold Price**: $468,000
- **Median Sold Price**: $410,000
- **Sold Price Range**: $185,000 - $1,180,000

## Market Insights
- **Price Trend**: Rising (active listings 3.6% higher than recent sales)
- **Inventory Level**: Moderate (245 active listings)
```

#### Market Trend Interpretation

The tool provides intelligent market analysis:

- **Rising Trends**: Active prices >5% higher than sold prices
- **Stable Trends**: Active prices within ±5% of sold prices  
- **Declining Trends**: Active prices >5% lower than sold prices

**Inventory Levels:**
- **Low**: <20 properties (seller's market)
- **Moderate**: 20-50 properties (balanced market)
- **High**: >50 properties (buyer's market)

---

### 4. find_agent

Find real estate agents and members by various criteria.

#### Tool Schema

```json
{
  "name": "find_agent",
  "description": "Find real estate agents or members",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": {"type": "string", "description": "Agent name (partial or full)"},
      "office": {"type": "string", "description": "Office name"},
      "city": {"type": "string", "description": "City"},
      "state": {"type": "string", "description": "State abbreviation"},
      "specialization": {"type": "string", "description": "Agent specialization"},
      "limit": {
        "type": "integer",
        "default": 20,
        "minimum": 1,
        "maximum": 50,
        "description": "Maximum number of results"
      }
    },
    "minProperties": 1
  }
}
```

#### Usage Examples

##### Find by Name
```json
{
  "name": "find_agent",
  "arguments": {
    "name": "John Smith",
    "limit": 10
  }
}
```

##### Find by Location
```json
{
  "name": "find_agent",
  "arguments": {
    "city": "Austin",
    "state": "TX",
    "limit": 20
  }
}
```

##### Find by Office
```json
{
  "name": "find_agent",
  "arguments": {
    "office": "Keller Williams",
    "city": "Austin",
    "state": "TX"
  }
}
```

##### Find by Specialization
```json
{
  "name": "find_agent",
  "arguments": {
    "specialization": "luxury homes",
    "city": "Dallas",
    "state": "TX"
  }
}
```

#### Response Format

```markdown
Found 12 real estate agents:

1. **John Smith** (ID: MEMBER123)
   📧 john.smith@example.com
   📱 (512) 555-0123
   🏢 ABC Realty Group
   📍 Austin, TX
   📄 License: TX-123456789
   🏆 CRS, GRI

2. **Jane Doe** (ID: MEMBER124)
   📧 jane.doe@example.com
   📞 (512) 555-0124
   🏢 XYZ Properties
   📍 Austin, TX
   📄 License: TX-987654321

**Search Summary:**
- Criteria: City: Austin, State: TX
- Results: 12 agents found
```

## Advanced Features

### Query Optimization

The tools implement several optimization features:

1. **Query Caching**: Frequent searches are cached to improve response times
2. **Batch Processing**: Related queries are batched when possible
3. **Smart Defaults**: Intelligent defaults based on query context
4. **Result Ranking**: Results ranked by relevance and recency

### Error Recovery

Comprehensive error handling with graceful degradation:

1. **Partial Results**: Return available data when some fields are missing
2. **Alternative Formats**: Fall back to basic formats when mapping fails
3. **Retry Logic**: Automatic retry for transient failures
4. **User Guidance**: Clear instructions for resolving issues

### Rate Limiting

Built-in rate limiting protection:
- Automatic retry with exponential backoff
- Request queuing during high load
- Clear rate limit error messages
- Suggestion to retry after delay

## Tool Integration Patterns

### Workflow Examples

#### Property Research Workflow
```
1. search_properties (broad criteria)
2. get_property_details (for interesting listings)
3. analyze_market (for target areas)
4. find_agent (for local expertise)
```

#### Market Analysis Workflow
```
1. analyze_market (target area overview)
2. search_properties (current inventory)
3. analyze_market (comparable areas)
4. find_agent (local market experts)
```

#### Investment Analysis Workflow
```
1. analyze_market (multiple cities)
2. search_properties (investment criteria)
3. get_property_details (due diligence)
4. find_agent (local investment specialists)
```

### Chaining Tool Calls

Tools are designed to work together seamlessly:

- Search results include listing IDs for detail retrieval
- Market analysis suggests property search criteria
- Property details include agent information
- Agent search can filter by market areas

## Performance Considerations

### Response Times

Typical response times under normal conditions:

- **search_properties**: 150-300ms
- **get_property_details**: 100-200ms  
- **analyze_market**: 300-500ms
- **find_agent**: 100-250ms

### Concurrent Usage

- Support for 100+ concurrent users
- Request queuing during peak usage
- Automatic load balancing
- Performance monitoring and alerting

### Scalability

- Horizontal scaling support
- Database connection pooling
- Intelligent caching strategies
- Graceful degradation under load

## Testing and Validation

### Unit Testing

Each tool has comprehensive unit tests covering:
- Input validation scenarios
- API response handling
- Error conditions
- Data mapping accuracy

### Integration Testing

End-to-end testing with real API calls:
- Live data validation
- Performance benchmarking
- Error scenario simulation
- Cross-tool workflow testing

### Test Coverage

Current test coverage: 85%+ for all tool implementations

## Security Considerations

### Input Sanitization

All tool inputs are sanitized to prevent:
- SQL injection attacks
- XSS vulnerabilities
- Path traversal attempts
- Command injection

### Data Privacy

- No sensitive data stored locally
- API credentials secured
- Request logging excludes PII
- Response filtering for privacy

### Authentication

- Bearer token validation on each request
- Automatic token refresh
- Secure credential storage
- Access logging and monitoring

This comprehensive tool API provides robust, secure, and user-friendly access to real estate data through the MCP protocol.