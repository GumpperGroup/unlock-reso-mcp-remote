"""Google Maps Places API (New) client for location resolution."""

import asyncio
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
import json

import aiohttp
from aiohttp import ClientError, ClientResponseError

from ..config.settings import get_settings
from ..config.logging_config import setup_logging

logger = setup_logging(__name__)


class GooglePlacesError(Exception):
    """Base exception for Google Places API related errors."""
    pass


class GooglePlacesRateLimitError(GooglePlacesError):
    """Raised when Google Places API rate limit is exceeded."""
    pass


class GooglePlacesNotFoundError(GooglePlacesError):
    """Raised when a location is not found."""
    pass


class LocationCache:
    """Simple in-memory cache for location resolutions."""

    def __init__(self, ttl_hours: int = 24, max_size: int = 1000):
        """
        Initialize location cache.

        Args:
            ttl_hours: Time to live for cached entries in hours
            max_size: Maximum number of entries to cache
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl_hours = ttl_hours
        self._max_size = max_size

    def _generate_key(self, location: str) -> str:
        """Generate cache key from location string."""
        normalized = location.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()

    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """Check if cache entry is expired."""
        expiry = entry.get('expires_at', 0)
        return time.time() > expiry

    def _cleanup_expired(self):
        """Remove expired entries from cache."""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.get('expires_at', 0) <= current_time
        ]
        for key in expired_keys:
            del self._cache[key]

    def get(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Get coordinates from cache.

        Args:
            location: Location string to look up

        Returns:
            Tuple of (latitude, longitude) if found and not expired, None otherwise
        """
        self._cleanup_expired()

        key = self._generate_key(location)
        entry = self._cache.get(key)

        if entry and not self._is_expired(entry):
            coords = entry.get('coordinates')
            if coords:
                logger.debug("Cache hit for location: %s", location)
                return coords

        return None

    def set(self, location: str, latitude: float, longitude: float):
        """
        Store coordinates in cache.

        Args:
            location: Location string
            latitude: Latitude coordinate
            longitude: Longitude coordinate
        """
        # Enforce max size with LRU eviction
        if len(self._cache) >= self._max_size:
            # Remove oldest entry
            oldest_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k].get('created_at', 0)
            )
            del self._cache[oldest_key]

        key = self._generate_key(location)
        expires_at = time.time() + (self._ttl_hours * 3600)

        self._cache[key] = {
            'coordinates': (latitude, longitude),
            'created_at': time.time(),
            'expires_at': expires_at
        }

        logger.debug("Cached coordinates for location: %s", location)

    def clear(self):
        """Clear all cached entries."""
        self._cache.clear()
        logger.debug("Location cache cleared")

    def stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        self._cleanup_expired()
        return {
            'total_entries': len(self._cache),
            'max_size': self._max_size,
            'ttl_hours': self._ttl_hours
        }


class GooglePlacesClient:
    """Client for Google Maps Places API (New)."""

    def __init__(self,
                 api_key: Optional[str] = None,
                 enable_caching: Optional[bool] = None,
                 cache_ttl_hours: Optional[int] = None,
                 max_requests_per_day: Optional[int] = None):
        """
        Initialize Google Places API client.

        Args:
            api_key: Google Maps API key (defaults to settings)
            enable_caching: Enable location caching (defaults to settings)
            cache_ttl_hours: Cache TTL in hours (defaults to settings)
            max_requests_per_day: Daily request limit (defaults to settings)
        """
        self.settings = get_settings()

        self.api_key = api_key or self.settings.google_maps_api_key
        self.enable_caching = enable_caching if enable_caching is not None else self.settings.google_maps_enable_caching
        self.max_requests_per_day = max_requests_per_day or self.settings.google_maps_max_requests_per_day

        if not self.api_key:
            raise GooglePlacesError("Google Maps API key is required")

        # Initialize cache if enabled
        self.cache = None
        if self.enable_caching:
            cache_ttl = cache_ttl_hours or self.settings.google_maps_cache_ttl_hours
            self.cache = LocationCache(ttl_hours=cache_ttl)

        # Request tracking for rate limiting
        self._request_count = 0
        self._request_date = datetime.now().date()

        # API configuration
        self.base_url = "https://places.googleapis.com/v1/places"
        self.timeout = aiohttp.ClientTimeout(total=10, connect=5)

        logger.info("GooglePlacesClient initialized with caching: %s", self.enable_caching)

    def _check_rate_limit(self):
        """Check if we're within daily rate limits."""
        current_date = datetime.now().date()

        # Reset counter if it's a new day
        if current_date != self._request_date:
            self._request_count = 0
            self._request_date = current_date

        if self._request_count >= self.max_requests_per_day:
            raise GooglePlacesRateLimitError(
                f"Daily rate limit of {self.max_requests_per_day} requests exceeded"
            )

    def _increment_request_count(self):
        """Increment request counter."""
        self._request_count += 1
        logger.debug("Request count: %d/%d", self._request_count, self.max_requests_per_day)

    async def _make_request(self,
                          session: aiohttp.ClientSession,
                          method: str,
                          endpoint: str,
                          **kwargs) -> Dict[str, Any]:
        """
        Make an authenticated request to the Google Places API.

        Args:
            session: aiohttp client session
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request parameters

        Returns:
            Parsed JSON response

        Raises:
            GooglePlacesError: If request fails
        """
        try:
            # Check rate limits
            self._check_rate_limit()

            url = f"{self.base_url}{endpoint}"

            # Add API key authentication
            headers = kwargs.get('headers', {})
            headers.update({
                'X-Goog-Api-Key': self.api_key,
                'Content-Type': 'application/json'
            })
            kwargs['headers'] = headers
            kwargs['timeout'] = self.timeout

            logger.debug("Making %s request to: %s", method, endpoint)

            response = await session.request(method, url, **kwargs)
            self._increment_request_count()

            # Handle different response statuses
            if response.status == 200:
                data = await response.json()
                return data
            elif response.status == 400:
                error_text = await response.text()
                raise GooglePlacesError(f"Bad request: {error_text}")
            elif response.status == 401:
                raise GooglePlacesError("Invalid API key or authentication failed")
            elif response.status == 403:
                raise GooglePlacesError("API access forbidden - check API key permissions")
            elif response.status == 429:
                raise GooglePlacesRateLimitError("Rate limit exceeded")
            elif response.status == 404:
                raise GooglePlacesNotFoundError("Location not found")
            else:
                response.raise_for_status()

        except aiohttp.ClientError as e:
            logger.error("HTTP error in Google Places API request: %s", str(e))
            raise GooglePlacesError(f"Network error: {str(e)}")
        except Exception as e:
            if isinstance(e, (GooglePlacesError, GooglePlacesRateLimitError, GooglePlacesNotFoundError)):
                raise
            logger.error("Unexpected error in Google Places API request: %s", str(e))
            raise GooglePlacesError(f"Unexpected error: {str(e)}")

    async def resolve_location_to_coordinates(self, location: str) -> Tuple[float, float]:
        """
        Resolve a location string to coordinates using Google Places API.

        Args:
            location: Location name, address, or point of interest

        Returns:
            Tuple of (latitude, longitude)

        Raises:
            GooglePlacesError: If location resolution fails
            GooglePlacesNotFoundError: If location is not found
            GooglePlacesRateLimitError: If rate limit is exceeded
        """
        if not location or not location.strip():
            raise GooglePlacesError("Location string cannot be empty")

        location = location.strip()

        # Check cache first
        if self.cache:
            cached_coords = self.cache.get(location)
            if cached_coords:
                return cached_coords

        # Prepare text search request
        request_data = {
            "textQuery": location,
            "maxResultCount": 1
        }

        async with aiohttp.ClientSession() as session:
            try:
                # Use Text Search endpoint for location resolution
                headers = {
                    'X-Goog-FieldMask': 'places.location,places.displayName'
                }
                response = await self._make_request(
                    session,
                    'POST',
                    ':searchText',
                    json=request_data,
                    headers=headers
                )

                # Extract coordinates from response
                places = response.get('places', [])
                if not places:
                    raise GooglePlacesNotFoundError(f"Location '{location}' not found")

                place = places[0]
                location_data = place.get('location', {})

                latitude = location_data.get('latitude')
                longitude = location_data.get('longitude')

                if latitude is None or longitude is None:
                    raise GooglePlacesError(f"Invalid coordinates received for location '{location}'")

                coordinates = (float(latitude), float(longitude))

                # Cache the result
                if self.cache:
                    self.cache.set(location, coordinates[0], coordinates[1])

                logger.info("Resolved location '%s' to coordinates: %s", location, coordinates)
                return coordinates

            except (GooglePlacesError, GooglePlacesRateLimitError, GooglePlacesNotFoundError):
                raise
            except Exception as e:
                logger.error("Unexpected error resolving location '%s': %s", location, str(e))
                raise GooglePlacesError(f"Failed to resolve location '{location}': {str(e)}")

    async def find_nearby_places(self,
                                latitude: float,
                                longitude: float,
                                radius_meters: float = 1000,
                                place_types: Optional[List[str]] = None,
                                max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Find places near given coordinates.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius_meters: Search radius in meters
            place_types: List of place types to search for
            max_results: Maximum number of results to return

        Returns:
            List of place information dictionaries

        Raises:
            GooglePlacesError: If search fails
        """
        if not (-90 <= latitude <= 90):
            raise GooglePlacesError(f"Invalid latitude: {latitude}")
        if not (-180 <= longitude <= 180):
            raise GooglePlacesError(f"Invalid longitude: {longitude}")
        if radius_meters <= 0 or radius_meters > 50000:
            raise GooglePlacesError(f"Invalid radius: {radius_meters}. Must be between 0 and 50000 meters")

        # Prepare nearby search request
        request_data = {
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "radius": radius_meters
                }
            },
            "maxResultCount": min(max_results, 20),  # API limit is 20
            "rankPreference": "DISTANCE"
        }

        # Add place types if specified
        if place_types:
            request_data["includedTypes"] = place_types

        async with aiohttp.ClientSession() as session:
            try:
                # Add field mask for nearby search
                headers = {
                    'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.location,places.rating,places.types'
                }
                response = await self._make_request(
                    session,
                    'POST',
                    ':searchNearby',
                    json=request_data,
                    headers=headers
                )

                places = response.get('places', [])

                logger.info("Found %d places near coordinates (%f, %f)",
                          len(places), latitude, longitude)

                return places

            except (GooglePlacesError, GooglePlacesRateLimitError):
                raise
            except Exception as e:
                logger.error("Unexpected error finding nearby places: %s", str(e))
                raise GooglePlacesError(f"Failed to find nearby places: {str(e)}")

    def get_cache_stats(self) -> Optional[Dict[str, int]]:
        """
        Get cache statistics.

        Returns:
            Cache statistics dictionary or None if caching is disabled
        """
        if self.cache:
            return self.cache.stats()
        return None

    def clear_cache(self):
        """Clear location cache."""
        if self.cache:
            self.cache.clear()

    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get API usage statistics.

        Returns:
            Usage statistics dictionary
        """
        return {
            'requests_today': self._request_count,
            'daily_limit': self.max_requests_per_day,
            'remaining_requests': max(0, self.max_requests_per_day - self._request_count),
            'request_date': self._request_date.isoformat(),
            'cache_enabled': self.enable_caching,
            'cache_stats': self.get_cache_stats()
        }


# Convenience functions for common operations
async def resolve_location(location: str) -> Tuple[float, float]:
    """
    Convenience function to resolve a location to coordinates.

    Args:
        location: Location string to resolve

    Returns:
        Tuple of (latitude, longitude)
    """
    client = GooglePlacesClient()
    return await client.resolve_location_to_coordinates(location)


async def find_places_near_location(location: str,
                                  radius_meters: float = 1000,
                                  place_types: Optional[List[str]] = None,
                                  max_results: int = 20) -> List[Dict[str, Any]]:
    """
    Convenience function to find places near a location.

    Args:
        location: Location string
        radius_meters: Search radius in meters
        place_types: List of place types to search for
        max_results: Maximum number of results

    Returns:
        List of place information dictionaries
    """
    client = GooglePlacesClient()

    # First resolve location to coordinates
    latitude, longitude = await client.resolve_location_to_coordinates(location)

    # Then find nearby places
    return await client.find_nearby_places(
        latitude=latitude,
        longitude=longitude,
        radius_meters=radius_meters,
        place_types=place_types,
        max_results=max_results
    )