"""MCP server implementation for UNLOCK MLS RESO data access."""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    CallToolResult,
    ListResourcesResult,
    ListToolsResult,
    ReadResourceResult,
)

from .auth.oauth2 import OAuth2Handler
from .reso_client import ResoWebApiClient
from .utils.data_mapper import ResoDataMapper
from .utils.validators import QueryValidator, ValidationError
from .config.settings import get_settings
from .config.logging_config import setup_logging

logger = setup_logging(__name__)

class UnlockMlsServer:
    """MCP server for UNLOCK MLS RESO data access."""
    
    def __init__(self):
        """Initialize the MCP server."""
        self.settings = get_settings()
        self.oauth_handler = OAuth2Handler(self.settings)
        self.reso_client = ResoWebApiClient(self.settings, self.oauth_handler)
        self.data_mapper = ResoDataMapper()
        self.query_validator = QueryValidator()
        
        # Create MCP server instance
        self.server = Server("unlock-mls-mcp")
        self._setup_handlers()
        
        logger.info("UnlockMlsServer initialized")
    
    def _setup_handlers(self):
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available MCP tools."""
            tools = [
                Tool(
                    name="search_properties",
                    description="Search for properties using natural language or specific criteria",
                    inputSchema={
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
                ),
                Tool(
                    name="get_property_details",
                    description="Get comprehensive details for a specific property",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "listing_id": {
                                "type": "string",
                                "description": "Property listing ID"
                            }
                        },
                        "required": ["listing_id"]
                    }
                ),
                Tool(
                    name="analyze_market",
                    description="Analyze market trends and statistics for a location",
                    inputSchema={
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
                ),
                Tool(
                    name="find_agent",
                    description="Find real estate agents or members",
                    inputSchema={
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
                )
            ]
            
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls."""
            try:
                if name == "search_properties":
                    return await self._search_properties(arguments)
                elif name == "get_property_details":
                    return await self._get_property_details(arguments)
                elif name == "analyze_market":
                    return await self._analyze_market(arguments)
                elif name == "find_agent":
                    return await self._find_agent(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except ValidationError as e:
                logger.warning("Validation error in %s: %s", name, e)
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Validation error: {str(e)}")]
                )
            except Exception as e:
                logger.error("Error in %s: %s", name, e, exc_info=True)
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")]
                )
        
        @self.server.list_resources()
        async def handle_list_resources() -> ListResourcesResult:
            """List available MCP resources."""
            resources = [
                Resource(
                    uri="property://search/examples",
                    name="Property Search Examples",
                    description="Common property search query examples",
                    mimeType="text/markdown"
                ),
                Resource(
                    uri="property://types/reference",
                    name="Property Types Reference",
                    description="Reference guide for property types and statuses",
                    mimeType="text/markdown"
                ),
                Resource(
                    uri="market://analysis/guide",
                    name="Market Analysis Guide",
                    description="Guide for understanding market analysis data",
                    mimeType="text/markdown"
                )
            ]
            
            return ListResourcesResult(resources=resources)
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """Get resource content."""
            if uri == "property://search/examples":
                content = self._get_search_examples()
            elif uri == "property://types/reference":
                content = self._get_property_types_reference()
            elif uri == "market://analysis/guide":
                content = self._get_market_analysis_guide()
            else:
                raise ValueError(f"Unknown resource: {uri}")
            
            return ReadResourceResult(
                contents=[TextContent(type="text", text=content)]
            )
    
    async def _search_properties(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Search for properties."""
        query = arguments.get("query")
        filters = arguments.get("filters", {})
        limit = arguments.get("limit", 25)
        
        # Parse natural language query if provided
        if query:
            parsed_filters = self.query_validator.parse_natural_language_query(query)
            # Merge with explicit filters (explicit takes precedence)
            parsed_filters.update(filters)
            filters = parsed_filters
        
        # Validate filters
        if filters:
            filters = self.query_validator.validate_search_filters(filters)
        
        logger.info("Searching properties with filters: %s", filters)
        
        # Search properties
        properties = await self.reso_client.query_properties(
            filters=filters,
            limit=limit
        )
        
        if not properties:
            return CallToolResult(
                content=[TextContent(type="text", text="No properties found matching your criteria.")]
            )
        
        # Map properties to standardized format
        mapped_properties = self.data_mapper.map_properties(properties)
        
        # Format results
        result_text = f"Found {len(mapped_properties)} properties:\n\n"
        
        for i, prop in enumerate(mapped_properties[:limit], 1):
            summary = self.data_mapper.get_property_summary(prop)
            result_text += f"{i}. **{prop.get('listing_id', 'N/A')}** - {summary}\n"
            
            if prop.get("address"):
                result_text += f"   📍 {prop['address']}\n"
            
            if prop.get("remarks"):
                # Truncate remarks to first 100 characters
                remarks = prop["remarks"][:100] + "..." if len(prop["remarks"]) > 100 else prop["remarks"]
                result_text += f"   💬 {remarks}\n"
            
            result_text += "\n"
        
        # Add search summary
        result_text += f"\n**Search Summary:**\n"
        if query:
            result_text += f"- Query: {query}\n"
        if filters:
            filter_summary = []
            for key, value in filters.items():
                if key.startswith(('min_', 'max_')):
                    filter_summary.append(f"{key.replace('_', ' ')}: {value:,}" if isinstance(value, int) else f"{key.replace('_', ' ')}: {value}")
                else:
                    filter_summary.append(f"{key.replace('_', ' ')}: {value}")
            result_text += f"- Filters: {', '.join(filter_summary)}\n"
        result_text += f"- Results: {len(mapped_properties)} properties\n"
        
        return CallToolResult(
            content=[TextContent(type="text", text=result_text)]
        )
    
    async def _get_property_details(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get detailed property information."""
        listing_id = arguments["listing_id"]
        
        logger.info("Getting property details for listing: %s", listing_id)
        
        # Get property details
        properties = await self.reso_client.query_properties(
            filters={"listing_id": listing_id},
            limit=1
        )
        
        if not properties:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Property with listing ID '{listing_id}' not found.")]
            )
        
        # Map property to standardized format
        property_data = self.data_mapper.map_property(properties[0])
        
        # Format detailed property information
        result_text = f"# Property Details - {property_data.get('listing_id', 'N/A')}\n\n"
        
        # Basic information
        result_text += "## Basic Information\n"
        result_text += f"- **Status**: {property_data.get('status', 'N/A').replace('_', ' ').title()}\n"
        result_text += f"- **Property Type**: {property_data.get('property_type', 'N/A').replace('_', ' ').title()}\n"
        if property_data.get("property_subtype"):
            result_text += f"- **Property Subtype**: {property_data['property_subtype']}\n"
        
        # Pricing
        result_text += "\n## Pricing\n"
        if property_data.get("list_price"):
            result_text += f"- **List Price**: ${property_data['list_price']:,}\n"
        if property_data.get("original_list_price"):
            result_text += f"- **Original List Price**: ${property_data['original_list_price']:,}\n"
        if property_data.get("sold_price"):
            result_text += f"- **Sold Price**: ${property_data['sold_price']:,}\n"
        
        # Property details
        result_text += "\n## Property Details\n"
        if property_data.get("bedrooms"):
            result_text += f"- **Bedrooms**: {property_data['bedrooms']}\n"
        if property_data.get("bathrooms"):
            result_text += f"- **Bathrooms**: {property_data['bathrooms']}\n"
        if property_data.get("full_bathrooms") or property_data.get("half_bathrooms"):
            result_text += f"- **Full/Half Baths**: {property_data.get('full_bathrooms', 0)}/{property_data.get('half_bathrooms', 0)}\n"
        if property_data.get("square_feet"):
            result_text += f"- **Living Area**: {property_data['square_feet']:,} sq ft\n"
        if property_data.get("lot_size"):
            result_text += f"- **Lot Size**: {property_data['lot_size']} acres\n"
        if property_data.get("lot_size_sqft"):
            result_text += f"- **Lot Size**: {property_data['lot_size_sqft']:,} sq ft\n"
        if property_data.get("year_built"):
            result_text += f"- **Year Built**: {property_data['year_built']}\n"
        if property_data.get("stories"):
            result_text += f"- **Stories**: {property_data['stories']}\n"
        if property_data.get("garage_spaces"):
            result_text += f"- **Garage Spaces**: {property_data['garage_spaces']}\n"
        
        # Location
        result_text += "\n## Location\n"
        if property_data.get("address"):
            result_text += f"- **Address**: {property_data['address']}\n"
        result_text += f"- **City**: {property_data.get('city', 'N/A')}\n"
        result_text += f"- **State**: {property_data.get('state', 'N/A')}\n"
        result_text += f"- **ZIP Code**: {property_data.get('zip_code', 'N/A')}\n"
        if property_data.get("county"):
            result_text += f"- **County**: {property_data['county']}\n"
        if property_data.get("subdivision"):
            result_text += f"- **Subdivision**: {property_data['subdivision']}\n"
        
        # Features
        features = []
        if property_data.get("pool"):
            features.append("Pool")
        if property_data.get("fireplace"):
            features.append("Fireplace")
        if property_data.get("waterfront"):
            features.append("Waterfront")
        if features:
            result_text += f"\n## Features\n"
            result_text += f"- {', '.join(features)}\n"
        
        if property_data.get("view"):
            result_text += f"- **View**: {property_data['view']}\n"
        
        # Schools
        schools = []
        if property_data.get("elementary_school"):
            schools.append(f"Elementary: {property_data['elementary_school']}")
        if property_data.get("middle_school"):
            schools.append(f"Middle: {property_data['middle_school']}")
        if property_data.get("high_school"):
            schools.append(f"High: {property_data['high_school']}")
        
        if schools:
            result_text += f"\n## Schools\n"
            for school in schools:
                result_text += f"- {school}\n"
        
        # Dates
        result_text += "\n## Important Dates\n"
        if property_data.get("list_date"):
            result_text += f"- **Listed**: {property_data['list_date']}\n"
        if property_data.get("sold_date"):
            result_text += f"- **Sold**: {property_data['sold_date']}\n"
        if property_data.get("contract_date"):
            result_text += f"- **Under Contract**: {property_data['contract_date']}\n"
        if property_data.get("modification_date"):
            result_text += f"- **Last Modified**: {property_data['modification_date']}\n"
        
        # Agent information
        if property_data.get("listing_agent_name") or property_data.get("listing_office"):
            result_text += "\n## Listing Information\n"
            if property_data.get("listing_agent_name"):
                result_text += f"- **Listing Agent**: {property_data['listing_agent_name']}\n"
            if property_data.get("listing_office"):
                result_text += f"- **Listing Office**: {property_data['listing_office']}\n"
            if property_data.get("listing_agent_phone"):
                result_text += f"- **Phone**: {property_data['listing_agent_phone']}\n"
            if property_data.get("listing_agent_email"):
                result_text += f"- **Email**: {property_data['listing_agent_email']}\n"
        
        # Remarks
        if property_data.get("remarks"):
            result_text += f"\n## Description\n{property_data['remarks']}\n"
        
        if property_data.get("showing_instructions"):
            result_text += f"\n## Showing Instructions\n{property_data['showing_instructions']}\n"
        
        return CallToolResult(
            content=[TextContent(type="text", text=result_text)]
        )
    
    async def _analyze_market(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Analyze market trends and statistics."""
        city = arguments.get("city")
        state = arguments.get("state")
        zip_code = arguments.get("zip_code")
        property_type = arguments.get("property_type", "residential")
        days_back = arguments.get("days_back", 90)
        
        logger.info("Analyzing market for location: %s %s %s", city, state, zip_code)
        
        # Build location filter
        location_filter = {}
        if city:
            location_filter["city"] = city
        if state:
            location_filter["state"] = state
        if zip_code:
            location_filter["zip_code"] = zip_code
        
        location_filter["property_type"] = property_type
        
        # Get active listings
        active_properties = await self.reso_client.query_properties(
            filters={**location_filter, "status": "active"},
            limit=1000
        )
        
        # Get recently sold properties
        sold_properties = await self.reso_client.query_properties(
            filters={**location_filter, "status": "sold"},
            limit=1000
        )
        
        # Map properties
        active_mapped = self.data_mapper.map_properties(active_properties)
        sold_mapped = self.data_mapper.map_properties(sold_properties)
        
        # Calculate statistics
        location_name = f"{city}, {state}" if city and state else zip_code or "the area"
        
        result_text = f"# Market Analysis - {location_name.title()}\n\n"
        result_text += f"**Property Type**: {property_type.replace('_', ' ').title()}\n"
        result_text += f"**Analysis Period**: Last {days_back} days\n\n"
        
        # Active listings analysis
        result_text += "## Active Listings\n"
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
            
            # Bedroom distribution
            bedroom_counts = {}
            for prop in active_mapped:
                bedrooms = prop.get("bedrooms")
                if bedrooms:
                    bedroom_counts[bedrooms] = bedroom_counts.get(bedrooms, 0) + 1
            
            if bedroom_counts:
                result_text += "- **Bedroom Distribution**:\n"
                for bedrooms in sorted(bedroom_counts.keys()):
                    result_text += f"  - {bedrooms} BR: {bedroom_counts[bedrooms]} properties\n"
        
        # Recently sold analysis
        result_text += "\n## Recently Sold Properties\n"
        result_text += f"- **Total Sold**: {len(sold_mapped)} properties\n"
        
        if sold_mapped:
            sold_prices = [p["sold_price"] for p in sold_mapped if p.get("sold_price")]
            if sold_prices:
                result_text += f"- **Average Sold Price**: ${sum(sold_prices) // len(sold_prices):,}\n"
                result_text += f"- **Median Sold Price**: ${sorted(sold_prices)[len(sold_prices)//2]:,}\n"
                result_text += f"- **Sold Price Range**: ${min(sold_prices):,} - ${max(sold_prices):,}\n"
        
        # Market insights
        result_text += "\n## Market Insights\n"
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
            
            if len(active_mapped) > 0:
                inventory_level = "High" if len(active_mapped) > 50 else "Moderate" if len(active_mapped) > 20 else "Low"
                result_text += f"- **Inventory Level**: {inventory_level} ({len(active_mapped)} active listings)\n"
        
        if not active_mapped and not sold_mapped:
            result_text += "No properties found for the specified criteria.\n"
        
        return CallToolResult(
            content=[TextContent(type="text", text=result_text)]
        )
    
    async def _find_agent(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Find real estate agents or members."""
        name = arguments.get("name")
        office = arguments.get("office")
        city = arguments.get("city")
        state = arguments.get("state")
        specialization = arguments.get("specialization")
        limit = arguments.get("limit", 20)
        
        logger.info("Searching for agents with criteria: %s", arguments)
        
        # Build search filters
        filters = {}
        if name:
            filters["agent_name"] = name
        if office:
            filters["office_name"] = office
        if city:
            filters["city"] = city
        if state:
            filters["state"] = state
        if specialization:
            filters["specialization"] = specialization
        
        # Search members
        members = await self.reso_client.query_members(
            filters=filters,
            limit=limit
        )
        
        if not members:
            return CallToolResult(
                content=[TextContent(type="text", text="No agents found matching your criteria.")]
            )
        
        # Format results
        result_text = f"Found {len(members)} real estate agents:\n\n"
        
        for i, member in enumerate(members[:limit], 1):
            # Extract member information
            member_key = member.get("MemberKey", "N/A")
            first_name = member.get("MemberFirstName", "")
            last_name = member.get("MemberLastName", "")
            full_name = f"{first_name} {last_name}".strip() or member.get("MemberFullName", "N/A")
            
            result_text += f"{i}. **{full_name}** (ID: {member_key})\n"
            
            # Contact information
            if member.get("MemberEmail"):
                result_text += f"   📧 {member['MemberEmail']}\n"
            if member.get("MemberMobilePhone"):
                result_text += f"   📱 {member['MemberMobilePhone']}\n"
            elif member.get("MemberDirectPhone"):
                result_text += f"   📞 {member['MemberDirectPhone']}\n"
            
            # Office information
            if member.get("MemberOfficeName"):
                result_text += f"   🏢 {member['MemberOfficeName']}\n"
            
            # Location
            location_parts = []
            if member.get("MemberCity"):
                location_parts.append(member["MemberCity"])
            if member.get("MemberStateOrProvince"):
                location_parts.append(member["MemberStateOrProvince"])
            if location_parts:
                result_text += f"   📍 {', '.join(location_parts)}\n"
            
            # License information
            if member.get("MemberStateLicense"):
                result_text += f"   📄 License: {member['MemberStateLicense']}\n"
            
            # Specialization or designation
            if member.get("MemberDesignation"):
                result_text += f"   🏆 {member['MemberDesignation']}\n"
            
            result_text += "\n"
        
        # Add search summary
        result_text += f"**Search Summary:**\n"
        search_criteria = []
        if name:
            search_criteria.append(f"Name: {name}")
        if office:
            search_criteria.append(f"Office: {office}")
        if city and state:
            search_criteria.append(f"Location: {city}, {state}")
        elif city:
            search_criteria.append(f"City: {city}")
        elif state:
            search_criteria.append(f"State: {state}")
        if specialization:
            search_criteria.append(f"Specialization: {specialization}")
        
        if search_criteria:
            result_text += f"- Criteria: {', '.join(search_criteria)}\n"
        result_text += f"- Results: {len(members)} agents found\n"
        
        return CallToolResult(
            content=[TextContent(type="text", text=result_text)]
        )
    
    def _get_search_examples(self) -> str:
        """Get property search examples."""
        return """# Property Search Examples

## Natural Language Queries

Use natural, conversational language to search for properties:

### Basic Searches
- "3 bedroom house in Austin TX"
- "condo under $400k"
- "single family homes with pool"
- "properties over 2000 sqft"

### Price-Based Searches
- "houses under $500k in Dallas"
- "homes between $300k and $600k"
- "properties over $1M with waterfront"
- "condos below 250k in Houston"

### Location-Specific Searches
- "townhouses in San Antonio TX"
- "homes in 78701 zip code"
- "properties in Travis County"
- "houses near downtown Austin"

### Feature-Based Searches
- "4 bedroom 3 bath house with garage"
- "single family home over 2500 sqft"
- "new construction under $700k"
- "homes with pool and fireplace"

### Complex Searches
- "3+ bedroom house under $450k in Austin TX with pool and 2+ car garage"
- "recently built condo under $300k near downtown with 2+ bedrooms"
- "luxury home over $1M with waterfront and 4+ bedrooms"

## Search Filters

You can also use specific filters:

- **Location**: city, state, zip_code
- **Price**: min_price, max_price
- **Size**: min_bedrooms, max_bedrooms, min_bathrooms, max_bathrooms
- **Square Footage**: min_sqft, max_sqft
- **Property Type**: residential, condo, townhouse, single_family, multi_family, manufactured, land, commercial, business
- **Status**: active, under_contract, pending, sold, closed, expired, withdrawn, cancelled, hold

## Tips for Better Results

1. **Be specific**: Include city and state for location-based searches
2. **Use ranges**: Instead of exact numbers, use "under", "over", or "between"
3. **Combine criteria**: Mix location, price, and features for targeted results
4. **Check spelling**: Ensure city and state names are spelled correctly
5. **Try variations**: If no results, try broader criteria or different property types
"""
    
    def _get_property_types_reference(self) -> str:
        """Get property types reference."""
        return """# Property Types & Status Reference

## Property Types

### Residential Properties
- **single_family**: Detached single-family homes, houses
- **condo**: Condominiums, condos
- **townhouse**: Townhomes, row houses
- **multi_family**: Duplexes, triplexes, apartment buildings
- **manufactured**: Mobile homes, manufactured housing

### Other Property Types
- **land**: Vacant land, lots
- **commercial**: Office buildings, retail spaces, warehouses
- **business**: Business opportunities, franchises
- **residential**: General residential (includes all residential subtypes)

## Property Status

### Active Listings
- **active**: Currently for sale and available
- **under_contract**: Sale pending, buyer found
- **pending**: Sale in progress, awaiting closing

### Completed Sales
- **sold**: Recently sold
- **closed**: Sale completed and closed

### Inactive Listings
- **expired**: Listing period ended without sale
- **withdrawn**: Removed from market by seller
- **cancelled**: Listing cancelled
- **hold**: Temporarily off market

## Search Tips by Property Type

### Single Family Homes
- Best for: Families, first-time buyers, investment properties
- Typical features: Private yards, garages, multiple bedrooms
- Search examples: "3 bedroom house", "single family home with garage"

### Condominiums
- Best for: Urban living, low maintenance, amenities
- Typical features: Shared amenities, HOA fees, urban locations
- Search examples: "downtown condo", "2 bedroom condo with amenities"

### Townhouses
- Best for: More space than condos, less maintenance than houses
- Typical features: Multi-level, shared walls, small yards
- Search examples: "3 bedroom townhouse", "townhome with garage"

### Land
- Best for: Building custom homes, investment, development
- Typical features: Acreage, zoning restrictions, utilities
- Search examples: "residential land", "5+ acres for building"

### Commercial
- Best for: Business investment, office space, retail locations
- Typical features: Commercial zoning, high traffic areas
- Search examples: "office building", "retail space downtown"
"""
    
    def _get_market_analysis_guide(self) -> str:
        """Get market analysis guide."""
        return """# Market Analysis Guide

## Understanding Market Data

### Active Listings Statistics
- **Total Active**: Number of properties currently for sale
- **Average Price**: Mean listing price of active properties
- **Median Price**: Middle price point (50% above, 50% below)
- **Price Range**: Lowest to highest priced active listings
- **Price per SqFt**: Average cost per square foot
- **Bedroom Distribution**: Breakdown by number of bedrooms

### Recently Sold Statistics
- **Total Sold**: Number of properties sold in the analysis period
- **Average Sold Price**: Mean sale price of sold properties
- **Median Sold Price**: Middle sale price
- **Sold Price Range**: Lowest to highest sale prices

### Market Insights

#### Price Trends
- **Rising**: Active listings priced significantly higher than recent sales
- **Declining**: Active listings priced lower than recent sales
- **Stable**: Active listings within 5% of recent sale prices

#### Inventory Levels
- **Low**: Fewer than 20 active listings (seller's market)
- **Moderate**: 20-50 active listings (balanced market)
- **High**: More than 50 active listings (buyer's market)

## Market Analysis Tips

### For Buyers
- **Rising Market**: Act quickly, expect competition, consider offers above asking
- **Declining Market**: Take your time, negotiate aggressively, wait for better deals
- **Stable Market**: Normal negotiations, standard timelines

### For Sellers
- **Rising Market**: Price competitively or slightly above, expect quick sales
- **Declining Market**: Price below market, be flexible on terms
- **Stable Market**: Price at market value, normal marketing time

### For Investors
- **Low Inventory**: Good for selling, challenging for buying
- **High Inventory**: Good for buying, more negotiating power
- **Price Trends**: Use for timing buy/sell decisions

## Analysis Limitations

- Data reflects MLS listings only (not all sales)
- Analysis period may not capture seasonal variations
- Local micro-markets may differ from area-wide trends
- New construction and private sales not included
- Market conditions change rapidly

## Custom Analysis Parameters

- **Property Type**: Focus on specific property types for targeted insights
- **Days Back**: Adjust time period (30-365 days) based on market activity
- **Location**: Use city/state or ZIP code for geographic focus
- **Price Range**: Filter by price ranges for segment-specific analysis
"""

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting UNLOCK MLS MCP server")
        
        try:
            # Test authentication
            await self.oauth_handler.get_access_token()
            logger.info("Authentication successful")
            
            # Run the server
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream
                )
                
        except Exception as e:
            logger.error("Failed to start server: %s", e, exc_info=True)
            raise

def main():
    """Main entry point."""
    server = UnlockMlsServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main()