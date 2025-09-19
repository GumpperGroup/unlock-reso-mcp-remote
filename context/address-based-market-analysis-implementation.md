# Address-Based Market Analysis Implementation Plan

## Problem Statement

**Current Limitation**: The MCP server **cannot** perform market analysis based on a specific property address like "8604 Dorotha Ct, Austin, TX 78759".

**Current Tools Available:**
- `analyze_market`: Only supports city/state or ZIP code
- `search_properties`: Supports location but not specific addresses
- No address parsing or geocoding capabilities

**User Impact**: Questions about market analysis around specific property addresses cannot be answered directly.

## Research Findings

### ✅ Bridge Interactive API Supports Address Searches

From `/context/bridge-interactive-unlock-api-documentation.md:340-341`:
```
Search for a property by address:
$filter=UnparsedAddress eq '123 Main'

Case-insensitive search:  
$filter=tolower(UnparsedAddress) eq '123 main'
```

### ✅ RESO Address Fields Available

From Bridge Interactive Property API endpoint documentation:
- **`UnparsedAddress`**: Full civic address as single entity (e.g., "8604 Dorotha Ct, Austin, TX 78759")
- **`StreetNumber`**: Street number portion (e.g., "8604")
- **`StreetName`**: Street name portion (e.g., "Dorotha")
- **`StreetSuffix`**: Street suffix (e.g., "Ct")
- **`StreetDirPrefix`**: Direction prefix (e.g., "N", "S")
- **`StreetDirSuffix`**: Direction suffix
- **`City`**: City name
- **`StateOrProvince`**: State code
- **`PostalCode`**: ZIP code

### ✅ Property Coordinates Available

Properties include `Latitude` and `Longitude` fields that can be used for radius-based market analysis around the target address.

### ✅ Address Data Already Mapped

From `/src/utils/data_mapper.py:103,178-207`: Properties already include formatted addresses in output through `_format_address()` method.

## Implementation Strategy: Hybrid Approach

**Core Concept**: Find the target property by address, extract its coordinates, then perform radius-based market analysis around that location.

### Workflow:
1. **Find Target Property**: Search by `UnparsedAddress` to locate the specific property
2. **Extract Coordinates**: Get `Latitude` and `Longitude` from the target property
3. **Radius Analysis**: Use coordinates for market analysis within specified radius
4. **Fallback Strategy**: Use ZIP code analysis if target property not found or lacks coordinates

## Technical Implementation Plan

### Phase 1: Core Address Search Capability (1 hour)

#### 1.1 Extend RESO Client for Address Search

**Location**: Add method to `/src/reso_client.py` after `query_properties()`

```python
async def find_property_by_address(self, address: str) -> Optional[Dict[str, Any]]:
    """
    Find a specific property by its address.
    
    Args:
        address: Full property address
        
    Returns:
        Property record or None if not found
    """
    logger.info("Finding property by address: %s", address)
    
    try:
        # Use case-insensitive search for better matching
        results = await self.query_properties(
            filters={"UnparsedAddress": address},
            limit=5  # Get a few results in case of variations
        )
        
        if results:
            # Return the first match
            return results[0]
        else:
            # Try with lowercase for case-insensitive matching
            results = await self.query_properties_raw(
                filter_str=f"tolower(UnparsedAddress) eq '{address.lower()}'",
                limit=5
            )
            return results[0] if results else None
            
    except Exception as e:
        logger.error("Error finding property by address: %s", str(e))
        return None

async def query_properties_raw(self, filter_str: str, limit: int = 25) -> List[Dict[str, Any]]:
    """
    Query properties using raw OData filter string.
    
    Args:
        filter_str: Raw OData filter expression
        limit: Maximum number of results
        
    Returns:
        List of property records
    """
    query_params = {
        "filter": filter_str,
        "top": min(limit, 200),
        "orderby": "ModificationTimestamp desc"
    }
    
    query_string = self._build_odata_query(**query_params)
    url = f"{self.endpoints['Property']}?{query_string}"
    
    async with aiohttp.ClientSession() as session:
        data = await self._make_request(session, "GET", url)
        return data.get("value", [])
```

#### 1.2 Add Address Filter Support

**Location**: Extend `_build_property_filter()` in `/src/reso_client.py` around line 275

```python
# Add after line 273 (listing_id filter)
# Address filter
if kwargs.get("UnparsedAddress"):
    address = kwargs["UnparsedAddress"]
    # Use case-insensitive matching for addresses
    filters.append(f"tolower(UnparsedAddress) eq '{address.lower()}'")
```

### Phase 2: Address-Based Market Analysis Tool (2 hours)

#### 2.1 Add New MCP Tool

**Location**: Add to `handle_list_tools()` in `/src/server.py` around line 185

```python
Tool(
    name="analyze_market_by_address",
    description="Analyze market trends around a specific property address",
    inputSchema={
        "type": "object",
        "properties": {
            "address": {
                "type": "string",
                "description": "Full property address (e.g., '8604 Dorotha Ct, Austin, TX 78759')"
            },
            "radius_miles": {
                "type": "number",
                "description": "Analysis radius around the address in miles",
                "default": 1.0,
                "minimum": 0.1,
                "maximum": 5.0
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
        "required": ["address"]
    }
)
```

#### 2.2 Add Tool Handler

**Location**: Add to `handle_call_tool()` in `/src/server.py` around line 200

```python
elif name == "analyze_market_by_address":
    return await self._analyze_market_by_address(arguments)
```

#### 2.3 Implement Core Analysis Method

**Location**: Add new method to `/src/server.py` after `_analyze_market()`

```python
async def _analyze_market_by_address(self, arguments: Dict[str, Any]) -> list[TextContent]:
    """Analyze market trends around a specific property address."""
    try:
        address = arguments["address"]
        radius_miles = arguments.get("radius_miles", 1.0)
        property_type = arguments.get("property_type")
        days_back = arguments.get("days_back", 90)
        
        logger.info("Analyzing market by address: %s within %f miles", address, radius_miles)
        
        # Step 1: Find the target property by address
        target_property = await self.reso_client.find_property_by_address(address)
        
        if not target_property:
            # Fallback: Extract ZIP code and do ZIP-based analysis
            zip_code = self._extract_zip_from_address(address)
            if zip_code:
                logger.info("Property not found by address, falling back to ZIP analysis: %s", zip_code)
                return await self._analyze_market({
                    "zip_code": zip_code,
                    "property_type": property_type,
                    "days_back": days_back
                })
            else:
                return [TextContent(type="text", text=f"Could not find property at address '{address}' or extract location for analysis.")]
        
        # Step 2: Extract coordinates from target property
        latitude = target_property.get("Latitude")
        longitude = target_property.get("Longitude")
        
        # Map target property for display
        target_mapped = self.data_mapper.map_property(target_property)
        
        if latitude and longitude:
            # Step 3: Use coordinate-based analysis around target property
            logger.info("Using coordinates from target property: %f, %f", latitude, longitude)
            
            # Build coordinate-based filters
            coordinate_filter = {
                "latitude": latitude,
                "longitude": longitude,
                "radius_miles": radius_miles
            }
            
            if property_type:
                coordinate_filter["property_type"] = property_type
            
            # Get active listings around the address
            active_properties = await self.reso_client.query_properties_by_coordinates(
                filters={**coordinate_filter, "status": "active"},
                limit=1000
            )
            
            # Get recently sold properties around the address
            sold_properties = await self.reso_client.query_properties_by_coordinates(
                filters={**coordinate_filter, "status": "sold"},
                limit=1000
            )
            
            # Map properties
            active_mapped = self.data_mapper.map_properties(active_properties)
            sold_mapped = self.data_mapper.map_properties(sold_properties)
            
            # Generate analysis with target property context
            result_text = f"# Market Analysis - Around {address}\n\n"
            result_text += f"**Target Address**: {address}\n"
            result_text += f"**Analysis Radius**: {radius_miles} miles around target property\n"
            if property_type:
                result_text += f"**Property Type**: {property_type.replace('_', ' ').title()}\n"
            result_text += f"**Analysis Period**: Last {days_back} days\n\n"
            
            # Add target property details
            result_text += "## Target Property Details\n"
            result_text += f"- **Status**: {target_mapped.get('status', 'N/A').replace('_', ' ').title()}\n"
            if target_mapped.get("list_price"):
                result_text += f"- **List Price**: ${target_mapped['list_price']:,}\n"
            if target_mapped.get("sold_price"):
                result_text += f"- **Sold Price**: ${target_mapped['sold_price']:,}\n"
            result_text += f"- **Property Type**: {target_mapped.get('property_type', 'N/A').replace('_', ' ').title()}\n"
            if target_mapped.get("bedrooms"):
                result_text += f"- **Bedrooms**: {target_mapped['bedrooms']}\n"
            if target_mapped.get("bathrooms"):
                result_text += f"- **Bathrooms**: {target_mapped['bathrooms']}\n"
            if target_mapped.get("square_feet"):
                result_text += f"- **Square Feet**: {target_mapped['square_feet']:,}\n"
            if target_mapped.get("year_built"):
                result_text += f"- **Year Built**: {target_mapped['year_built']}\n"
            
            result_text += f"\n## Market Analysis Within {radius_miles} Miles\n"
            
            # Active listings analysis (reuse existing logic from _analyze_market)
            result_text += f"### Active Listings\n"
            result_text += f"- **Total Active**: {len(active_mapped)} properties\n"
            
            if active_mapped:
                prices = [p["list_price"] for p in active_mapped if p.get("list_price")]
                if prices:
                    result_text += f"- **Average Price**: ${sum(prices) // len(prices):,}\n"
                    result_text += f"- **Median Price**: ${sorted(prices)[len(prices)//2]:,}\n"
                    result_text += f"- **Price Range**: ${min(prices):,} - ${max(prices):,}\n"
                
                sqft_data = [(p["square_feet"], p["list_price"]) for p in active_mapped 
                            if p.get("square_feet") and p.get("list_price")]
                if sqft_data:
                    avg_price_per_sqft = sum(price/sqft for sqft, price in sqft_data) / len(sqft_data)
                    result_text += f"- **Average Price/SqFt**: ${avg_price_per_sqft:.2f}\n"
            
            # Recently sold analysis
            result_text += f"\n### Recently Sold Properties\n"
            result_text += f"- **Total Sold**: {len(sold_mapped)} properties\n"
            
            if sold_mapped:
                sold_prices = [p["sold_price"] for p in sold_mapped if p.get("sold_price")]
                if sold_prices:
                    result_text += f"- **Average Sold Price**: ${sum(sold_prices) // len(sold_prices):,}\n"
                    result_text += f"- **Median Sold Price**: ${sorted(sold_prices)[len(sold_prices)//2]:,}\n"
                    result_text += f"- **Sold Price Range**: ${min(sold_prices):,} - ${max(sold_prices):,}\n"
            
            # Market insights
            result_text += f"\n### Market Insights\n"
            if active_mapped and sold_mapped:
                active_avg = sum(p["list_price"] for p in active_mapped if p.get("list_price")) / len([p for p in active_mapped if p.get("list_price")])
                sold_avg = sum(p["sold_price"] for p in sold_mapped if p.get("sold_price")) / len([p for p in sold_mapped if p.get("sold_price")])
                
                if active_avg and sold_avg:
                    price_trend = ((active_avg - sold_avg) / sold_avg) * 100
                    if price_trend > 5:
                        result_text += f"- **Price Trend**: Rising (active listings {price_trend:.1f}% higher than recent sales)\n"
                    elif price_trend < -5:
                        result_text += f"- **Price Trend**: Declining (active listings {abs(price_trend):.1f}% lower than recent sales)\n"
                    else:
                        result_text += f"- **Price Trend**: Stable (active listings within 5% of recent sales)\n"
            
            result_text += f"- **Location**: Centered on {address}\n"
            result_text += f"- **Search Area**: {radius_miles}-mile radius covers approximately {3.14159 * radius_miles * radius_miles:.1f} square miles\n"
            
            return [TextContent(type="text", text=result_text)]
            
        else:
            # Fallback to ZIP-based analysis
            zip_code = target_property.get("PostalCode")
            if zip_code:
                logger.info("No coordinates available, falling back to ZIP analysis: %s", zip_code)
                result = await self._analyze_market({
                    "zip_code": zip_code,
                    "property_type": property_type,
                    "days_back": days_back
                })
                
                # Prepend target property information
                target_info = f"# Market Analysis - Around {address}\n\n"
                target_info += f"**Target Address**: {address}\n"
                target_info += f"**Fallback Analysis**: Using ZIP code {zip_code} (coordinates not available)\n\n"
                
                # Modify the result to include target context
                original_text = result[0].text
                modified_text = target_info + original_text.replace("# Market Analysis -", "## ZIP Code Analysis -")
                
                return [TextContent(type="text", text=modified_text)]
            else:
                return [TextContent(type="text", text=f"Found property at '{address}' but could not determine location for market analysis.")]
                
    except ValidationError:
        raise
    except Exception as e:
        logger.error("Address market analysis error: %s", str(e))
        return [TextContent(type="text", text=f"Error analyzing market by address: {str(e)}")]

def _extract_zip_from_address(self, address: str) -> Optional[str]:
    """Extract ZIP code from address string."""
    import re
    
    # Look for 5-digit ZIP codes at the end of the address
    zip_pattern = r'\b(\d{5})\b'
    match = re.search(zip_pattern, address)
    if match:
        return match.group(1)
    
    # Look for ZIP+4 format and extract just the 5-digit part
    zip_plus4_pattern = r'\b(\d{5})-\d{4}\b'
    match = re.search(zip_plus4_pattern, address)
    if match:
        return match.group(1)
    
    return None
```

### Phase 3: Natural Language Address Parsing (1 hour)

#### 3.1 Add Address Extraction to Validator

**Location**: Add method to `/src/utils/validators.py` in `QueryValidator` class

```python
def _extract_address_info(self, query: str) -> Dict[str, str]:
    """Extract address information from natural language queries."""
    filters = {}
    
    # Address patterns - look for full addresses
    address_patterns = [
        # "market analysis for 8604 Dorotha Ct, Austin, TX 78759"
        r'(?:for|at|near|around)\s+(.+?(?:\d{5}(?:-\d{4})?|\w{2}\s+\d{5}(?:-\d{4})?))',
        # "8604 Dorotha Ct, Austin, TX 78759"
        r'(\d+\s+[A-Za-z\s]+(?:St|Ave|Ct|Dr|Ln|Rd|Way|Blvd|Street|Avenue|Court|Drive|Lane|Road|Boulevard)[,\s]+[A-Za-z\s]+[,\s]+[A-Z]{2}(?:\s+\d{5}(?:-\d{4})?)?)',
        # "123 Main Street, Austin TX"
        r'(\d+\s+[A-Za-z\s]+[,\s]+[A-Za-z\s]+[,\s]+[A-Z]{2})',
    ]
    
    for pattern in address_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            address = match.group(1).strip()
            # Clean up the address
            address = re.sub(r'\s+', ' ', address)  # Normalize whitespace
            address = address.rstrip(',. ')  # Remove trailing punctuation
            filters['address'] = address
            break
    
    return filters
```

#### 3.2 Update Natural Language Parser

**Location**: Modify `parse_natural_language_query()` in `/src/utils/validators.py`

```python
# Add address extraction (insert after neighborhood extraction)
address_info = self._extract_address_info(query)
filters.update(address_info)
```

### Phase 4: Documentation Updates (30 minutes)

#### 4.1 Add Address Search Examples

**Location**: Update `_get_search_examples()` in `/src/server.py`

```markdown
### Address-Based Market Analysis
- "analyze market for 8604 Dorotha Ct, Austin, TX 78759"
- "market analysis around 123 Main Street, Dallas TX 75201"
- "what's the market like near 456 Oak Ave, Houston, TX 77001"
- "market trends within 2 miles of 789 Pine St, San Antonio TX 78205"
```

#### 4.2 Add Guided Workflow

**Location**: Update `_get_guided_analysis_prompts()` in `/src/server.py`

```markdown
### Scenario: Address-Based Market Analysis
**Goal**: Analyze market around a specific property address

**Step 1**: Use address-based analysis
```
{
  "address": "8604 Dorotha Ct, Austin, TX 78759",
  "radius_miles": 1.0,
  "property_type": "residential",
  "days_back": 90
}
```

**Step 2**: Review target property details
- Property status, price, and characteristics
- Coordinates for radius-based analysis

**Step 3**: Analyze surrounding market
- Active listings within radius
- Recent sales activity
- Price trends and market insights
```

## Example Usage

### Direct Tool Call
```json
{
  "tool": "analyze_market_by_address",
  "arguments": {
    "address": "8604 Dorotha Ct, Austin, TX 78759",
    "radius_miles": 1.0,
    "property_type": "residential",
    "days_back": 90
  }
}
```

### Natural Language Query
```
"Analyze the market for 8604 Dorotha Ct, Austin, TX 78759"
"What's the market like around 8604 Dorotha Ct within 2 miles?"
"Market analysis near 8604 Dorotha Ct, Austin, TX"
```

### Expected API Calls
```
1. Find target property:
   GET /Property?$filter=tolower(UnparsedAddress) eq '8604 dorotha ct, austin, tx 78759'

2. Market analysis around coordinates:
   GET /Property?$filter=StandardStatus eq 'Active' and geo.distance(Coordinates, POINT(-97.751 30.378)) lt 1.0
```

## Expected Response Format

```markdown
# Market Analysis - Around 8604 Dorotha Ct, Austin, TX 78759

**Target Address**: 8604 Dorotha Ct, Austin, TX 78759
**Analysis Radius**: 1.0 miles around target property
**Property Type**: All residential
**Analysis Period**: Last 90 days

## Target Property Details
- **Status**: Active
- **List Price**: $545,000
- **Property Type**: Single Family
- **Bedrooms**: 4
- **Bathrooms**: 3
- **Square Feet**: 2,456
- **Year Built**: 2018

## Market Analysis Within 1.0 Miles

### Active Listings
- **Total Active**: 23 properties
- **Average Price**: $512,750
- **Median Price**: $485,000
- **Price Range**: $325,000 - $875,000
- **Average Price/SqFt**: $298.50

### Recently Sold Properties
- **Total Sold**: 18 properties
- **Average Sold Price**: $495,200
- **Median Sold Price**: $475,000
- **Sold Price Range**: $310,000 - $795,000

### Market Insights
- **Price Trend**: Rising (active listings 3.5% higher than recent sales)
- **Location**: Centered on 8604 Dorotha Ct, Austin, TX 78759
- **Search Area**: 1.0-mile radius covers approximately 3.1 square miles
```

## Technical Considerations

### Address Matching Strategy
1. **Primary**: Exact `UnparsedAddress` match
2. **Secondary**: Case-insensitive match using `tolower()`
3. **Tertiary**: Partial address matching (street number + name)

### Fallback Hierarchy
1. **Best**: Target property found → use coordinates for radius analysis
2. **Good**: Target property not found → extract ZIP code → ZIP-based analysis
3. **Basic**: ZIP not extractable → extract city/state → city-based analysis
4. **Error**: No location extractable → return error message

### Error Handling
- **Address not found**: Clear message with suggested alternatives
- **No coordinates**: Graceful fallback to ZIP or city analysis
- **Invalid radius**: Validation with helpful limits
- **API errors**: Robust error handling with user-friendly messages

### Performance Optimization
- **Limit searches**: Use reasonable limits for target property search
- **Cache results**: Consider caching for repeated address queries
- **Parallel requests**: Query active and sold properties simultaneously

## Success Metrics

### Immediate Success
- ✅ Tool finds properties by full address using `UnparsedAddress`
- ✅ Extracts coordinates from target property for radius analysis
- ✅ Provides market analysis around specific addresses
- ✅ Graceful fallback when target property not found

### User Experience Success
- ✅ Natural language queries with addresses parsed correctly
- ✅ Clear target property context in analysis results
- ✅ Helpful error messages for address issues
- ✅ Consistent response format with existing tools

### Technical Success
- ✅ Integration with existing coordinate-based analysis
- ✅ Proper address parsing and validation
- ✅ Robust error handling and fallback strategies
- ✅ Documentation updated with address examples

## Future Enhancements

### Phase 5: Advanced Features (Future)
1. **Address Normalization**: Standardize address formats for better matching
2. **Partial Address Matching**: Support incomplete addresses with intelligent suggestions
3. **Multiple Property Analysis**: Analyze market around multiple addresses simultaneously
4. **Historical Analysis**: Track market changes around specific addresses over time
5. **Comparable Properties**: Find similar properties within radius for CMA analysis

This implementation plan provides the complete roadmap for adding address-based market analysis capability to the UNLOCK MLS RESO Reference MCP Server, enabling users to perform market analysis around specific property addresses.