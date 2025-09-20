
"""MCP server implementation for UNLOCK MLS RESO data access."""

import asyncio
from typing import Dict, Any, Optional

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
from .utils.location_service import LocationService, LocationServiceError
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

        # Initialize location service if Google Maps API key is available
        self.location_service = None

        # Debug: Check Google Maps API key status
        api_key = self.settings.google_maps_api_key
        api_key_status = "configured" if api_key else "missing"
        if api_key:
            api_key_preview = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "too_short"
        else:
            api_key_preview = "None"

        logger.info("Google Maps API key status: %s (preview: %s)", api_key_status, api_key_preview)

        if self.settings.google_maps_api_key:
            try:
                self.location_service = LocationService()
                logger.info("Location service enabled with Google Maps integration")
            except Exception as e:
                logger.error("Failed to initialize location service: %s", e)
                import traceback
                logger.error("Location service initialization traceback: %s", traceback.format_exc())
        else:
            logger.warning("Location service disabled - Google Maps API key not configured")
        
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
                                    },
                                    "neighborhood": {
                                        "type": "string",
                                        "description": "Neighborhood, subdivision, or area name"
                                    },
                                    "subdivision": {
                                        "type": "string", 
                                        "description": "Specific subdivision name"
                                    },
                                    "mls_area_major": {
                                        "type": "string",
                                        "description": "Major MLS marketing area"
                                    },
                                    "mls_area_minor": {
                                        "type": "string",
                                        "description": "Minor/sub MLS marketing area"
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
                ),
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
            ]

            # Add location-based search tool if Google Maps is configured
            if self.location_service:
                tools.append(
                    Tool(
                        name="find_properties_near_location",
                        description="Find real estate properties near any location (businesses, landmarks, addresses, hospitals, schools, etc.) using Google Maps integration",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "Location name, address, business name, or point of interest (e.g., 'Austin City Hall', '123 Main St, Austin TX', 'Starbucks on 6th Street')"
                                },
                                "radius_miles": {
                                    "type": "number",
                                    "description": "Search radius in miles",
                                    "default": 1.0,
                                    "minimum": 0.1,
                                    "maximum": 10.0
                                },
                                "property_filters": {
                                    "type": "object",
                                    "description": "Standard RESO property search filters",
                                    "properties": {
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
                                    "description": "Maximum number of properties to return",
                                    "default": 25,
                                    "minimum": 1,
                                    "maximum": 100
                                }
                            },
                            "required": ["location"]
                        }
                    )
                )

                # Add distance calculation tool
                tools.append(
                    Tool(
                        name="find_distance_to_nearest",
                        description="Find the distance between a property address and the nearest location of a specific type (hospitals, schools, restaurants, etc.)",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "property_address": {
                                    "type": "string",
                                    "description": "Property address to calculate distance from"
                                },
                                "place_type": {
                                    "type": "string",
                                    "description": "Type of place to find (e.g., 'hospital', 'school', 'restaurant', 'grocery_store', 'park', 'gas_station')"
                                },
                                "radius_miles": {
                                    "type": "number",
                                    "default": 5.0,
                                    "minimum": 0.1,
                                    "maximum": 25.0,
                                    "description": "Search radius in miles (default: 5.0)"
                                },
                                "max_results": {
                                    "type": "integer",
                                    "default": 5,
                                    "minimum": 1,
                                    "maximum": 20,
                                    "description": "Maximum number of nearest places to return (default: 5)"
                                }
                            },
                            "required": ["property_address", "place_type"]
                        }
                    )
                )

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
                elif name == "analyze_market_by_address":
                    return await self._analyze_market_by_address(arguments)
                elif name == "find_agent":
                    return await self._find_agent(arguments)
                elif name == "find_properties_near_location":
                    return await self._find_properties_near_location(arguments)
                elif name == "find_distance_to_nearest":
                    return await self._find_distance_to_nearest(arguments)
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
            
            # Handle neighborhood field mapping
            if "neighborhood" in filters:
                # Try SubdivisionName as the primary field for neighborhoods
                filters["SubdivisionName"] = filters.pop("neighborhood")
            
            # Map specific neighborhood fields to RESO field names
            if "subdivision" in filters:
                filters["SubdivisionName"] = filters.pop("subdivision")
            
            if "mls_area_major" in filters:
                filters["MLSAreaMajor"] = filters.pop("mls_area_major")
            
            if "mls_area_minor" in filters:
                filters["MLSAreaMinor"] = filters.pop("mls_area_minor")
            
            logger.info("Searching properties with filters: %s", filters)
            
            # Search properties with fallback logic for neighborhoods
            properties = await self.reso_client.query_properties(
                filters=filters,
                limit=limit
            )
            
            # If no results and we have a neighborhood search, try fallback strategies
            original_neighborhood = None
            if not properties and any(key in filters for key in ['SubdivisionName', 'MLSAreaMajor', 'MLSAreaMinor']):
                # Store original neighborhood value for fallback message
                original_neighborhood = filters.get('SubdivisionName') or filters.get('MLSAreaMajor') or filters.get('MLSAreaMinor')
                
                # Try fallback: search without neighborhood to see if other criteria work
                fallback_filters = {k: v for k, v in filters.items() 
                                  if k not in ['SubdivisionName', 'MLSAreaMajor', 'MLSAreaMinor']}
                
                if fallback_filters:  # Only try fallback if we have other criteria
                    fallback_properties = await self.reso_client.query_properties(
                        filters=fallback_filters,
                        limit=min(limit, 10)  # Limit fallback results
                    )
                    
                    if fallback_properties:
                        # Map fallback properties to check if any have subdivision data
                        mapped_fallback = self.data_mapper.map_properties(fallback_properties)
                        
                        # Check if any fallback results have subdivision names
                        available_subdivisions = set()
                        for prop in mapped_fallback:
                            if prop.get('subdivision'):
                                available_subdivisions.add(prop['subdivision'])
                        
                        # Create helpful error message with suggestions
                        error_msg = f"No properties found in '{original_neighborhood}' neighborhood"
                        if fallback_properties:
                            city = filters.get('city', 'the area')
                            state = filters.get('state', '')
                            location = f"{city}, {state}".strip(', ')
                            error_msg += f", but found {len(fallback_properties)} properties in {location}"
                            
                            if available_subdivisions:
                                subdivisions_list = sorted(list(available_subdivisions))[:5]  # Show max 5
                                error_msg += f".\n\n**Available neighborhoods/subdivisions in this area:**\n"
                                for sub in subdivisions_list:
                                    error_msg += f"- {sub}\n"
                                if len(available_subdivisions) > 5:
                                    error_msg += f"- ... and {len(available_subdivisions) - 5} more\n"
                            else:
                                error_msg += ".\n\n**Note:** Properties in this area may not have specific neighborhood/subdivision data in the MLS."
                        
                        error_msg += f"\n\n**Suggestions:**\n"
                        error_msg += f"- Try searching for '{original_neighborhood}' without quotes\n"
                        error_msg += f"- Check if the neighborhood name is spelled correctly\n"
                        error_msg += f"- Try searching by street name if you know specific streets\n"
                        error_msg += f"- Use broader area search (city/ZIP code only)\n"
                        
                        return [TextContent(type="text", text=error_msg)]
            
            if not properties:
                # Standard no results message
                message = "No properties found matching your criteria."
                if original_neighborhood:
                    city = filters.get('city', '')
                    state = filters.get('state', '')
                    location = f" in {city}, {state}".strip(', ') if city or state else ""
                    message = f"No properties found for '{original_neighborhood}'{location}. Try checking the spelling or using a broader search."
                
                return [TextContent(type="text", text=message)]
            
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
            property_type = arguments.get("property_type")
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
            
            if property_type:
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
            if property_type:
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

    async def _find_properties_near_location(self, arguments: Dict[str, Any]) -> list[TextContent]:
        """Find properties near a location using Google Maps Places API."""
        if not self.location_service:
            return [TextContent(type="text", text="Location-based search is not available. Please configure the Google Maps API key to enable this feature.")]

        try:
            location = arguments["location"]
            radius_miles = arguments.get("radius_miles", 1.0)
            property_filters = arguments.get("property_filters", {})
            limit = arguments.get("limit", 25)

            logger.info("Finding properties near location: %s within %f miles", location, radius_miles)

            # Validate property filters if provided
            if property_filters:
                property_filters = self.query_validator.validate_search_filters(property_filters)

            # Use location service to find properties
            properties, metadata = await self.location_service.expand_search_if_needed(
                location=location,
                radius_miles=radius_miles,
                reso_client=self.reso_client,
                property_filters=property_filters,
                limit=limit,
                min_results=3  # Expand search if fewer than 3 results
            )

            if not properties:
                # Generate helpful error message based on location type
                resolved_info = metadata.get('resolved_location', {})
                location_type = resolved_info.get('location_type', 'general')

                error_msg = f"No properties found near '{location}' within {radius_miles} miles"

                if property_filters:
                    filter_desc = []
                    for key, value in property_filters.items():
                        if key.startswith(('min_', 'max_')):
                            filter_desc.append(f"{key.replace('_', ' ')}: {value:,}" if isinstance(value, int) else f"{key.replace('_', ' ')}: {value}")
                        else:
                            filter_desc.append(f"{key.replace('_', ' ')}: {value}")
                    error_msg += f" matching your criteria ({', '.join(filter_desc)})"

                error_msg += ".\n\n**Suggestions:**\n"
                error_msg += f"- Try expanding the search radius (currently {radius_miles} miles)\n"
                error_msg += "- Adjust or remove some property filters\n"
                error_msg += "- Check the spelling of the location name\n"

                if location_type == 'business':
                    error_msg += "- Try including the city name with the business\n"
                elif location_type == 'address':
                    error_msg += "- Verify the address is correct and complete\n"

                return [TextContent(type="text", text=error_msg)]

            # Map properties to standardized format
            try:
                mapped_properties = self.data_mapper.map_properties(properties)
            except Exception as mapping_error:
                logger.warning("Data mapping error, returning limited results: %s", mapping_error)
                # Return basic property data without full mapping
                result_text = f"Found {len(properties)} properties near '{location}' (limited details due to data formatting issues):\n\n"
                for i, prop in enumerate(properties[:limit], 1):
                    listing_id = prop.get("ListingId", "N/A")
                    price = prop.get("ListPrice", "N/A")
                    distance = prop.get("distance_miles")
                    distance_str = f" ({distance:.1f} mi)" if distance else ""
                    result_text += f"{i}. **{listing_id}** - ${price:,}{distance_str}\n" if isinstance(price, (int, float)) else f"{i}. **{listing_id}** - {price}{distance_str}\n"

                return [TextContent(type="text", text=result_text)]

            # Format results with location context
            resolved_info = metadata.get('resolved_location', {})
            search_center = metadata.get('search_center', {})
            actual_radius = metadata.get('expanded_radius_miles', radius_miles)

            result_text = f"Found {len(mapped_properties)} properties near **{location}**:\n\n"

            # Add location resolution details
            if resolved_info.get('resolved_coordinates'):
                coords = resolved_info['resolved_coordinates']
                result_text += f"📍 **Resolved Location**: {coords['latitude']:.4f}, {coords['longitude']:.4f}\n"

            if actual_radius != radius_miles:
                result_text += f"🔍 **Search Radius**: Expanded from {radius_miles} to {actual_radius:.1f} miles\n"
            else:
                result_text += f"🔍 **Search Radius**: {radius_miles} miles\n"

            result_text += "\n"

            # List properties with distance information
            for i, prop in enumerate(mapped_properties[:limit], 1):
                try:
                    summary = self.data_mapper.get_property_summary(prop)
                except Exception as summary_error:
                    logger.warning("Property summary error for listing %s: %s", prop.get('listing_id', 'N/A'), summary_error)
                    summary = "Details unavailable due to data formatting issues"

                # Add distance information if available
                distance_info = ""
                if prop.get("distance_miles"):
                    distance_info = f" ({prop['distance_miles']:.1f} mi)"

                result_text += f"{i}. **{prop.get('listing_id', 'N/A')}** - {summary}{distance_info}\n"

                if prop.get("address"):
                    result_text += f"   📍 {prop['address']}\n"

                if prop.get("remarks"):
                    # Truncate remarks to first 100 characters
                    remarks = prop["remarks"][:100] + "..." if len(prop["remarks"]) > 100 else prop["remarks"]
                    result_text += f"   💬 {remarks}\n"

                result_text += "\n"

            # Add search summary
            result_text += f"\n**Search Summary:**\n"
            result_text += f"- **Location**: {location}\n"
            if resolved_info.get('location_type'):
                result_text += f"- **Location Type**: {resolved_info['location_type'].title()}\n"
            result_text += f"- **Search Area**: {actual_radius:.1f} mile radius (~{metadata.get('search_area_sq_miles', 0):.1f} sq mi)\n"

            # Add filter summary if filters were applied
            if property_filters:
                filter_summary = []
                for key, value in property_filters.items():
                    if key.startswith(('min_', 'max_')):
                        filter_summary.append(f"{key.replace('_', ' ')}: {value:,}" if isinstance(value, int) else f"{key.replace('_', ' ')}: {value}")
                    else:
                        filter_summary.append(f"{key.replace('_', ' ')}: {value}")
                result_text += f"- **Filters**: {', '.join(filter_summary)}\n"

            result_text += f"- **Results**: {len(mapped_properties)} properties found\n"

            # Add note about radius expansion if it occurred
            if actual_radius != radius_miles:
                result_text += f"\n*Note: Search radius was automatically expanded from {radius_miles} to {actual_radius:.1f} miles to find more results.*\n"

            return [TextContent(type="text", text=result_text)]

        except LocationServiceError as e:
            error_message = f"Location search error: {str(e)}"
            logger.error("Location service error: %s", str(e))
            return [TextContent(type="text", text=error_message)]
        except ValidationError as e:
            error_message = f"Validation error: {str(e)}"
            logger.warning("Validation error in find_properties_near_location: %s", e)
            return [TextContent(type="text", text=error_message)]
        except Exception as e:
            # Handle errors gracefully
            error_message = "An error occurred while searching for properties near the location."

            if "google" in str(e).lower() or "places" in str(e).lower():
                error_message = f"Google Maps service error: {str(e)}"
            elif "authentication" in str(e).lower() or "api key" in str(e).lower():
                error_message = "Google Maps API authentication error. Please check your API key configuration."
            elif "quota" in str(e).lower() or "rate limit" in str(e).lower():
                error_message = "Google Maps API quota exceeded. Please try again later or contact support."
            elif "timeout" in str(e).lower():
                error_message = "Location search timeout. Please try again with a more specific location."
            elif hasattr(e, 'status'):
                if e.status == 403:
                    error_message = "Access denied: Please check your Google Maps API key permissions."
                elif e.status == 429:
                    error_message = "Rate limit exceeded: Too many location requests. Please wait a moment and try again."
                elif e.status >= 500:
                    error_message = "Google Maps service temporarily unavailable. Please try again later."

            logger.error("Error in find_properties_near_location: %s", str(e))
            return [TextContent(type="text", text=error_message)]

    async def _find_distance_to_nearest(self, arguments: Dict[str, Any]) -> list[TextContent]:
        """Find distance between a property address and nearest location of specified type."""

        # Debug: Check location service status
        logger.info("Distance search requested - Location service status: %s",
                   "available" if self.location_service else "not available")

        if not self.location_service:
            api_key_status = "configured" if self.settings.google_maps_api_key else "missing"
            return [TextContent(type="text", text=f"Location-based search is not available. Google Maps API key is {api_key_status}. Please configure the GOOGLE_MAPS_API_KEY environment variable to enable this feature.")]

        try:
            property_address = arguments["property_address"]
            place_type = arguments["place_type"]
            radius_miles = arguments.get("radius_miles", 5.0)
            max_results = arguments.get("max_results", 5)

            logger.info("Finding nearest %s to property at: %s within %f miles", place_type, property_address, radius_miles)

            # Use location service to find nearest places
            results = await self.location_service.find_distance_to_nearest(
                address=property_address,
                place_type=place_type,
                radius_miles=radius_miles,
                max_results=max_results
            )

            # Extract the locations from the result dictionary
            locations = results.get('nearest_locations', []) if results else []

            if not locations:
                error_msg = f"No {place_type.replace('_', ' ')} locations found within {radius_miles} miles of '{property_address}'.\n\n"
                error_msg += "**Suggestions:**\n"
                error_msg += f"- Try expanding the search radius (currently {radius_miles} miles)\n"
                error_msg += "- Check the spelling of the property address\n"
                error_msg += f"- Try a different place type (e.g., 'hospital' instead of '{place_type}')\n"
                error_msg += "- Verify the address is complete with city and state\n"
                return [TextContent(type="text", text=error_msg)]

            # Format results
            result_text = f"Found {len(locations)} {place_type.replace('_', ' ')} location(s) near **{property_address}**:\n\n"

            for i, place in enumerate(locations, 1):
                name = place.get('name', 'Unknown')
                distance = place.get('straight_line_distance_miles', 0)
                address = place.get('address', 'Address not available')
                rating = place.get('rating')
                place_id = place.get('place_id', '')

                result_text += f"{i}. **{name}** ({distance:.1f} miles)\n"
                result_text += f"   📍 {address}\n"

                if rating:
                    result_text += f"   ⭐ Rating: {rating}/5\n"

                if place_id:
                    result_text += f"   🔗 Google Maps: https://maps.google.com/?cid={place_id}\n"

                result_text += "\n"

            # Add search summary
            result_text += f"**Search Summary:**\n"
            result_text += f"- **Property**: {property_address}\n"
            result_text += f"- **Looking for**: {place_type.replace('_', ' ').title()}\n"
            result_text += f"- **Search Radius**: {radius_miles} miles\n"
            result_text += f"- **Results**: {len(locations)} locations found\n"

            if locations:
                nearest = locations[0]
                result_text += f"- **Nearest**: {nearest.get('name', 'Unknown')} at {nearest.get('straight_line_distance_miles', 0):.1f} miles\n"

            return [TextContent(type="text", text=result_text)]

        except Exception as e:
            # Log the full error details for debugging
            import traceback
            logger.error("Error in find_distance_to_nearest - Exception type: %s", type(e).__name__)
            logger.error("Error in find_distance_to_nearest - Exception message: %s", str(e))
            logger.error("Error in find_distance_to_nearest - Full traceback: %s", traceback.format_exc())

            # Handle errors gracefully with detailed error messages
            error_message = f"Location search failed: {str(e)}"

            # Check for specific Google Maps API errors
            if "google" in str(e).lower() or "places" in str(e).lower():
                error_message = f"Google Maps service error: {str(e)}"
            elif "authentication" in str(e).lower() or "api key" in str(e).lower():
                error_message = "Google Maps API authentication error. Please check your API key configuration."
            elif "quota" in str(e).lower() or "rate limit" in str(e).lower():
                error_message = "Google Maps API quota exceeded. Please try again later or contact support."
            elif "timeout" in str(e).lower():
                error_message = "Location search timeout. Please try again with a more specific address."
            elif hasattr(e, 'status'):
                if e.status == 403:
                    error_message = "Access denied: Please check your Google Maps API key permissions."
                elif e.status == 429:
                    error_message = "Rate limit exceeded: Too many location requests. Please wait a moment and try again."
                elif e.status >= 500:
                    error_message = "Google Maps service temporarily unavailable. Please try again later."

            # Check for common issues
            elif "api_key" in str(e).lower() or "missing" in str(e).lower():
                error_message = "Google Maps API key is missing or invalid. Please configure the GOOGLE_MAPS_API_KEY environment variable."
            elif "location_service" in str(e).lower():
                error_message = "Location service is not properly configured. Check Google Maps API setup."

            # For debugging: include exception type and more details
            error_message += f"\n\n**Debug Info**: {type(e).__name__}: {str(e)}"

            return [TextContent(type="text", text=error_message)]

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

    
    async def _find_agent(self, arguments: Dict[str, Any]) -> list[TextContent]:
        """Find real estate agents or members."""
        name = arguments.get("name")
        office = arguments.get("office")
        city = arguments.get("city")
        state = arguments.get("state")
        specialization = arguments.get("specialization")
        limit = arguments.get("limit", 20)
        
        logger.info("Searching for agents with criteria: %s", arguments)
        
        # Build search filters using correct RESO member field names
        filters = {}
        if name:
            # Use a more flexible approach for name searching
            filters["MemberFullName"] = name
        if office:
            filters["MemberOfficeName"] = office
        if city:
            filters["MemberCity"] = city
        if state:
            filters["MemberStateOrProvince"] = state
        if specialization:
            filters["MemberDesignation"] = specialization
        
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

### Neighborhood/Subdivision Searches
- "homes in Austin Woods neighborhood"
- "properties in Barton Hills Austin TX"
- "houses in Circle C Ranch subdivision under $700k"
- "3 bedroom in Westlake Hills area"
- "condos in the Domain neighborhood"
- "properties in Steiner Ranch community"
- "houses in Mueller development"
- "homes in the Bouldin Creek area"

**Enhanced Neighborhood Search Features:**
- **Flexible Matching**: Searches use partial name matching, so "Austin Woods" will find "Austin Woods Subdivision"
- **Smart Suggestions**: If an exact neighborhood isn't found, you'll get suggestions of available neighborhoods
- **Multiple Fields**: Searches across SubdivisionName, MLSAreaMajor, and MLSAreaMinor for comprehensive coverage
- **Fallback Logic**: Automatically provides alternative results when specific neighborhoods have no listings

### Address-Based Market Analysis
- "analyze market for 8604 Dorotha Ct, Austin, TX 78759"
- "market analysis around 123 Main Street, Dallas TX 75201"
- "what's the market like near 456 Oak Ave, Houston, TX 77001"
- "market trends within 2 miles of 789 Pine St, San Antonio TX 78205"

**Address-Based Analysis Features:**
- **Radius Analysis**: Analyze market around specific addresses within 0.1 to 5 miles
- **Property Context**: Shows target property details alongside market analysis
- **Coordinate-Based**: Uses exact coordinates for precise radius searches
- **Smart Fallbacks**: Falls back to ZIP code analysis if address not found or coordinates unavailable

## Search Filters

You can also use specific filters:

- **Location**: city, state, zip_code
- **Neighborhood**: neighborhood, subdivision, mls_area_major, mls_area_minor
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
6. **Neighborhood searches**: Use partial names for neighborhoods - the system will find close matches
7. **No results?**: The system will suggest available neighborhoods when your search doesn't match exactly
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
- **Authentication**: Valid token {'available' if self.settings.bridge_server_token else 'unavailable'}
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

### Scenario 4: Neighborhood-Specific Search
**Goal**: Find properties in specific neighborhoods or subdivisions

**Step 1**: Use natural language with neighborhood names
```
Query: "homes in Austin Woods neighborhood"
Query: "properties in Barton Hills Austin TX"
Query: "houses in Circle C Ranch subdivision under $700k"
```

**Step 2**: Try partial neighborhood names if needed
```
Query: "homes in Mueller" (will find Mueller Development)
Query: "properties in Steiner Ranch" (will find Steiner Ranch Community)
```

**Step 3**: Use fallback suggestions when no exact matches
```
If your neighborhood search returns no results, the system will:
- Suggest similar neighborhoods with available properties
- Show you what subdivisions are available in that city
- Provide alternative search options
```

**Step 4**: Combine neighborhood with other criteria
```
Filters: {
  "neighborhood": "Austin Woods",
  "city": "Austin",
  "state": "TX",
  "min_bedrooms": 3,
  "max_price": 600000
}
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
5. **Neighborhood searches**: Try partial neighborhood names or check system suggestions for available subdivisions

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

### Scenario 3: Address-Based Market Analysis
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

**Step 4**: Interpret radius-based results
- **Tight radius (0.1-0.5 miles)**: Immediate neighborhood conditions
- **Medium radius (0.5-1.5 miles)**: Local area market dynamics  
- **Wide radius (1.5-5.0 miles)**: Broader market context

**Market Insights:**
- Compare target property to neighborhood averages
- Identify pricing opportunities or concerns
- Understand local market velocity and trends

### Scenario 4: Investment Market Selection
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

