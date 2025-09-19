# Coordinate-Based Market Analysis Implementation Plan

## Problem Statement

**Current Limitation**: The MCP server **cannot** answer coordinate-based market analysis questions like "Perform a market analysis within a mile radius of coordinates 30.378052720939845, -97.75102685459593".

The existing `analyze_market` tool only supports:
- City + State: `{"city": "Austin", "state": "TX"}`
- ZIP code: `{"zip_code": "78701"}`

**User Impact**: Questions about market analysis around specific coordinates, addresses, or radius-based searches cannot be answered.

## Research Findings

### ✅ Bridge Interactive API Supports Geospatial Queries

From `/context/bridge-interactive-unlock-api-documentation.md:321`:
```
geo.distance | Search by coordinates | Return listings that are near specific co-ordinates, to a radius of 0.5 miles:
https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=geo.distance(Coordinates, POINT(-118.62 34.22)) lt 0.5
```

**Key Technical Details:**
- Uses `geo.distance(Coordinates, POINT(longitude latitude)) lt radius_in_miles`
- Radius specified in miles (decimal values supported)
- Standard OData geospatial functions supported

### ✅ Property Coordinates Already Available

From `/src/utils/data_mapper.py:111-112`:
```python
# Geographic coordinates
"latitude": self._safe_float(property_data.get("Latitude")),
"longitude": self._safe_float(property_data.get("Longitude")),
```

From `/context/bridge-interactive-property-api-endpoint.md`:
- `Latitude`: Geographic latitude in degrees and decimal parts
- `Longitude`: Geographic longitude in degrees and decimal parts

### ✅ Market Analysis Logic Exists

Current `_analyze_market()` method in `/src/server.py:618-750` provides:
- Active listings statistics (count, average price, median, price/sqft, bedroom distribution)
- Recently sold properties analysis
- Market trend calculations (price direction)
- Professional formatting and insights

**Reusable Components:**
- Property filtering and querying logic
- Statistics calculation methods
- Result formatting and presentation
- Error handling patterns

## Technical Specification

### New Tool Schema

```json
{
  "name": "analyze_market_by_coordinates",
  "description": "Analyze market trends and statistics within a radius of specific coordinates",
  "inputSchema": {
    "type": "object",
    "properties": {
      "latitude": {
        "type": "number",
        "description": "Latitude coordinate (-90 to 90)",
        "minimum": -90,
        "maximum": 90
      },
      "longitude": {
        "type": "number", 
        "description": "Longitude coordinate (-180 to 180)",
        "minimum": -180,
        "maximum": 180
      },
      "radius_miles": {
        "type": "number",
        "description": "Search radius in miles",
        "default": 1.0,
        "minimum": 0.1,
        "maximum": 10.0
      },
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
    "required": ["latitude", "longitude"]
  }
}
```

### Bridge API Integration Pattern

**OData Filter Construction:**
```python
# For coordinates: 30.378052720939845, -97.75102685459593, radius: 1.0 mile
geo_filter = f"geo.distance(Coordinates, POINT({longitude} {latitude})) lt {radius_miles}"

# Combined with other filters:
full_filter = f"StandardStatus eq 'Active' and {geo_filter}"
```

**Example API Request:**
```
https://api.bridgedataoutput.com/api/v2/OData/actris_ref/Property?
$filter=geo.distance(Coordinates, POINT(-97.75102685459593 30.378052720939845)) lt 1.0
&$top=1000
&$orderby=ModificationTimestamp desc
```

### Expected Tool Response Format

```markdown
# Market Analysis - Within 1.0 miles of (30.378, -97.751)

**Coordinates**: 30.378052720939845, -97.75102685459593 (Austin, TX area)
**Search Radius**: 1.0 miles
**Property Type**: All residential
**Analysis Period**: Last 90 days

## Active Listings
- **Total Active**: 45 properties
- **Average Price**: $525,750
- **Median Price**: $485,000
- **Price Range**: $275,000 - $1,250,000
- **Average Price/SqFt**: $285.50
- **Bedroom Distribution**:
  - 2 BR: 8 properties
  - 3 BR: 22 properties
  - 4 BR: 12 properties
  - 5+ BR: 3 properties

## Recently Sold Properties
- **Total Sold**: 28 properties
- **Average Sold Price**: $502,100
- **Median Sold Price**: $475,000
- **Sold Price Range**: $285,000 - $875,000

## Market Insights
- **Price Trend**: Rising (active listings 4.7% higher than recent sales)
- **Inventory Level**: Moderate (45 active listings)
- **Market Activity**: Strong (28 sales in 90 days)
- **Price Stability**: Good price consistency within radius
```

## Implementation Plan

### Phase 1: Core Tool Implementation (2-3 hours)

#### 1.1 Add New MCP Tool (`src/server.py`)

**Location**: Add to `handle_list_tools()` method around line 185

```python
Tool(
    name="analyze_market_by_coordinates",
    description="Analyze market trends and statistics within a radius of specific coordinates",
    inputSchema={
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
                "description": "Latitude coordinate (-90 to 90)",
                "minimum": -90,
                "maximum": 90
            },
            "longitude": {
                "type": "number",
                "description": "Longitude coordinate (-180 to 180)",
                "minimum": -180,
                "maximum": 180
            },
            "radius_miles": {
                "type": "number",
                "description": "Search radius in miles",
                "default": 1.0,
                "minimum": 0.1,
                "maximum": 10.0
            },
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
        "required": ["latitude", "longitude"]
    }
)
```

#### 1.2 Add Tool Handler (`src/server.py`)

**Location**: Add to `handle_call_tool()` method around line 200

```python
elif name == "analyze_market_by_coordinates":
    return await self._analyze_market_by_coordinates(arguments)
```

#### 1.3 Implement Core Method (`src/server.py`)

**Location**: Add new method after `_analyze_market()` around line 750

```python
async def _analyze_market_by_coordinates(self, arguments: Dict[str, Any]) -> list[TextContent]:
    """Analyze market trends within a radius of specific coordinates."""
    try:
        latitude = arguments["latitude"]
        longitude = arguments["longitude"]
        radius_miles = arguments.get("radius_miles", 1.0)
        property_type = arguments.get("property_type")
        days_back = arguments.get("days_back", 90)
        
        logger.info("Analyzing market by coordinates: %f, %f within %f miles", 
                   latitude, longitude, radius_miles)
        
        # Validate coordinates
        if not (-90 <= latitude <= 90):
            raise ValidationError(f"Invalid latitude: {latitude}. Must be between -90 and 90.")
        if not (-180 <= longitude <= 180):
            raise ValidationError(f"Invalid longitude: {longitude}. Must be between -180 and 180.")
        if not (0.1 <= radius_miles <= 10.0):
            raise ValidationError(f"Invalid radius: {radius_miles}. Must be between 0.1 and 10.0 miles.")
        
        # Build coordinate-based filters
        coordinate_filter = {
            "latitude": latitude,
            "longitude": longitude,
            "radius_miles": radius_miles
        }
        
        if property_type:
            coordinate_filter["property_type"] = property_type
        
        # Get active listings
        active_properties = await self.reso_client.query_properties_by_coordinates(
            filters={**coordinate_filter, "status": "active"},
            limit=1000
        )
        
        # Get recently sold properties
        sold_properties = await self.reso_client.query_properties_by_coordinates(
            filters={**coordinate_filter, "status": "sold"},
            limit=1000
        )
        
        # Map properties (reuse existing logic)
        active_mapped = self.data_mapper.map_properties(active_properties)
        sold_mapped = self.data_mapper.map_properties(sold_properties)
        
        # Generate coordinate-based analysis (reuse existing calculation logic)
        location_name = f"Within {radius_miles} miles of ({latitude:.3f}, {longitude:.3f})"
        
        result_text = f"# Market Analysis - {location_name}\n\n"
        result_text += f"**Coordinates**: {latitude}, {longitude}\n"
        result_text += f"**Search Radius**: {radius_miles} miles\n"
        if property_type:
            result_text += f"**Property Type**: {property_type.replace('_', ' ').title()}\n"
        result_text += f"**Analysis Period**: Last {days_back} days\n\n"
        
        # Reuse existing market analysis statistics logic
        # [Similar to existing _analyze_market method lines 668-750]
        
        return [TextContent(type="text", text=result_text)]
        
    except ValidationError:
        raise
    except Exception as e:
        logger.error("Coordinate market analysis error: %s", str(e))
        return [TextContent(type="text", text=f"Error analyzing market by coordinates: {str(e)}")]
```

#### 1.4 Extend RESO Client (`src/reso_client.py`)

**Location**: Add new method after `query_properties()` around line 354

```python
async def query_properties_by_coordinates(self,
                                        filters: Optional[Dict[str, Any]] = None,
                                        select_fields: Optional[List[str]] = None,
                                        order_by: Optional[str] = None,
                                        limit: int = 25,
                                        offset: int = 0) -> List[Dict[str, Any]]:
    """
    Query properties by geographic coordinates and radius.
    
    Args:
        filters: Property filter criteria including coordinate parameters
        select_fields: Fields to select
        order_by: Sort order
        limit: Maximum number of results
        offset: Number of results to skip
        
    Returns:
        List of property records
        
    Raises:
        ResoApiError: If query fails
    """
    logger.info("Querying properties by coordinates with filters: %s", filters)
    
    # Build query parameters
    query_params = {
        "top": min(limit, 200),  # API maximum
        "skip": offset
    }
    
    # Build coordinate-based filter
    if filters:
        filter_str = self._build_coordinate_property_filter(**filters)
    else:
        filter_str = "StandardStatus eq 'Active'"
    
    if filter_str:
        query_params["filter"] = filter_str
    
    # Add field selection
    if select_fields:
        query_params["select"] = select_fields
    
    # Add ordering
    if order_by:
        query_params["orderby"] = order_by
    else:
        query_params["orderby"] = "ModificationTimestamp desc"
    
    # Build query string
    query_string = self._build_odata_query(**query_params)
    url = f"{self.endpoints['Property']}?{query_string}"
    
    async with aiohttp.ClientSession() as session:
        data = await self._make_request(session, "GET", url)
        
        # Extract results from OData response
        if "value" in data:
            results = data["value"]
            logger.info("Retrieved %d properties by coordinates", len(results))
            return results
        else:
            logger.warning("Unexpected response format: %s", data)
            return []

def _build_coordinate_property_filter(self,
                                    latitude: Optional[float] = None,
                                    longitude: Optional[float] = None,
                                    radius_miles: Optional[float] = None,
                                    property_type: Optional[str] = None,
                                    status: Optional[str] = None,
                                    **kwargs) -> str:
    """
    Build a filter string for coordinate-based property queries.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        radius_miles: Search radius in miles
        property_type: Property type
        status: Property status
        **kwargs: Additional filter parameters
        
    Returns:
        OData filter string with geo.distance function
    """
    filters = []
    
    # Always filter to active listings unless status specified
    if status:
        filters.append(f"StandardStatus eq '{status}'")
    else:
        filters.append("StandardStatus eq 'Active'")
    
    # Add coordinate-based filter
    if latitude is not None and longitude is not None and radius_miles is not None:
        # Use Bridge API geo.distance function
        geo_filter = f"geo.distance(Coordinates, POINT({longitude} {latitude})) lt {radius_miles}"
        filters.append(geo_filter)
    
    # Property type filter
    if property_type:
        filters.append(f"PropertyType eq '{property_type}'")
    
    # Additional custom filters (reuse existing logic)
    for key, value in kwargs.items():
        if value is not None and key not in ['latitude', 'longitude', 'radius_miles']:
            if isinstance(value, str):
                filters.append(f"{key} eq '{value}'")
            else:
                filters.append(f"{key} eq {value}")
    
    return " and ".join(filters)
```

### Phase 2: Enhanced Features (1-2 hours)

#### 2.1 Natural Language Parsing (`src/utils/validators.py`)

**Location**: Add new method to `QueryValidator` class

```python
def _extract_coordinate_info(self, query: str) -> Dict[str, Any]:
    """Extract coordinate and radius information from query."""
    filters = {}
    
    # Coordinate patterns
    coordinate_patterns = [
        r'coordinates?\s+([+-]?\d+\.?\d*),\s*([+-]?\d+\.?\d*)',
        r'lat\s*([+-]?\d+\.?\d*)\s*lon\s*([+-]?\d+\.?\d*)',
        r'(\d+\.\d+),\s*(-\d+\.\d+)',  # Typical lat,lng format
    ]
    
    for pattern in coordinate_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            try:
                lat, lng = float(match.group(1)), float(match.group(2))
                if -90 <= lat <= 90 and -180 <= lng <= 180:
                    filters['latitude'] = lat
                    filters['longitude'] = lng
                    break
            except ValueError:
                continue
    
    # Radius patterns
    radius_patterns = [
        r'within\s+(\d+\.?\d*)\s*miles?',
        r'(\d+\.?\d*)\s*mile\s*radius',
        r'radius\s+of\s+(\d+\.?\d*)\s*miles?',
    ]
    
    for pattern in radius_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            try:
                radius = float(match.group(1))
                if 0.1 <= radius <= 10.0:
                    filters['radius_miles'] = radius
                    break
            except ValueError:
                continue
    
    return filters
```

#### 2.2 Update Natural Language Query Parser

**Location**: Modify `parse_natural_language_query()` in `src/utils/validators.py`

```python
# Add coordinate extraction
coordinate_info = self._extract_coordinate_info(query)
filters.update(coordinate_info)
```

#### 2.3 Documentation Updates

**Location**: Update MCP resources in `src/server.py`

Add coordinate search examples to `_get_search_examples()`:
```markdown
### Coordinate-Based Searches
- "market analysis within 1 mile of coordinates 30.378, -97.751"
- "properties within 2 miles of 30.378052720939845, -97.75102685459593"
- "analyze market within 0.5 mile radius of lat 30.378 lon -97.751"
```

Add new guided workflow to `_get_guided_analysis_prompts()`:
```markdown
### Scenario: Coordinate-Based Market Analysis
**Goal**: Analyze market around specific coordinates or addresses

**Step 1**: Use coordinate-based analysis
```
{
  "latitude": 30.378052720939845,
  "longitude": -97.75102685459593,
  "radius_miles": 1.0,
  "property_type": "residential",
  "days_back": 90
}
```
```

### Phase 3: Testing & Validation (1 hour)

#### 3.1 Test Cases

```python
test_cases = [
    # Austin, TX University area
    {
        "latitude": 30.378052720939845,
        "longitude": -97.75102685459593,
        "radius_miles": 1.0,
        "expected": "Valid coordinate search"
    },
    # Invalid coordinates
    {
        "latitude": 91.0,  # Invalid latitude
        "longitude": -97.751,
        "radius_miles": 1.0,
        "expected": "ValidationError: Invalid latitude"
    },
    # Invalid radius
    {
        "latitude": 30.378,
        "longitude": -97.751,
        "radius_miles": 15.0,  # Too large
        "expected": "ValidationError: Invalid radius"
    }
]
```

#### 3.2 Integration Testing

1. **Bridge API Validation**: Test `geo.distance` query construction
2. **Market Analysis Logic**: Verify statistics calculation with coordinate results
3. **Natural Language**: Test coordinate extraction from various query formats
4. **Error Handling**: Validate coordinate and radius boundary checks

## Example Implementation Usage

### Direct Tool Call
```json
{
  "tool": "analyze_market_by_coordinates",
  "arguments": {
    "latitude": 30.378052720939845,
    "longitude": -97.75102685459593,
    "radius_miles": 1.0,
    "property_type": "residential",
    "days_back": 90
  }
}
```

### Natural Language Query
```
"Analyze the residential market within 1 mile of coordinates 30.378052720939845, -97.75102685459593"
```

### Expected Bridge API Call
```
GET /api/v2/OData/actris_ref/Property?$filter=StandardStatus eq 'Active' and geo.distance(Coordinates, POINT(-97.75102685459593 30.378052720939845)) lt 1.0 and PropertyType eq 'residential'&$top=1000&$orderby=ModificationTimestamp desc
```

## Technical Considerations

### Performance
- **API Rate Limits**: Geospatial queries may be more expensive than regular filters
- **Large Radius Impact**: Searches over 5 miles may return many results, affecting performance
- **Caching Strategy**: Consider caching coordinate-based results for repeated queries

### Data Quality
- **Coordinate Accuracy**: Not all properties may have precise coordinates
- **Missing Data**: Handle properties without Latitude/Longitude gracefully
- **Boundary Cases**: Properties exactly at radius boundary may be inconsistent

### User Experience
- **Coordinate Validation**: Provide clear error messages for invalid coordinates
- **Radius Guidance**: Suggest optimal radius ranges for different analysis needs
- **Location Context**: Where possible, provide city/neighborhood context for coordinates

## Future Enhancements

### Phase 4: Advanced Features (Future)
1. **Address Geocoding**: Convert addresses to coordinates using geocoding service
2. **Multiple Points**: Support analysis around multiple coordinate points
3. **Polygon Searches**: Use `geo.intersects` for custom area definitions
4. **Coordinate Clustering**: Group nearby properties for analysis
5. **Distance Calculations**: Show distance from center point in results

### Integration Opportunities
1. **Map Visualization**: Generate map links or embed coordinates in responses
2. **Walking Distance**: Consider walkability analysis within radius
3. **School Districts**: Overlay school district boundaries with coordinate searches
4. **Transportation**: Include transit stops and major roads in analysis

## Success Metrics

### Immediate Success
- ✅ Tool successfully handles coordinate-based market analysis requests
- ✅ Bridge API geo.distance queries work correctly
- ✅ Market statistics calculated accurately for coordinate results
- ✅ Input validation prevents invalid coordinate/radius combinations

### User Experience Success
- ✅ Natural language queries with coordinates parsed correctly
- ✅ Clear error messages for invalid inputs
- ✅ Response format consistent with existing market analysis tools
- ✅ Performance acceptable for typical radius searches (< 5 seconds)

### Technical Success
- ✅ Code follows existing patterns and conventions
- ✅ Error handling robust for API failures and edge cases
- ✅ Documentation updated with coordinate search examples
- ✅ Integration tests validate geospatial functionality

This implementation plan provides the complete roadmap for adding coordinate-based market analysis capability to the UNLOCK MLS RESO Reference MCP Server.