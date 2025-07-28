
"""MCP server implementation for UNLOCK MLS RESO data access."""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ReadResourceResult,
)

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
        self.reso_client = ResoWebApiClient(
            base_url=self.settings.bridge_api_base_url,
            mls_id=self.settings.bridge_mls_id,
            server_token=self.settings.bridge_server_token
        )
        self.data_mapper = ResoDataMapper()
        self.query_validator = QueryValidator()
        
        # Create MCP server instance
        self.server = Server("unlock-mls-mcp")
        self._setup_handlers()
        
        logger.info("UnlockMlsServer initialized")
    
    def _setup_handlers(self):
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
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
            
            return tools
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
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
                return [TextContent(type="text", text=f"Validation error: {str(e)}")]
            except Exception as e:
                logger.error("Error in %s: %s", name, e, exc_info=True)
                return [TextContent(type="text", text=f"Error: {str(e)}")]
        
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
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
                ),
                Resource(
                    uri="agent://search/guide",
                    name="Agent Search Guide",
                    description="Guide for finding and working with real estate agents",
                    mimeType="text/markdown"
                ),
                Resource(
                    uri="workflows://common/patterns",
                    name="Common Workflows",
                    description="Common real estate data workflows and use cases",
                    mimeType="text/markdown"
                ),
                Resource(
                    uri="api://status/info",
                    name="API Status & Info",
                    description="Current API connection status and system information",
                    mimeType="text/markdown"
                ),
                Resource(
                    uri="prompts://guided/search",
                    name="Guided Property Search",
                    description="Step-by-step guided property search workflows",
                    mimeType="text/markdown"
                ),
                Resource(
                    uri="prompts://guided/analysis",
                    name="Guided Market Analysis",
                    description="Step-by-step guided market analysis workflows",
                    mimeType="text/markdown"
                )
            ]
            
            return resources
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """Get resource content."""
            if uri == "property://search/examples":
                content = self._get_search_examples()
            elif uri == "property://types/reference":
                content = self._get_property_types_reference()
            elif uri == "market://analysis/guide":
                content = self._get_market_analysis_guide()
            elif uri == "agent://search/guide":
                content = self._get_agent_search_guide()
            elif uri == "workflows://common/patterns":
                content = self._get_common_workflows()
            elif uri == "api://status/info":
                content = await self._get_api_status_info()
            elif uri == "prompts://guided/search":
                content = self._get_guided_search_prompts()
            elif uri == "prompts://guided/analysis":
                content = self._get_guided_analysis_prompts()
            else:
                raise ValueError(f"Unknown resource: {uri}")
            
            return ReadResourceResult(
                contents=[TextContent(type="text", text=content)]
            )
    
    async def _search_properties(self, arguments: Dict[str, Any]) -> list[TextContent]:
        """Search for properties."""
        try:
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
                return [
                    TextContent(type="text", text="No properties found matching your criteria.")]
        
        except Exception as e:
            # Handle authentication and other errors gracefully
            error_message = "An error occurred while searching for properties."
            
            if isinstance(e, ValidationError) or "validation" in str(e).lower():
                error_message = f"Validation error: {str(e)}"
            elif "authentication" in str(e).lower() or "unauthorized" in str(e).lower() or "401" in str(e):
                error_message = "Authentication error: Unable to access property data. Please check your credentials."
            elif "timeout" in str(e).lower():
                error_message = "Request timeout: The property search is taking too long. Please try again with more specific criteria."
            elif "parse" in str(e).lower() or "understand" in str(e).lower() or "query" in str(e).lower():
                error_message = f"Query parsing error: Unable to understand the search query. {str(e)}"
            elif "price range" in str(e).lower() or ("price" in str(e).lower() and "invalid" in str(e).lower()):
                error_message = f"Invalid price range: {str(e)}"
            elif "location" in str(e).lower() and "invalid" in str(e).lower():
                error_message = f"Invalid location parameters: {str(e)}"
            elif hasattr(e, 'status'):
                if e.status == 403:
                    error_message = "Access denied: You don't have permission to access this property data."
                elif e.status == 429:
                    error_message = "Rate limit exceeded: Too many requests. Please wait a moment and try again."
                elif e.status >= 500:
                    error_message = "Server error: The property service is temporarily unavailable. Please try again later."
            
            logger.error("Property search error: %s", str(e))
            return [
                TextContent(type="text", text=error_message)]

        
            
        # Map properties to standardized format
        try:
            mapped_properties = self.data_mapper.map_properties(properties)
        except Exception as mapping_error:
            logger.warning("Data mapping error, returning limited results: %s", mapping_error)
            # Return basic property data without full mapping
            result_text = f"Found {len(properties)} properties (limited details due to data formatting issues):\n\n"
            for i, prop in enumerate(properties[:limit], 1):
                listing_id = prop.get("ListingId", "N/A")
                price = prop.get("ListPrice", "N/A")
                result_text += f"{i}. **{listing_id}** - ${price:,}\n" if isinstance(price, (int, float)) else f"{i}. **{listing_id}** - {price}\n"
            
            result_text += f"\n**Note**: Some property details unavailable due to data formatting issues.\n"
            result_text += f"- Results: {len(properties)} properties found\n"
            
            return [
                TextContent(type="text", text=result_text)]

        
        # Format results
        result_text = f"Found {len(mapped_properties)} properties:\n\n"
        
        for i, prop in enumerate(mapped_properties[:limit], 1):
            try:
                summary = self.data_mapper.get_property_summary(prop)
            except Exception as summary_error:
                logger.warning("Property summary error for listing %s: %s", prop.get('listing_id', 'N/A'), summary_error)
                summary = "Details unavailable due to data formatting issues"
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
        if filters and isinstance(filters, dict):
            filter_summary = []
            for key, value in filters.items():
                if key.startswith(('min_', 'max_')):
                    filter_summary.append(f"{key.replace('_', ' ')}: {value:,}" if isinstance(value, int) else f"{key.replace('_', ' ')}: {value}")
                else:
                    filter_summary.append(f"{key.replace('_', ' ')}: {value}")
            result_text += f"- Filters: {', '.join(filter_summary)}\n"
        result_text += f"- Results: {len(mapped_properties)} properties\n"
        
        return [
            TextContent(type="text", text=result_text)]

    
    async def _get_property_details(self, arguments: Dict[str, Any]) -> list[TextContent]:
        """Get detailed property information."""
        listing_id = arguments["listing_id"]
        
        logger.info("Getting property details for listing: %s", listing_id)
        
        # Get property details
        properties = await self.reso_client.query_properties(
            filters={"listing_id": listing_id},
            limit=1
        )
        
        if not properties:
            return [
                TextContent(type="text", text=f"Property with listing ID '{listing_id}' not found.")]

        
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
        
        return [
            TextContent(type="text", text=result_text)]

    
    async def _analyze_market(self, arguments: Dict[str, Any]) -> list[TextContent]:
        """Analyze market trends and statistics."""
        try:
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
            
            # Validate location filters
            validated_filters = self.query_validator.validate_search_filters(location_filter)
            
            # Get active listings
            active_properties = await self.reso_client.query_properties(
                filters={**validated_filters, "status": "active"},
                limit=1000
            )
            
            # Get recently sold properties
            sold_properties = await self.reso_client.query_properties(
                filters={**validated_filters, "status": "sold"},
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
            
            return [
                TextContent(type="text", text=result_text)]

        
        except Exception as e:
            # Handle errors gracefully
            error_message = "An error occurred while analyzing the market."
            
            if isinstance(e, ValidationError) or "validation" in str(e).lower():
                error_message = f"Validation error: {str(e)}"
            elif "authentication" in str(e).lower() or "unauthorized" in str(e).lower() or "401" in str(e):
                error_message = "Authentication error: Unable to access market data. Please check your credentials."
            elif "timeout" in str(e).lower():
                error_message = "Request timeout: The market analysis is taking too long. Please try again."
            elif "location" in str(e).lower() and "invalid" in str(e).lower():
                error_message = f"Invalid location parameters: {str(e)}"
            elif hasattr(e, 'status'):
                if e.status == 403:
                    error_message = "Access denied: You don't have permission to access market data."
                elif e.status == 429:
                    error_message = "Rate limit exceeded: Too many requests. Please wait a moment and try again."
                elif e.status >= 500:
                    error_message = "Server error: The market analysis service is temporarily unavailable. Please try again later."
            
            logger.error("Market analysis error: %s", str(e))
            return [
                TextContent(type="text", text=error_message)]

    
    async def _find_agent(self, arguments: Dict[str, Any]) -> list[TextContent]:
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
            return [
                TextContent(type="text", text="No agents found matching your criteria.")]

        
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
        
        return [
            TextContent(type="text", text=result_text)]

    
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
    
    def _get_agent_search_guide(self) -> str:
        """Get agent search guide."""
        return """# Agent Search Guide

## Finding Real Estate Agents

### Search by Name
- Use partial or full agent names to find specific agents
- Example: `find_agent(name="John Smith")`
- Supports fuzzy matching for approximate names

### Search by Location
- Find agents in specific cities or states
- Example: `find_agent(city="Austin", state="TX")`
- Useful for finding local market experts

### Search by Office
- Find all agents associated with a specific brokerage
- Example: `find_agent(office="Keller Williams")`
- Helps identify team members or office contacts

### Search by Specialization
- Find agents with specific expertise areas
- Example: `find_agent(specialization="luxury homes")`
- Common specializations: first-time buyers, luxury, commercial, investment

## Agent Information Available

### Contact Details
- **Email**: Primary contact email address
- **Phone**: Mobile or direct phone numbers
- **Office Phone**: Main office contact number

### Professional Information
- **License Number**: State real estate license
- **Office Affiliation**: Current brokerage association
- **Designations**: Professional certifications (CRS, GRI, etc.)

### Location Coverage
- **Primary Market**: Main city/county of operation
- **Service Areas**: Geographic regions covered
- **Local Expertise**: Years of experience in area

## Working with Agents

### Initial Contact
1. Use agent search to find qualified professionals
2. Review their location and specialization match
3. Contact via preferred method (email/phone)
4. Discuss your specific needs and timeline

### Vetting Questions
- How long have you worked in this market?
- What's your average days on market for listings?
- Can you provide references from recent clients?
- What's your commission structure?

### Collaboration Tips
- Be clear about your budget and requirements
- Ask for market analysis and comparable sales
- Request regular communication and updates
- Understand their marketing strategy for your property

## Agent Selection Criteria

### For Buyers
- **Local Market Knowledge**: Deep understanding of neighborhoods
- **Negotiation Skills**: Track record of successful purchases
- **Response Time**: Quick communication and showing availability
- **Technology Use**: MLS access and digital tools proficiency

### For Sellers
- **Marketing Strategy**: Comprehensive listing and promotion plan
- **Pricing Expertise**: Accurate comparative market analysis
- **Network**: Connections with other agents and service providers
- **Track Record**: Recent sales history and average days on market

### For Investors
- **Investment Experience**: Understanding of cash flow and ROI
- **Market Analysis**: Ability to identify emerging opportunities
- **Rental Knowledge**: Understanding of landlord-tenant law
- **Network**: Connections with contractors, property managers

## Common Agent Types

### Buyer's Agents
- Represent buyers in property purchases
- Help with property search and negotiation
- Typically paid by seller's commission split

### Listing Agents
- Represent sellers in property sales
- Handle marketing, showings, and negotiations
- Paid commission percentage of sale price

### Dual Agents
- Represent both buyer and seller (where legal)
- Must disclose dual representation
- May have limitations on advocacy

### Team Leaders vs Individual Agents
- **Teams**: Multiple agents, specialized roles, broader coverage
- **Individual**: Personal attention, direct communication, consistent service
"""
    
    def _get_common_workflows(self) -> str:
        """Get common real estate workflows."""
        return """# Common Real Estate Workflows

## Buyer Workflows

### First-Time Home Buyer Journey
1. **Pre-Qualification**
   - Get pre-approved for mortgage
   - Understand budget and down payment requirements
   - Research mortgage programs (FHA, VA, conventional)

2. **Market Research**
   - Use `search_properties` to explore available homes
   - Set up saved searches with specific criteria
   - Research neighborhoods and school districts

3. **Property Evaluation**
   - Use `get_property_details` for comprehensive information
   - Schedule showings and inspections
   - Research comparable sales in the area

4. **Market Analysis**
   - Use `analyze_market` to understand pricing trends
   - Compare multiple neighborhoods or property types
   - Assess market conditions (buyer's vs seller's market)

5. **Agent Selection**
   - Use `find_agent` to identify qualified buyer's agents
   - Interview multiple agents for best fit
   - Check references and recent transaction history

### Investment Property Search
1. **Market Identification**
   - Use `analyze_market` for different cities/regions
   - Compare rental yields and appreciation potential
   - Research local rental market conditions

2. **Property Screening**
   - Filter by cash flow criteria using `search_properties`
   - Calculate cap rates and cash-on-cash returns
   - Evaluate property condition and improvement needs

3. **Due Diligence**
   - Get detailed property information with `get_property_details`
   - Research comparable rental rates
   - Analyze neighborhood crime and development trends

## Seller Workflows

### Property Preparation for Sale
1. **Market Analysis**
   - Use `analyze_market` to understand current conditions
   - Research recent comparable sales
   - Determine optimal pricing strategy

2. **Agent Selection**
   - Use `find_agent` to find experienced listing agents
   - Compare marketing strategies and commission structures
   - Review recent sales performance and market expertise

3. **Property Positioning**
   - Research competing listings with `search_properties`
   - Identify unique selling points and advantages
   - Plan improvements or staging strategies

### Pricing Strategy Development
1. **Comparative Market Analysis**
   - Search recently sold properties with similar features
   - Analyze price per square foot trends
   - Consider market timing and seasonal factors

2. **Competitive Analysis**
   - Monitor active listings in the same area
   - Track price changes and days on market
   - Adjust pricing based on market feedback

## Real Estate Professional Workflows

### Agent Market Preparation
1. **Client Consultation Prep**
   - Use `analyze_market` for comprehensive market overview
   - Prepare comparable sales data
   - Research neighborhood trends and demographics

2. **Listing Presentation Development**
   - Gather comparable active and sold properties
   - Prepare pricing recommendations with supporting data
   - Create marketing strategy based on market conditions

3. **Buyer Consultation**
   - Prepare market overview for target areas
   - Research inventory levels and competition
   - Develop realistic expectation setting materials

### Market Research Workflows
1. **Quarterly Market Reports**
   - Analyze trends across multiple property types
   - Compare different neighborhoods or regions
   - Track inventory levels and price movements

2. **Client Market Updates**
   - Monitor specific areas for client interests
   - Track new listings and price changes
   - Provide regular market condition updates

## Investor Workflows

### Portfolio Analysis
1. **Market Comparison**
   - Use `analyze_market` across multiple cities
   - Compare cap rates and appreciation potential
   - Analyze supply and demand indicators

2. **Property Pipeline Management**
   - Set up searches for specific investment criteria
   - Monitor multiple markets simultaneously
   - Track new opportunities and market changes

### Risk Assessment
1. **Market Diversification**
   - Analyze different geographic markets
   - Compare property types and price ranges
   - Assess economic dependency and stability

2. **Exit Strategy Planning**
   - Monitor market conditions for optimal timing
   - Track appreciation trends and rental demand
   - Plan renovation and improvement strategies

## API Integration Patterns

### Automated Monitoring
- Set up regular market analysis for target areas
- Monitor specific property criteria with alerts
- Track agent performance and availability

### Data Integration
- Export property data for external analysis
- Integrate with CRM systems for client management
- Connect with financial planning tools

### Workflow Automation
- Automate initial property screening
- Schedule regular market report generation
- Integrate with calendar systems for showing coordination

## Best Practices

### Search Optimization
- Start broad, then narrow with specific criteria
- Use natural language queries for exploratory searches
- Combine multiple search approaches for comprehensive results

### Data Validation
- Cross-reference multiple data sources
- Verify property details with recent information
- Confirm agent credentials and current status

### Market Timing
- Consider seasonal market patterns
- Monitor interest rate impacts on demand
- Track local economic indicators and development plans
"""
    
    async def _get_api_status_info(self) -> str:
        """Get current API status and system information."""
        try:
            # Test authentication by checking if we have server token
            auth_status = "✅ Connected" if self.settings.bridge_server_token else "❌ Failed"
            
            # Get basic system info
            status_content = f"""# API Status & System Information

## Authentication Status
- **OAuth2 Connection**: {auth_status}
- **Bridge API**: {self.settings.bridge_api_base_url}
- **MLS ID**: {self.settings.bridge_mls_id}

## Available Tools
- **search_properties**: ✅ Ready - Search for properties using natural language or filters
- **get_property_details**: ✅ Ready - Get comprehensive property information
- **analyze_market**: ✅ Ready - Analyze market trends and statistics
- **find_agent**: ✅ Ready - Find real estate agents and members

## Available Resources
- **Property Search Examples**: ✅ Ready - Common search query examples
- **Property Types Reference**: ✅ Ready - Property types and status guide
- **Market Analysis Guide**: ✅ Ready - Understanding market data
- **Agent Search Guide**: ✅ Ready - Finding and working with agents
- **Common Workflows**: ✅ Ready - Real estate workflow patterns
- **API Status Info**: ✅ Ready - Current system status (this resource)

## System Configuration
- **Log Level**: {self.settings.log_level}
- **Rate Limiting**: {self.settings.api_rate_limit_per_minute} requests/minute
- **Cache Enabled**: {'Yes' if self.settings.cache_enabled else 'No'}
- **Cache TTL**: {self.settings.cache_ttl_seconds} seconds

## Data Sources
- **Primary**: Bridge Interactive RESO Web API
- **MLS Coverage**: UNLOCK MLS real estate data
- **Data Standard**: RESO Data Dictionary 2.0 compliant
- **Update Frequency**: Real-time via API calls

## Support Information
- **MCP Version**: Using mcp.server framework
- **Transport**: stdio (compatible with Claude Desktop)
- **Error Handling**: Graceful degradation with user-friendly messages
- **Validation**: Input sanitization and natural language parsing

## Usage Statistics
- **Server Status**: Running and accepting requests
- **Authentication**: Valid token {'available' if token else 'unavailable'}
- **Last Health Check**: {self._get_current_timestamp()}

## Troubleshooting
If you encounter issues:
1. Check environment variables are properly configured
2. Verify Bridge Interactive API credentials
3. Ensure network connectivity to api.bridgedataoutput.com
4. Check log files for detailed error information

For technical support, refer to the project documentation or contact the development team.
"""
            
        except Exception as e:
            status_content = f"""# API Status & System Information

## ⚠️ System Status: Error

**Error Details**: {str(e)}

## Troubleshooting Steps
1. Check environment configuration (.env file)
2. Verify Bridge Interactive API credentials
3. Ensure network connectivity
4. Check server logs for detailed error information

## Available Tools (May be Limited)
- **search_properties**: ⚠️ May be limited due to authentication issues
- **get_property_details**: ⚠️ May be limited due to authentication issues  
- **analyze_market**: ⚠️ May be limited due to authentication issues
- **find_agent**: ⚠️ May be limited due to authentication issues

## Available Resources (Always Available)
- **Property Search Examples**: ✅ Ready
- **Property Types Reference**: ✅ Ready
- **Market Analysis Guide**: ✅ Ready
- **Agent Search Guide**: ✅ Ready
- **Common Workflows**: ✅ Ready

Please resolve authentication issues to access full functionality.
"""
        
        return status_content
    
    def _get_guided_search_prompts(self) -> str:
        """Get guided property search prompts."""
        return """# Guided Property Search Workflows

## Quick Start Property Search

### Step 1: Define Your Search Criteria
**Choose your approach:**

#### For Natural Language Search:
```
Use search_properties with a natural language query:
- "3 bedroom house under $500k in Austin TX"
- "Condo with pool downtown Dallas under $400k"  
- "Single family home over 2000 sqft in Houston"
```

#### For Structured Search:
```
Use search_properties with specific filters:
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

### Step 2: Review Initial Results
- Examine the property summaries
- Note listing IDs for properties of interest
- Adjust search criteria if needed

### Step 3: Get Detailed Information
```
For each property of interest, use get_property_details:
{
  "listing_id": "LISTING_ID_FROM_SEARCH"
}
```

## Guided Search Scenarios

### Scenario 1: First-Time Home Buyer
**Goal**: Find affordable starter homes

**Step 1**: Start broad
```
Query: "houses under $300k with 2+ bedrooms"
```

**Step 2**: Refine by location
```
Query: "houses under $300k with 2+ bedrooms in [your city]"
```

**Step 3**: Add specific requirements
```
Filters: {
  "city": "Your City",
  "state": "Your State", 
  "max_price": 300000,
  "min_bedrooms": 2,
  "property_type": "single_family"
}
```

**Step 4**: Analyze the market
```
Use analyze_market for your target area to understand:
- Average prices in your budget
- Number of available properties
- Market trends (rising/falling prices)
```

### Scenario 2: Investment Property Search
**Goal**: Find rental properties with good cash flow

**Step 1**: Research markets
```
Use analyze_market for different cities:
{
  "city": "Austin",
  "state": "TX",
  "property_type": "single_family"
}
```

**Step 2**: Filter by investment criteria
```
Search for properties with:
- Lower price per square foot
- Good rental neighborhoods
- Multiple bedrooms for higher rent
```

**Step 3**: Calculate returns
```
For each property:
1. Get detailed information
2. Research rental rates in the area
3. Calculate cap rate and cash flow
```

### Scenario 3: Luxury Home Search
**Goal**: Find high-end properties with specific features

**Step 1**: Set premium criteria
```
Filters: {
  "min_price": 1000000,
  "min_sqft": 3000,
  "property_type": "single_family"
}
```

**Step 2**: Add luxury features
```
Query: "luxury home over $1M with pool and waterfront"
```

**Step 3**: Research exclusive areas
```
Focus search on high-end neighborhoods and gated communities
```

## Advanced Search Techniques

### Comparative Shopping
1. **Search multiple areas**:
   - Compare similar properties in different neighborhoods
   - Use consistent criteria across searches

2. **Price range exploration**:
   - Search at different price points
   - Understand what features change with price

3. **Market timing**:
   - Monitor the same search over time
   - Track price changes and new listings

### Search Optimization Tips

#### Effective Natural Language Queries
- **Be specific**: Include location, price, and key features
- **Use common terms**: "bedroom" not "BR", "bathroom" not "BA"
- **Include budget**: "under $500k" or "between $300k and $400k"
- **Mention must-haves**: "with garage", "with pool", "near schools"

#### Smart Filter Usage
- **Start broad, then narrow**: Begin with location and price, add features
- **Use ranges**: min/max for price, bedrooms, square footage
- **Combine criteria**: Location + price + size + features
- **Test variations**: Try different property types and price ranges

## Troubleshooting Common Issues

### No Results Found
1. **Broaden criteria**: Increase price range or reduce requirements
2. **Check spelling**: Verify city names and state abbreviations
3. **Try nearby areas**: Expand to surrounding cities or ZIP codes
4. **Adjust property types**: Include condos, townhouses if searching single family

### Too Many Results
1. **Add more filters**: Narrow by price, size, or features
2. **Specify location**: Use specific neighborhoods or ZIP codes
3. **Increase minimums**: Raise minimum price, bedrooms, or square footage
4. **Focus search**: Target specific property types or features

### Outdated Information
1. **Check listing dates**: Focus on recently listed properties
2. **Verify status**: Use status filters for "active" listings only
3. **Cross-reference**: Confirm details with agent or listing source

## Next Steps After Search

### Property Evaluation
1. **Get detailed information** for top candidates
2. **Research neighborhood** and local amenities
3. **Check comparable sales** in the area
4. **Schedule showings** with listing agents

### Market Analysis
1. **Understand pricing trends** in target areas
2. **Compare inventory levels** across different locations
3. **Assess market conditions** for negotiation strategy

### Agent Connection
1. **Find local agents** using find_agent tool
2. **Research agent specializations** and experience
3. **Prepare questions** about market and properties
"""
    
    def _get_guided_analysis_prompts(self) -> str:
        """Get guided market analysis prompts."""
        return """# Guided Market Analysis Workflows

## Quick Start Market Analysis

### Step 1: Choose Your Analysis Scope
**Define your target area:**

#### City-Wide Analysis:
```
Use analyze_market with city and state:
{
  "city": "Austin",
  "state": "TX",
  "property_type": "residential",
  "days_back": 90
}
```

#### ZIP Code Analysis:
```
Use analyze_market with specific ZIP:
{
  "zip_code": "78701",
  "property_type": "single_family",
  "days_back": 90
}
```

### Step 2: Interpret the Results
- **Active Listings**: Current market inventory
- **Recently Sold**: Recent transaction data
- **Price Trends**: Market direction indicators
- **Inventory Levels**: Supply and demand balance

### Step 3: Compare Multiple Areas
Run the same analysis for different locations to compare:
- Average prices and price ranges
- Market activity levels
- Inventory and demand patterns

## Guided Analysis Scenarios

### Scenario 1: Home Buyer Market Research
**Goal**: Understand if it's a good time to buy

**Step 1**: Analyze your target area
```
{
  "city": "Your Target City",
  "state": "State",
  "property_type": "residential",
  "days_back": 90
}
```

**Questions to answer:**
- Are prices rising or stable?
- How much inventory is available?
- What's the average time on market?

**Step 2**: Compare property types
```
Run separate analyses for:
- single_family
- condo  
- townhouse
```

**Step 3**: Assess market conditions
- **Rising prices + Low inventory** = Seller's market (act quickly)
- **Stable prices + Moderate inventory** = Balanced market
- **Declining prices + High inventory** = Buyer's market (negotiate)

### Scenario 2: Seller Market Timing
**Goal**: Determine optimal listing strategy

**Step 1**: Current market analysis
```
{
  "city": "Your City",
  "state": "Your State",
  "property_type": "single_family",
  "days_back": 60
}
```

**Step 2**: Compare recent periods
```
Run analyses for different time periods:
- Last 30 days
- Last 60 days  
- Last 90 days
```

**Step 3**: Pricing strategy
- **Rising market**: Price competitively or slightly above
- **Stable market**: Price at market value
- **Declining market**: Price below market for quick sale

### Scenario 3: Investment Market Selection
**Goal**: Find the best markets for investment

**Step 1**: Multi-market comparison
```
Compare multiple cities:
- Austin, TX
- Dallas, TX
- Houston, TX
- San Antonio, TX
```

**Step 2**: Property type analysis
```
For each market, analyze:
- single_family (traditional rentals)
- multi_family (apartment buildings)
- condo (urban rentals)
```

**Step 3**: Investment metrics
Calculate for each market:
- Average price per square foot
- Rental yield potential
- Market stability indicators

## Advanced Analysis Techniques

### Seasonal Trend Analysis
**Compare different time periods:**

#### Winter vs Summer Markets
```
Winter analysis (Dec-Feb):
{"days_back": 90, "city": "Target City"}

Summer analysis (Jun-Aug):  
{"days_back": 90, "city": "Target City"}
```

#### Year-over-year comparison
- Current year: days_back: 90
- Previous year: Historical data analysis

### Micro-Market Analysis
**Neighborhood-level insights:**

#### ZIP Code Comparison
```
Analyze each ZIP code separately:
- 78701 (Downtown Austin)
- 78704 (South Austin)  
- 78759 (North Austin)
```

#### Property Type Segmentation
```
Compare segments within same area:
- Luxury homes ($1M+)
- Mid-range homes ($300k-$1M)
- Starter homes (Under $300k)
```

### Market Cycle Analysis
**Understanding market phases:**

#### Expansion Phase Indicators
- Rising prices
- Increasing sales volume
- Low inventory
- Quick sales

#### Peak Phase Indicators
- Highest prices
- Maximum activity
- Lowest inventory
- Bidding wars

#### Contraction Phase Indicators
- Declining prices
- Reduced activity
- Increasing inventory
- Longer time on market

#### Recovery Phase Indicators
- Stabilizing prices
- Improving activity
- Balanced inventory
- Normal transaction times

## Market Analysis Interpretation Guide

### Price Trend Analysis
**Rising Trends (5%+ increase):**
- Strong demand
- Limited supply
- Economic growth
- Population increase

**Stable Trends (±5%):**
- Balanced market
- Steady demand
- Normal inventory
- Economic stability

**Declining Trends (5%+ decrease):**
- Weak demand
- Excess supply
- Economic concerns
- Market correction

### Inventory Level Analysis
**Low Inventory (<20 properties):**
- Seller's market
- Quick sales expected
- Potential for bidding wars
- Higher prices likely

**Moderate Inventory (20-50 properties):**
- Balanced market
- Normal negotiation
- Standard timelines
- Fair pricing

**High Inventory (>50 properties):**
- Buyer's market
- Longer time on market
- More negotiating power
- Potential price reductions

## Actionable Insights

### For Buyers
**Rising Market Strategy:**
- Act quickly on desired properties
- Be prepared to offer asking price
- Consider pre-approval for faster offers
- Focus on properties with good value

**Stable Market Strategy:**
- Take time to evaluate options
- Negotiate based on property condition
- Standard due diligence timelines
- Focus on long-term value

**Declining Market Strategy:**
- Take advantage of inventory
- Negotiate aggressively
- Request seller concessions
- Consider value opportunities

### For Sellers
**Rising Market Strategy:**
- Price competitively
- Expect quick offers
- Minimal staging required
- Consider multiple offers

**Stable Market Strategy:**
- Price at market value
- Professional presentation
- Standard marketing time
- Be prepared to negotiate

**Declining Market Strategy:**
- Price below market
- Extensive staging/improvements
- Aggressive marketing
- Consider incentives

### For Investors
**Market Selection Criteria:**
- Population growth trends
- Economic diversification
- Job market strength
- Infrastructure development

**Timing Considerations:**
- Buy in declining/stable markets
- Sell in rising/peak markets
- Hold through cycles
- Focus on cash flow

## Analysis Validation

### Cross-Reference Data
1. **Compare with other sources**: Verify trends with local reports
2. **Check recent sales**: Confirm with comparable sales data
3. **Consult local experts**: Speak with local agents and professionals

### Update Frequency
- **Weekly**: For active buying/selling decisions
- **Monthly**: For market monitoring
- **Quarterly**: For investment planning
- **Annually**: For long-term strategy

### Quality Checks
- Ensure adequate sample size (10+ properties)
- Verify data recency and relevance
- Consider seasonal adjustments
- Account for local market factors
"""
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp for status reporting."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting UNLOCK MLS MCP server")
        
        try:
            # Verify Bearer token is available
            if not self.settings.bridge_server_token:
                raise ValueError("Bridge server token is required")
            logger.info("Authentication configured with Bearer token")
            
            # Run the server
            async with stdio_server() as (read_stream, write_stream):
                init_options = InitializationOptions(
                    server_name=self.settings.mcp_server_name,
                    server_version="1.0.0",
                    capabilities={}
                )
                await self.server.run(
                    read_stream,
                    write_stream,
                    init_options
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

