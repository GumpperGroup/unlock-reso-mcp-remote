"""RESO Web API client for Bridge Interactive endpoints."""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from urllib.parse import quote, urlencode
import logging

import aiohttp
from aiohttp import ClientError, ClientResponseError

from .config.settings import settings
from .config.logging_config import setup_logging

logger = setup_logging(__name__)


class ResoApiError(Exception):
    """Base exception for RESO API related errors."""
    pass


class ResoWebApiClient:
    """Client for Bridge Interactive RESO Web API."""
    
    def __init__(self,
                 base_url: Optional[str] = None,
                 mls_id: Optional[str] = None,
                 server_token: Optional[str] = None):
        """
        Initialize RESO Web API client.
        
        Args:
            base_url: API base URL (defaults to settings)
            mls_id: MLS identifier (defaults to settings)
            server_token: Bearer token (defaults to settings)
        """
        self.base_url = base_url or settings.bridge_api_base_url
        self.mls_id = mls_id or settings.bridge_mls_id
        self.server_token = server_token or settings.bridge_server_token
        
        # Build OData endpoint URL
        self.odata_endpoint = f"{self.base_url}/OData/{self.mls_id}"
        
        # Resource endpoints
        self.endpoints = {
            "Property": f"{self.odata_endpoint}/Property",
            "Member": f"{self.odata_endpoint}/Member", 
            "Office": f"{self.odata_endpoint}/Office",
            "OpenHouse": f"{self.odata_endpoint}/OpenHouse",
            "Media": f"{self.odata_endpoint}/Media",
            "Lookup": f"{self.odata_endpoint}/Lookup"
        }
        
        # Default timeout
        self.timeout = aiohttp.ClientTimeout(total=30, connect=10)
        
        logger.info("ResoWebApiClient initialized for MLS: %s", self.mls_id)
    
    async def _make_request(self,
                          session: aiohttp.ClientSession,
                          method: str,
                          url: str,
                          **kwargs) -> Dict[str, Any]:
        """
        Make an authenticated request to the RESO API.
        
        Args:
            session: aiohttp client session
            method: HTTP method
            url: Request URL
            **kwargs: Additional request parameters
            
        Returns:
            Parsed JSON response
            
        Raises:
            ResoApiError: If request fails
        """
        try:
            # Add Bearer token authentication
            headers = kwargs.get('headers', {})
            headers.update({
                'Authorization': f'Bearer {self.server_token}',
                'Accept': 'application/json',
                'User-Agent': 'UNLOCK-MLS-MCP-Server/1.0'
            })
            kwargs['headers'] = headers
            kwargs['timeout'] = self.timeout
            
            response = await session.request(method, url, **kwargs)
            
            response.raise_for_status()
            
            # Handle different content types
            content_type = response.headers.get("content-type", "").lower()
            if "application/json" in content_type:
                data = await response.json()
            else:
                text = await response.text()
                raise ResoApiError(f"Unexpected content type: {content_type}. Response: {text}")
            
            logger.debug("API request successful: %s %s", method, url)
            return data
            
        except ClientResponseError as e:
            error_msg = f"HTTP {e.status}: {e.message}"
            if e.status == 400:
                error_msg = "Bad request - check query parameters"
            elif e.status == 403:
                error_msg = "Forbidden - check permissions for this MLS"
            elif e.status == 404:
                error_msg = "Resource not found"
            elif e.status == 429:
                error_msg = "Rate limit exceeded"
            elif e.status >= 500:
                error_msg = "Server error - try again later"
            
            logger.error("API request failed: %s %s - %s", method, url, error_msg)
            raise ResoApiError(error_msg) from e
            
        except Exception as auth_error:
            # Handle any authentication-related errors
            if "auth" in str(auth_error).lower():
                logger.error("Authentication failed: %s", str(auth_error))
                raise ResoApiError(f"Authentication failed: {str(auth_error)}") from auth_error
            # Re-raise if not authentication related
            raise
            
        except ClientError as e:
            logger.error("Network error: %s", str(e))
            raise ResoApiError(f"Network error: {str(e)}") from e
            
        except Exception as e:
            logger.error("Unexpected error: %s", str(e))
            raise ResoApiError(f"Unexpected error: {str(e)}") from e
    
    def _build_odata_query(self, **params) -> str:
        """
        Build OData query parameters.
        
        Args:
            **params: Query parameters
            
        Returns:
            OData query string
        """
        query_parts = []
        
        # Handle common OData parameters
        if params.get("filter"):
            query_parts.append(f"$filter={quote(params['filter'])}")
        
        if params.get("select"):
            fields = params["select"]
            if isinstance(fields, list):
                fields = ",".join(fields)
            query_parts.append(f"$select={quote(fields)}")
        
        if params.get("orderby"):
            query_parts.append(f"$orderby={quote(params['orderby'])}")
        
        if params.get("top"):
            query_parts.append(f"$top={params['top']}")
        
        if params.get("skip"):
            query_parts.append(f"$skip={params['skip']}")
        
        if params.get("expand"):
            query_parts.append(f"$expand={quote(params['expand'])}")
        
        if params.get("count"):
            query_parts.append("$count=true")
        
        return "&".join(query_parts)
    
    def _build_property_filter(self,
                             city: Optional[str] = None,
                             state: Optional[str] = None,
                             zip_code: Optional[str] = None,
                             min_price: Optional[float] = None,
                             max_price: Optional[float] = None,
                             min_bedrooms: Optional[int] = None,
                             max_bedrooms: Optional[int] = None,
                             min_bathrooms: Optional[float] = None,
                             max_bathrooms: Optional[float] = None,
                             min_sqft: Optional[int] = None,
                             max_sqft: Optional[int] = None,
                             property_type: Optional[str] = None,
                             property_subtype: Optional[str] = None,
                             status: Optional[str] = None,
                             listing_id: Optional[str] = None,
                             **kwargs) -> str:
        """
        Build a filter string for property queries.
        
        Args:
            city: City name
            state: State code
            zip_code: ZIP/postal code
            min_price: Minimum price
            max_price: Maximum price
            min_bedrooms: Minimum bedrooms
            max_bedrooms: Maximum bedrooms
            min_bathrooms: Minimum bathrooms
            max_bathrooms: Maximum bathrooms
            min_sqft: Minimum square footage
            max_sqft: Maximum square footage
            property_type: Property type
            property_subtype: Property subtype
            status: Property status
            listing_id: Specific listing ID
            **kwargs: Additional filter parameters
            
        Returns:
            OData filter string
        """
        filters = []
        
        # Always filter to active listings unless status specified
        if status:
            filters.append(f"StandardStatus eq '{status}'")
        else:
            filters.append("StandardStatus eq 'Active'")
        
        # Location filters
        if city:
            filters.append(f"City eq '{city}'")
        
        if state:
            filters.append(f"StateOrProvince eq '{state}'")
        
        if zip_code:
            filters.append(f"PostalCode eq '{zip_code}'")
        
        # Price filters
        if min_price is not None:
            filters.append(f"ListPrice ge {min_price}")
        
        if max_price is not None:
            filters.append(f"ListPrice le {max_price}")
        
        # Bedroom filters
        if min_bedrooms is not None:
            filters.append(f"BedroomsTotal ge {min_bedrooms}")
        
        if max_bedrooms is not None:
            filters.append(f"BedroomsTotal le {max_bedrooms}")
        
        # Bathroom filters
        if min_bathrooms is not None:
            filters.append(f"BathroomsTotalInteger ge {min_bathrooms}")
        
        if max_bathrooms is not None:
            filters.append(f"BathroomsTotalInteger le {max_bathrooms}")
        
        # Square footage filters
        if min_sqft is not None:
            filters.append(f"LivingArea ge {min_sqft}")
        
        if max_sqft is not None:
            filters.append(f"LivingArea le {max_sqft}")
        
        # Property type filters
        if property_type:
            filters.append(f"PropertyType eq '{property_type}'")
        
        if property_subtype:
            filters.append(f"PropertySubType eq '{property_subtype}'")
        
        # Specific listing
        if listing_id:
            filters.append(f"ListingId eq '{listing_id}'")
        
        # Additional custom filters
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, str):
                    # Use flexible matching for subdivision/neighborhood searches
                    if key in ['SubdivisionName', 'MLSAreaMajor', 'MLSAreaMinor']:
                        # Use contains for neighborhood searches to be more flexible
                        filters.append(f"contains({key}, '{value}')")
                    elif key == 'UnparsedAddress':
                        # Use case-insensitive matching for addresses
                        filters.append(f"tolower({key}) eq '{value.lower()}'")
                    else:
                        filters.append(f"{key} eq '{value}'")
                else:
                    filters.append(f"{key} eq {value}")
        
        return " and ".join(filters)
    
    async def query_properties(self,
                             filters: Optional[Dict[str, Any]] = None,
                             select_fields: Optional[List[str]] = None,
                             order_by: Optional[str] = None,
                             limit: int = 25,
                             offset: int = 0) -> List[Dict[str, Any]]:
        """
        Query properties from the RESO API.
        
        Args:
            filters: Property filter criteria
            select_fields: Fields to select
            order_by: Sort order
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of property records
            
        Raises:
            ResoApiError: If query fails
        """
        logger.info("Querying properties with filters: %s", filters)
        
        # Build query parameters
        query_params = {
            "top": min(limit, 200),  # API maximum
            "skip": offset
        }
        
        # Add filter (always include default status filter)
        if filters:
            filter_str = self._build_property_filter(**filters)
        else:
            filter_str = self._build_property_filter()
        
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
                logger.info("Retrieved %d properties", len(results))
                return results
            else:
                logger.warning("Unexpected response format: %s", data)
                return []
    
    async def get_property(self, listing_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific property by listing ID.
        
        Args:
            listing_id: Property listing ID
            
        Returns:
            Property record or None if not found
            
        Raises:
            ResoApiError: If query fails
        """
        logger.info("Getting property: %s", listing_id)
        
        try:
            results = await self.query_properties(
                filters={"listing_id": listing_id},
                limit=1
            )
            
            if results:
                return results[0]
            else:
                logger.info("Property not found: %s", listing_id)
                return None
                
        except ResoApiError as e:
            if "not found" in str(e).lower():
                return None
            raise
    
    async def query_properties_raw(self, filter_str: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Query properties using raw OData filter string.
        
        Args:
            filter_str: Raw OData filter expression
            limit: Maximum number of results
            
        Returns:
            List of property records
        """
        logger.info("Querying properties with raw filter: %s", filter_str)
        
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
            # First try with exact match using filter parameter
            results = await self.query_properties(
                filters={"UnparsedAddress": address},
                limit=5  # Get a few results in case of variations
            )
            
            if results:
                # Return the first match
                return results[0]
            else:
                # Try with case-insensitive raw query as fallback
                results = await self.query_properties_raw(
                    filter_str=f"tolower(UnparsedAddress) eq '{address.lower()}'",
                    limit=5
                )
                return results[0] if results else None
                
        except Exception as e:
            logger.error("Error finding property by address: %s", str(e))
            return None
    
    async def query_properties_by_coordinates(self,
                                            filters: Optional[Dict[str, Any]] = None,
                                            limit: int = 25) -> List[Dict[str, Any]]:
        """
        Query properties around specific coordinates using geo.distance.
        
        Args:
            filters: Filters including latitude, longitude, radius_miles
            limit: Maximum number of results
            
        Returns:
            List of property records within radius
        """
        if not filters or not all(k in filters for k in ['latitude', 'longitude', 'radius_miles']):
            raise ValueError("latitude, longitude, and radius_miles are required")
        
        latitude = filters['latitude']
        longitude = filters['longitude'] 
        radius_miles = filters['radius_miles']
        
        logger.info("Querying properties around coordinates: %f, %f within %f miles", 
                   latitude, longitude, radius_miles)
        
        # Build geo.distance filter
        geo_filter = f"geo.distance(Coordinates, POINT({longitude} {latitude})) lt {radius_miles}"
        
        # Add other filters
        additional_filters = []
        
        # Status filter
        status = filters.get('status', 'Active')
        if status.lower() == 'active':
            additional_filters.append("StandardStatus eq 'Active'")
        elif status.lower() == 'sold':
            additional_filters.append("(StandardStatus eq 'Sold' or StandardStatus eq 'Closed')")
        
        # Property type filter
        if filters.get('property_type'):
            additional_filters.append(f"PropertyType eq '{filters['property_type']}'")
        
        # Combine all filters
        all_filters = [geo_filter] + additional_filters
        filter_str = " and ".join(all_filters)
        
        return await self.query_properties_raw(filter_str, limit)
    
    async def query_members(self,
                          filters: Optional[Dict[str, Any]] = None,
                          select_fields: Optional[List[str]] = None,
                          limit: int = 25,
                          offset: int = 0) -> List[Dict[str, Any]]:
        """
        Query members/agents from the RESO API.
        
        Args:
            filters: Member filter criteria
            select_fields: Fields to select
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of member records
        """
        logger.info("Querying members with filters: %s", filters)
        
        query_params = {
            "top": min(limit, 200),
            "skip": offset
        }
        
        if select_fields:
            query_params["select"] = select_fields
        
        if filters:
            filter_parts = []
            for key, value in filters.items():
                if isinstance(value, str):
                    filter_parts.append(f"{key} eq '{value}'")
                else:
                    filter_parts.append(f"{key} eq {value}")
            
            if filter_parts:
                query_params["filter"] = " and ".join(filter_parts)
        
        query_string = self._build_odata_query(**query_params)
        url = f"{self.endpoints['Member']}?{query_string}"
        
        async with aiohttp.ClientSession() as session:
            data = await self._make_request(session, "GET", url)
            return data.get("value", [])
    
    async def query_offices(self,
                          filters: Optional[Dict[str, Any]] = None,
                          select_fields: Optional[List[str]] = None,
                          limit: int = 25,
                          offset: int = 0) -> List[Dict[str, Any]]:
        """
        Query offices from the RESO API.
        
        Args:
            filters: Office filter criteria
            select_fields: Fields to select  
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of office records
        """
        logger.info("Querying offices with filters: %s", filters)
        
        query_params = {
            "top": min(limit, 200),
            "skip": offset
        }
        
        if select_fields:
            query_params["select"] = select_fields
        
        if filters:
            filter_parts = []
            for key, value in filters.items():
                if isinstance(value, str):
                    filter_parts.append(f"{key} eq '{value}'")
                else:
                    filter_parts.append(f"{key} eq {value}")
            
            if filter_parts:
                query_params["filter"] = " and ".join(filter_parts)
        
        query_string = self._build_odata_query(**query_params)
        url = f"{self.endpoints['Office']}?{query_string}"
        
        async with aiohttp.ClientSession() as session:
            data = await self._make_request(session, "GET", url)
            return data.get("value", [])
    
    async def query_open_houses(self,
                              filters: Optional[Dict[str, Any]] = None,
                              select_fields: Optional[List[str]] = None,
                              limit: int = 25,
                              offset: int = 0) -> List[Dict[str, Any]]:
        """
        Query open houses from the RESO API.
        
        Args:
            filters: Open house filter criteria
            select_fields: Fields to select
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of open house records
        """
        logger.info("Querying open houses with filters: %s", filters)
        
        query_params = {
            "top": min(limit, 200),
            "skip": offset
        }
        
        if select_fields:
            query_params["select"] = select_fields
        
        if filters:
            filter_parts = []
            for key, value in filters.items():
                if isinstance(value, str):
                    filter_parts.append(f"{key} eq '{value}'")
                else:
                    filter_parts.append(f"{key} eq {value}")
            
            if filter_parts:
                query_params["filter"] = " and ".join(filter_parts)
        
        query_string = self._build_odata_query(**query_params)
        url = f"{self.endpoints['OpenHouse']}?{query_string}"
        
        async with aiohttp.ClientSession() as session:
            data = await self._make_request(session, "GET", url)
            return data.get("value", [])
    
    async def get_lookup_values(self,
                              lookup_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get lookup values from the RESO API.
        
        Args:
            lookup_name: Specific lookup to retrieve
            
        Returns:
            Lookup data
        """
        logger.info("Getting lookup values: %s", lookup_name or "all")
        
        url = self.endpoints['Lookup']
        if lookup_name:
            url += f"('{lookup_name}')"
        
        async with aiohttp.ClientSession() as session:
            data = await self._make_request(session, "GET", url)
            return data
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the RESO API.
        
        Returns:
            Health check results
        """
        logger.info("Performing RESO API health check")
        
        try:
            # Test authentication by making a simple API call
            
            # Test basic property query with minimal results
            results = await self.query_properties(limit=1)
            
            return {
                "status": "healthy",
                "authentication": "ok",
                "api_access": "ok",
                "mls_id": self.mls_id,
                "endpoint": self.odata_endpoint,
                "sample_records": len(results)
            }
            
        except Exception as e:
            logger.error("Health check failed: %s", str(e))
            return {
                "status": "unhealthy",
                "error": str(e),
                "mls_id": self.mls_id,
                "endpoint": self.odata_endpoint
            }