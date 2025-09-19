"""MCP server implementation for UNLOCK MLS RESO data access with HTTP Remote transport."""

import asyncio
import uvicorn
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from mcp.server import Server
from mcp.server.http import http_server
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

class UnlockMlsHttpServer:
    """MCP server for UNLOCK MLS RESO data access with HTTP transport."""
    
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
        
        # Create FastAPI app
        self.app = FastAPI(
            title="UNLOCK MLS MCP Server",
            description="MCP server for UNLOCK MLS real estate data via Bridge Interactive's RESO API",
            version="1.0.0"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Create MCP server instance
        self.server = Server("unlock-mls-mcp")
        self._setup_handlers()
        self._setup_http_routes()
        
        logger.info("UnlockMlsHttpServer initialized")
    
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
                                        "description": "Minor MLS marketing area"
                                    },
                                    "school_district": {
                                        "type": "string",
                                        "description": "School district name"
                                    },
                                    "elementary_school": {
                                        "type": "string",
                                        "description": "Elementary school name"
                                    },
                                    "middle_school": {
                                        "type": "string",
                                        "description": "Middle school name"
                                    },
                                    "high_school": {
                                        "type": "string",
                                        "description": "High school name"
                                    },
                                    "year_built_min": {
                                        "type": "integer",
                                        "description": "Minimum year built"
                                    },
                                    "year_built_max": {
                                        "type": "integer",
                                        "description": "Maximum year built"
                                    },
                                    "lot_size_min": {
                                        "type": "number",
                                        "description": "Minimum lot size in acres"
                                    },
                                    "lot_size_max": {
                                        "type": "number",
                                        "description": "Maximum lot size in acres"
                                    },
                                    "has_pool": {
                                        "type": "boolean",
                                        "description": "Property has swimming pool"
                                    },
                                    "has_garage": {
                                        "type": "boolean",
                                        "description": "Property has garage"
                                    },
                                    "has_fireplace": {
                                        "type": "boolean",
                                        "description": "Property has fireplace"
                                    },
                                    "has_central_air": {
                                        "type": "boolean",
                                        "description": "Property has central air conditioning"
                                    },
                                    "has_central_heat": {
                                        "type": "boolean",
                                        "description": "Property has central heating"
                                    },
                                    "has_dishwasher": {
                                        "type": "boolean",
                                        "description": "Property has dishwasher"
                                    },
                                    "has_microwave": {
                                        "type": "boolean",
                                        "description": "Property has microwave"
                                    },
                                    "has_refrigerator": {
                                        "type": "boolean",
                                        "description": "Property has refrigerator"
                                    },
                                    "has_washer": {
                                        "type": "boolean",
                                        "description": "Property has washer"
                                    },
                                    "has_dryer": {
                                        "type": "boolean",
                                        "description": "Property has dryer"
                                    },
                                    "has_ceiling_fans": {
                                        "type": "boolean",
                                        "description": "Property has ceiling fans"
                                    },
                                    "has_blinds": {
                                        "type": "boolean",
                                        "description": "Property has blinds"
                                    },
                                    "has_carpet": {
                                        "type": "boolean",
                                        "description": "Property has carpet"
                                    },
                                    "has_hardwood": {
                                        "type": "boolean",
                                        "description": "Property has hardwood floors"
                                    },
                                    "has_tile": {
                                        "type": "boolean",
                                        "description": "Property has tile floors"
                                    },
                                    "has_vinyl": {
                                        "type": "boolean",
                                        "description": "Property has vinyl floors"
                                    },
                                    "has_laminate": {
                                        "type": "boolean",
                                        "description": "Property has laminate floors"
                                    },
                                    "has_concrete": {
                                        "type": "boolean",
                                        "description": "Property has concrete floors"
                                    },
                                    "has_other_flooring": {
                                        "type": "boolean",
                                        "description": "Property has other flooring"
                                    },
                                    "has_other_appliances": {
                                        "type": "boolean",
                                        "description": "Property has other appliances"
                                    },
                                    "has_other_features": {
                                        "type": "boolean",
                                        "description": "Property has other features"
                                    }
                                }
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of properties to return (default: 50, max: 100)",
                                "default": 50
                            },
                            "offset": {
                                "type": "integer",
                                "description": "Number of properties to skip for pagination (default: 0)",
                                "default": 0
                            }
                        }
                    }
                ),
                Tool(
                    name="get_property_details",
                    description="Get detailed information about a specific property by MLS ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "mls_id": {
                                "type": "string",
                                "description": "MLS ID of the property"
                            }
                        },
                        "required": ["mls_id"]
                    }
                ),
                Tool(
                    name="get_market_analysis",
                    description="Get market analysis and trends for a specific area",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "City name for market analysis"
                            },
                            "state": {
                                "type": "string",
                                "description": "State abbreviation (e.g., TX, CA)"
                            },
                            "zip_code": {
                                "type": "string",
                                "description": "ZIP code for market analysis"
                            },
                            "property_type": {
                                "type": "string",
                                "enum": ["residential", "condo", "townhouse", "single_family", 
                                        "multi_family", "manufactured", "land", "commercial", "business"],
                                "description": "Property type for analysis"
                            },
                            "analysis_type": {
                                "type": "string",
                                "enum": ["price_trends", "inventory_levels", "days_on_market", 
                                        "comprehensive", "comparative_analysis"],
                                "description": "Type of market analysis to perform",
                                "default": "comprehensive"
                            }
                        }
                    }
                )
            ]
            return tools

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
            """Handle tool calls."""
            try:
                if name == "search_properties":
                    return await self._handle_search_properties(arguments)
                elif name == "get_property_details":
                    return await self._handle_get_property_details(arguments)
                elif name == "get_market_analysis":
                    return await self._handle_get_market_analysis(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
            except Exception as e:
                logger.error("Tool call failed: %s", e, exc_info=True)
                raise

        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            """List available resources."""
            return []

        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """Read a resource."""
            raise ValueError(f"Unknown resource: {uri}")

    def _setup_http_routes(self):
        """Set up HTTP routes for the FastAPI app."""
        
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {
                "message": "UNLOCK MLS MCP Server",
                "version": "1.0.0",
                "transport": "HTTP Remote",
                "status": "running"
            }
        
        @self.app.get("/health")
        async def health():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "timestamp": self._get_current_timestamp()
            }
        
        @self.app.get("/tools")
        async def list_tools():
            """List available tools via HTTP."""
            try:
                tools = await self.server._handlers.list_tools()
                return {"tools": tools}
            except Exception as e:
                logger.error("Failed to list tools: %s", e)
                raise HTTPException(status_code=500, detail=str(e))

    async def _handle_search_properties(self, arguments: Dict[str, Any]) -> list[TextContent]:
        """Handle property search."""
        # Implementation would be copied from the original server
        # This is a placeholder - you'll need to copy the full implementation
        return [TextContent(type="text", text="Property search functionality")]

    async def _handle_get_property_details(self, arguments: Dict[str, Any]) -> list[TextContent]:
        """Handle property details retrieval."""
        # Implementation would be copied from the original server
        return [TextContent(type="text", text="Property details functionality")]

    async def _handle_get_market_analysis(self, arguments: Dict[str, Any]) -> list[TextContent]:
        """Handle market analysis."""
        # Implementation would be copied from the original server
        return [TextContent(type="text", text="Market analysis functionality")]

    def _get_current_timestamp(self) -> str:
        """Get current timestamp for status reporting."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    async def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the MCP server with HTTP transport."""
        logger.info("Starting UNLOCK MLS MCP server with HTTP transport")
        
        try:
            # Verify Bearer token is available
            if not self.settings.bridge_server_token:
                raise ValueError("Bridge server token is required")
            logger.info("Authentication configured with Bearer token")
            
            # Create HTTP server
            config = uvicorn.Config(
                self.app,
                host=host,
                port=port,
                log_level="info"
            )
            server = uvicorn.Server(config)
            
            # Run the server
            await server.serve()
            
        except Exception as e:
            logger.error("Failed to start server: %s", e, exc_info=True)
            raise

def main():
    """Main entry point."""
    server = UnlockMlsHttpServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main()
