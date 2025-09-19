# API Reference

Complete reference documentation for the UNLOCK MLS MCP Server tools and resources.

## MCP Tools

### search_properties

Search for properties using natural language queries or structured filters.

#### Input Schema

```json
{
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
          "enum": ["residential", "condo", "townhouse", "single_family", "multi_family", "manufactured", "land", "commercial", "business"],
          "description": "Property type"
        },
        "status": {
          "type": "string",
          "enum": ["active", "under_contract", "pending", "sold", "closed", "expired", "withdrawn", "cancelled", "hold"],
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
```

#### Examples

**Natural Language Search:**
```json
{
  "query": "3 bedroom house under $500k in Austin TX",
  "limit": 25
}
```

**Structured Filter Search:**
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

**Combined Search:**
```json
{
  "query": "house with pool in Austin",
  "filters": {
    "max_price": 600000
  },
  "limit": 10
}
```

#### Response Format

Returns a formatted text response with property listings including:
- Listing ID and summary information
- Address and location details
- Property highlights and remarks
- Search summary with applied filters

---

### get_property_details

Get comprehensive details for a specific property by listing ID.

#### Input Schema

```json
{
  "type": "object",
  "properties": {
    "listing_id": {
      "type": "string",
      "description": "Property listing ID"
    }
  },
  "required": ["listing_id"]
}
```

#### Example

```json
{
  "listing_id": "LISTING123"
}
```

#### Response Format

Returns a detailed markdown-formatted property report including:

- **Basic Information**: Status, property type, subtype
- **Pricing**: List price, original price, sold price (if applicable)
- **Property Details**: Bedrooms, bathrooms, square footage, lot size, year built
- **Location**: Full address, city, state, ZIP, county, subdivision
- **Features**: Pool, fireplace, waterfront, view details
- **Schools**: Elementary, middle, and high school information
- **Important Dates**: Listed date, sold date, contract date, last modified
- **Listing Information**: Agent name, office, contact details
- **Description**: Public remarks and showing instructions

---

### analyze_market

Analyze market trends and statistics for a specific location.

#### Input Schema

```json
{
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
```

#### Examples

**City Analysis:**
```json
{
  "city": "Austin",
  "state": "TX",
  "property_type": "residential",
  "days_back": 90
}
```

**ZIP Code Analysis:**
```json
{
  "zip_code": "78701",
  "property_type": "single_family",
  "days_back": 60
}
```

#### Response Format

Returns a comprehensive market analysis report including:

- **Active Listings**: Total count, average/median prices, price range, price per sqft
- **Recently Sold Properties**: Sales data, pricing statistics
- **Market Insights**: Price trends (rising/stable/declining), inventory levels
- **Bedroom Distribution**: Breakdown by number of bedrooms
- **Market Conditions**: Assessment for buyers, sellers, and investors

---

### find_agent

Find real estate agents or members based on search criteria.

#### Input Schema

```json
{
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
```

#### Examples

**Name Search:**
```json
{
  "name": "John Smith",
  "limit": 10
}
```

**Location Search:**
```json
{
  "city": "Austin",
  "state": "TX",
  "limit": 20
}
```

**Office Search:**
```json
{
  "office": "Keller Williams",
  "city": "Dallas",
  "state": "TX"
}
```

#### Response Format

Returns agent information including:
- Agent name and member ID
- Contact information (email, phone)
- Office affiliation and location
- License information
- Professional designations
- Search summary with criteria used

---

## MCP Resources

### Property Search Examples
- **URI**: `property://search/examples`
- **Content**: Common property search query examples and patterns
- **Use Case**: Learning effective search techniques

### Property Types Reference
- **URI**: `property://types/reference`
- **Content**: Guide to property types and status values
- **Use Case**: Understanding property classification and status meanings

### Market Analysis Guide
- **URI**: `market://analysis/guide`
- **Content**: How to interpret market analysis data
- **Use Case**: Understanding market trends and making informed decisions

### Agent Search Guide
- **URI**: `agent://search/guide`
- **Content**: Guide for finding and working with real estate agents
- **Use Case**: Agent selection and professional relationship management

### Common Workflows
- **URI**: `workflows://common/patterns`
- **Content**: Real estate workflow patterns and best practices
- **Use Case**: Step-by-step guidance for common real estate tasks

### Guided Property Search
- **URI**: `prompts://guided/search`
- **Content**: Step-by-step guided property search workflows
- **Use Case**: Interactive property search assistance

### Guided Market Analysis
- **URI**: `prompts://guided/analysis`
- **Content**: Step-by-step guided market analysis workflows
- **Use Case**: Interactive market analysis assistance

### API Status & Info
- **URI**: `api://status/info`
- **Content**: Current system status and configuration information
- **Use Case**: System health monitoring and troubleshooting

---

## Error Handling

All tools implement comprehensive error handling with user-friendly messages:

### Validation Errors
- Input parameter validation
- Format checking (city names, state codes, etc.)
- Range validation (prices, dates, limits)

### API Errors
- Authentication failures
- Network connectivity issues
- Rate limiting responses
- Data not found scenarios

### Error Response Format

```json
{
  "content": [
    {
      "type": "text",
      "text": "Error: [User-friendly error message describing the issue and potential solutions]"
    }
  ]
}
```

### Common Error Messages

- **"Validation error: City name must be at least 2 characters"**
- **"Property with listing ID 'ABC123' not found"**
- **"No properties found matching your criteria"**
- **"No agents found matching your criteria"**
- **"Authentication error: Please check your API credentials"**

---

## Rate Limiting

The server implements rate limiting to comply with Bridge Interactive API limits:

- **Default Limit**: 60 requests per minute
- **Configurable**: Set via `API_RATE_LIMIT_PER_MINUTE` environment variable
- **Automatic Throttling**: Requests are automatically queued when limits are approached
- **Error Handling**: Clear messages when rate limits are exceeded

---

## Data Sources and Standards

### Bridge Interactive RESO API
- **Base URL**: `https://api.bridgedataoutput.com/api/v2`
- **Data Standard**: RESO Data Dictionary 2.0 compliant
- **MLS Coverage**: UNLOCK MLS real estate data
- **Authentication**: OAuth2 client credentials flow

### Data Freshness
- **Real-time**: Property data is fetched in real-time from the API
- **No Caching**: Current implementation does not cache responses
- **Update Frequency**: Data reflects the most recent information available in the MLS

### Data Quality
- **Standardized Fields**: All fields follow RESO Data Dictionary 2.0 naming conventions
- **Validated Inputs**: All user inputs are validated before API calls
- **Error Recovery**: Graceful handling of missing or invalid data fields
- **Consistent Formatting**: Addresses, prices, and dates are consistently formatted

---

## Usage Best Practices

### Search Optimization
1. **Start Broad**: Begin with general criteria and refine as needed
2. **Use Natural Language**: Leverage natural language parsing for exploration
3. **Combine Approaches**: Mix natural language queries with specific filters
4. **Iterate**: Refine searches based on initial results

### Market Analysis
1. **Compare Multiple Areas**: Analyze different locations for context
2. **Use Appropriate Time Ranges**: Adjust `days_back` based on market activity
3. **Consider Property Types**: Segment analysis by property type for accuracy
4. **Monitor Trends**: Regular analysis to track market changes

### Agent Search
1. **Local Focus**: Search by location for local market expertise
2. **Check Specializations**: Match agent expertise to your needs
3. **Verify Credentials**: Review licenses and professional designations
4. **Multiple Sources**: Use various criteria to find the best match

This API reference provides complete information for effectively using the UNLOCK MLS MCP Server tools and resources.