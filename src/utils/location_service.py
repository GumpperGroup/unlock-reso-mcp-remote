"""Location service for property searches using Google Places API integration."""

import re
from typing import Dict, List, Optional, Any, Tuple, Union
import logging
import math

from .google_places_client import (
    GooglePlacesClient,
    GooglePlacesError,
    GooglePlacesNotFoundError,
    GooglePlacesRateLimitError
)
from ..config.logging_config import setup_logging

logger = setup_logging(__name__)


class LocationServiceError(Exception):
    """Base exception for location service errors."""
    pass


class LocationService:
    """Service for location-based property search coordination."""

    def __init__(self, google_places_client: Optional[GooglePlacesClient] = None):
        """
        Initialize location service.

        Args:
            google_places_client: Optional Google Places client (creates new if None)
        """
        self.google_places_client = google_places_client or GooglePlacesClient()

        # Distance calculation constants
        self.EARTH_RADIUS_MILES = 3959.0
        self.MILES_TO_METERS = 1609.34

        logger.info("LocationService initialized")

    def _validate_coordinates(self, latitude: float, longitude: float) -> None:
        """
        Validate latitude and longitude coordinates.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Raises:
            LocationServiceError: If coordinates are invalid
        """
        if not (-90 <= latitude <= 90):
            raise LocationServiceError(f"Invalid latitude: {latitude}. Must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise LocationServiceError(f"Invalid longitude: {longitude}. Must be between -180 and 180")

    def _validate_radius(self, radius_miles: float) -> None:
        """
        Validate search radius.

        Args:
            radius_miles: Search radius in miles

        Raises:
            LocationServiceError: If radius is invalid
        """
        if not (0.1 <= radius_miles <= 10.0):
            raise LocationServiceError(f"Invalid radius: {radius_miles}. Must be between 0.1 and 10.0 miles")

    def _miles_to_meters(self, miles: float) -> float:
        """Convert miles to meters."""
        return miles * self.MILES_TO_METERS

    def _meters_to_miles(self, meters: float) -> float:
        """Convert meters to miles."""
        return meters / self.MILES_TO_METERS

    def _calculate_distance_miles(self,
                                lat1: float, lon1: float,
                                lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points in miles using Haversine formula.

        Args:
            lat1: Latitude of first point
            lon1: Longitude of first point
            lat2: Latitude of second point
            lon2: Longitude of second point

        Returns:
            Distance in miles
        """
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = (math.sin(dlat/2)**2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))

        return self.EARTH_RADIUS_MILES * c

    def _extract_coordinates_from_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Try to extract coordinates from address string if it contains lat/lng.

        Args:
            address: Address string that might contain coordinates

        Returns:
            Tuple of (latitude, longitude) if found, None otherwise
        """
        # Look for patterns like "lat:30.2672, lng:-97.7431" or "30.2672,-97.7431"
        coord_patterns = [
            r'lat\s*:\s*([+-]?\d+\.?\d*)\s*,\s*lng\s*:\s*([+-]?\d+\.?\d*)',
            r'latitude\s*:\s*([+-]?\d+\.?\d*)\s*,\s*longitude\s*:\s*([+-]?\d+\.?\d*)',
            r'([+-]?\d+\.?\d+)\s*,\s*([+-]?\d+\.?\d+)'
        ]

        for pattern in coord_patterns:
            match = re.search(pattern, address, re.IGNORECASE)
            if match:
                try:
                    lat = float(match.group(1))
                    lng = float(match.group(2))
                    self._validate_coordinates(lat, lng)
                    return (lat, lng)
                except (ValueError, LocationServiceError):
                    continue

        return None

    def _is_address_like(self, location: str) -> bool:
        """
        Determine if location string looks like an address.

        Args:
            location: Location string to analyze

        Returns:
            True if it looks like an address, False otherwise
        """
        address_indicators = [
            r'\d+\s+[A-Za-z]',  # House number + street
            r'\b\d{5}(?:-\d{4})?\b',  # ZIP code
            r'\b(st|street|ave|avenue|rd|road|blvd|boulevard|dr|drive|ct|court|pl|place|ln|lane|way|pkwy|parkway)\b',
            r'\b(apt|apartment|unit|suite|ste)\s*\d+',  # Apartment/unit numbers
            r'\b[A-Z]{2}\s+\d{5}',  # State + ZIP
        ]

        location_lower = location.lower()
        return any(re.search(pattern, location_lower, re.IGNORECASE) for pattern in address_indicators)

    def _is_business_name(self, location: str) -> bool:
        """
        Determine if location string looks like a business name.

        Args:
            location: Location string to analyze

        Returns:
            True if it looks like a business name, False otherwise
        """
        business_indicators = [
            r'\b(starbucks|mcdonalds|walmart|target|home depot|costco|whole foods|trader joes)\b',
            r'\b(restaurant|cafe|coffee|shop|store|market|center|mall|plaza)\b',
            r'\b(university|college|school|hospital|church|bank)\b',
            r'\b(hotel|motel|inn|resort)\b',
            r'\b(park|trail|beach|lake|river)\b'
        ]

        location_lower = location.lower()
        return any(re.search(pattern, location_lower, re.IGNORECASE) for pattern in business_indicators)

    def _classify_location_type(self, location: str) -> str:
        """
        Classify the type of location string.

        Args:
            location: Location string to classify

        Returns:
            One of: 'coordinates', 'address', 'business', 'landmark', 'general'
        """
        if self._extract_coordinates_from_address(location):
            return 'coordinates'
        elif self._is_address_like(location):
            return 'address'
        elif self._is_business_name(location):
            return 'business'
        elif any(keyword in location.lower() for keyword in ['city hall', 'downtown', 'airport', 'station']):
            return 'landmark'
        else:
            return 'general'

    async def resolve_location_to_coordinates(self, location: str) -> Tuple[float, float]:
        """
        Resolve a location string to coordinates with multiple strategies.

        Args:
            location: Location string (address, business name, landmark, etc.)

        Returns:
            Tuple of (latitude, longitude)

        Raises:
            LocationServiceError: If location cannot be resolved
        """
        if not location or not location.strip():
            raise LocationServiceError("Location string cannot be empty")

        location = location.strip()
        location_type = self._classify_location_type(location)

        logger.info("Resolving location '%s' (type: %s)", location, location_type)

        try:
            # Try to extract coordinates directly if present
            if location_type == 'coordinates':
                coords = self._extract_coordinates_from_address(location)
                if coords:
                    return coords

            # Use Google Places API for resolution
            coordinates = await self.google_places_client.resolve_location_to_coordinates(location)

            logger.info("Successfully resolved '%s' to coordinates: %s", location, coordinates)
            return coordinates

        except GooglePlacesNotFoundError:
            # Provide helpful suggestions based on location type
            suggestions = self._get_location_suggestions(location, location_type)
            raise LocationServiceError(
                f"Location '{location}' not found. {suggestions}"
            )
        except GooglePlacesRateLimitError as e:
            raise LocationServiceError(f"Location service temporarily unavailable: {str(e)}")
        except GooglePlacesError as e:
            raise LocationServiceError(f"Failed to resolve location '{location}': {str(e)}")

    def _get_location_suggestions(self, location: str, location_type: str) -> str:
        """
        Generate helpful suggestions for location resolution failures.

        Args:
            location: Original location string
            location_type: Classified location type

        Returns:
            Suggestion string
        """
        if location_type == 'address':
            return (
                "Try including more details like city and state, "
                "or check the street name spelling."
            )
        elif location_type == 'business':
            return (
                "Try including the city or adding more specific details "
                "like the street name or neighborhood."
            )
        elif location_type == 'landmark':
            return (
                "Try including the city name or being more specific "
                "about the landmark location."
            )
        else:
            return (
                "Try being more specific with the location name, "
                "including city and state, or using a street address."
            )

    async def find_properties_near_coordinates(self,
                                             latitude: float,
                                             longitude: float,
                                             radius_miles: float,
                                             reso_client,
                                             property_filters: Optional[Dict[str, Any]] = None,
                                             limit: int = 25) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Find properties near given coordinates using RESO client.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius_miles: Search radius in miles
            reso_client: RESO API client instance
            property_filters: Additional property filters
            limit: Maximum number of results

        Returns:
            Tuple of (properties list, search metadata)

        Raises:
            LocationServiceError: If search fails
        """
        try:
            self._validate_coordinates(latitude, longitude)
            self._validate_radius(radius_miles)

            # Prepare coordinate-based filters
            coordinate_filters = {
                "latitude": latitude,
                "longitude": longitude,
                "radius_miles": radius_miles
            }

            # Merge with additional property filters
            if property_filters:
                coordinate_filters.update(property_filters)

            logger.info("Searching properties near coordinates (%f, %f) within %f miles",
                       latitude, longitude, radius_miles)

            # Use existing coordinate-based search from RESO client
            properties = await reso_client.query_properties_by_coordinates(
                filters=coordinate_filters,
                limit=limit
            )

            # Calculate distances for returned properties
            enriched_properties = []
            for prop in properties:
                enriched_prop = dict(prop)

                # Add distance if property has coordinates
                prop_lat = prop.get('Latitude')
                prop_lng = prop.get('Longitude')

                if prop_lat and prop_lng:
                    distance = self._calculate_distance_miles(
                        latitude, longitude,
                        float(prop_lat), float(prop_lng)
                    )
                    enriched_prop['distance_miles'] = round(distance, 2)

                enriched_properties.append(enriched_prop)

            # Sort by distance if available
            enriched_properties.sort(key=lambda x: x.get('distance_miles', float('inf')))

            # Create search metadata
            search_metadata = {
                'search_center': {'latitude': latitude, 'longitude': longitude},
                'search_radius_miles': radius_miles,
                'total_results': len(enriched_properties),
                'search_area_sq_miles': round(math.pi * radius_miles * radius_miles, 2),
                'filters_applied': property_filters or {}
            }

            logger.info("Found %d properties near coordinates", len(enriched_properties))

            return enriched_properties, search_metadata

        except Exception as e:
            if isinstance(e, LocationServiceError):
                raise
            logger.error("Error finding properties near coordinates: %s", str(e))
            raise LocationServiceError(f"Failed to find properties near coordinates: {str(e)}")

    async def find_properties_near_location(self,
                                           location: str,
                                           radius_miles: float,
                                           reso_client,
                                           property_filters: Optional[Dict[str, Any]] = None,
                                           limit: int = 25) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Find properties near a location using integrated Google Places + RESO search.

        Args:
            location: Location string (address, business name, landmark, etc.)
            radius_miles: Search radius in miles
            reso_client: RESO API client instance
            property_filters: Additional property filters
            limit: Maximum number of results

        Returns:
            Tuple of (properties list, search metadata)

        Raises:
            LocationServiceError: If search fails
        """
        try:
            # Step 1: Resolve location to coordinates
            latitude, longitude = await self.resolve_location_to_coordinates(location)

            # Step 2: Search for properties near coordinates
            properties, metadata = await self.find_properties_near_coordinates(
                latitude=latitude,
                longitude=longitude,
                radius_miles=radius_miles,
                reso_client=reso_client,
                property_filters=property_filters,
                limit=limit
            )

            # Step 3: Enhance metadata with location information
            metadata['resolved_location'] = {
                'input_location': location,
                'resolved_coordinates': {'latitude': latitude, 'longitude': longitude},
                'location_type': self._classify_location_type(location)
            }

            return properties, metadata

        except LocationServiceError:
            raise
        except Exception as e:
            logger.error("Error finding properties near location '%s': %s", location, str(e))
            raise LocationServiceError(f"Failed to find properties near '{location}': {str(e)}")

    async def expand_search_if_needed(self,
                                     location: str,
                                     radius_miles: float,
                                     reso_client,
                                     property_filters: Optional[Dict[str, Any]] = None,
                                     limit: int = 25,
                                     min_results: int = 5,
                                     max_radius: float = 5.0) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Find properties near location with automatic radius expansion if needed.

        Args:
            location: Location string
            radius_miles: Initial search radius in miles
            reso_client: RESO API client instance
            property_filters: Additional property filters
            limit: Maximum number of results
            min_results: Minimum results before expanding radius
            max_radius: Maximum radius to expand to

        Returns:
            Tuple of (properties list, search metadata)
        """
        current_radius = radius_miles

        while current_radius <= max_radius:
            try:
                properties, metadata = await self.find_properties_near_location(
                    location=location,
                    radius_miles=current_radius,
                    reso_client=reso_client,
                    property_filters=property_filters,
                    limit=limit
                )

                # If we have enough results, return them
                if len(properties) >= min_results:
                    if current_radius > radius_miles:
                        metadata['radius_expanded'] = True
                        metadata['original_radius_miles'] = radius_miles
                        metadata['expanded_radius_miles'] = current_radius
                    return properties, metadata

                # Expand radius if we don't have enough results
                if current_radius < max_radius:
                    current_radius = min(current_radius * 1.5, max_radius)
                    logger.info("Expanding search radius to %f miles for location '%s'",
                              current_radius, location)
                else:
                    break

            except LocationServiceError:
                raise

        # Return whatever we found, even if it's less than min_results
        return properties, metadata

    def get_location_service_stats(self) -> Dict[str, Any]:
        """
        Get location service usage statistics.

        Returns:
            Statistics dictionary
        """
        stats = {
            'service_name': 'LocationService',
            'google_places_stats': self.google_places_client.get_usage_stats()
        }

        return stats

    def clear_caches(self):
        """Clear all service caches."""
        self.google_places_client.clear_cache()
        logger.info("Location service caches cleared")

    async def find_distance_to_nearest(self,
                                     address: str,
                                     place_type: str,
                                     radius_miles: float = 5.0,
                                     travel_mode: str = "driving",
                                     max_results: int = 5) -> Dict[str, Any]:
        """
        Find distance from an address to the nearest locations of a specific type.

        Args:
            address: Property address to start from
            place_type: Type of place to find (hospital, school, restaurant, etc.)
            radius_miles: Search radius in miles (default: 5.0)
            travel_mode: Travel mode for distance calculations (driving, walking, bicycling, transit)
            max_results: Maximum number of nearest locations to return (default: 5)

        Returns:
            Dictionary with nearest locations and distance information

        Raises:
            LocationServiceError: If search fails
        """
        try:
            # Step 1: Resolve address to coordinates
            logger.info("Finding distances from address '%s' to nearest '%s'", address, place_type)

            origin_lat, origin_lng = await self.resolve_location_to_coordinates(address)

            # Step 2: Find nearby places of the specified type
            radius_meters = self._miles_to_meters(radius_miles)

            # Map common place types to Google Places API types
            place_type_mapping = {
                'hospital': ['hospital'],
                'school': ['school', 'university'],
                'elementary_school': ['primary_school'],
                'high_school': ['secondary_school'],
                'restaurant': ['restaurant'],
                'grocery': ['grocery_or_supermarket'],
                'pharmacy': ['pharmacy'],
                'gas_station': ['gas_station'],
                'bank': ['bank'],
                'atm': ['atm'],
                'park': ['park'],
                'gym': ['gym'],
                'library': ['library'],
                'fire_station': ['fire_station'],
                'police': ['police'],
                'church': ['church'],
                'shopping_mall': ['shopping_mall'],
                'airport': ['airport'],
                'subway_station': ['subway_station', 'transit_station'],
                'bus_station': ['bus_station'],
                'coffee': ['cafe'],
                'starbucks': ['cafe'],
                'walmart': ['store'],
                'target': ['store'],
                'home_depot': ['store'],
                'costco': ['store']
            }

            # Get Google Places API types for the requested place type
            google_place_types = place_type_mapping.get(place_type.lower(), [place_type])

            places = await self.google_places_client.find_nearby_places(
                latitude=origin_lat,
                longitude=origin_lng,
                radius_meters=radius_meters,
                place_types=google_place_types,
                max_results=max_results * 2  # Get more to account for filtering
            )

            if not places:
                return {
                    'origin_address': address,
                    'origin_coordinates': {'latitude': origin_lat, 'longitude': origin_lng},
                    'place_type': place_type,
                    'search_radius_miles': radius_miles,
                    'nearest_locations': [],
                    'message': f"No {place_type} locations found within {radius_miles} miles of {address}"
                }

            # Step 3: Calculate distances and sort by proximity
            enriched_places = []
            for place in places[:max_results]:
                place_location = place.get('location', {})
                place_lat = place_location.get('latitude')
                place_lng = place_location.get('longitude')

                if place_lat and place_lng:
                    # Calculate straight-line distance
                    straight_distance = self._calculate_distance_miles(
                        origin_lat, origin_lng, place_lat, place_lng
                    )

                    place_info = {
                        'name': place.get('displayName', {}).get('text', 'Unknown'),
                        'address': place.get('formattedAddress', 'Address not available'),
                        'coordinates': {'latitude': place_lat, 'longitude': place_lng},
                        'straight_line_distance_miles': round(straight_distance, 2),
                        'place_id': place.get('id'),
                        'types': place.get('types', [])
                    }

                    enriched_places.append(place_info)

            # Sort by straight-line distance
            enriched_places.sort(key=lambda x: x['straight_line_distance_miles'])

            # Take only the requested number of results
            nearest_places = enriched_places[:max_results]

            # Step 4: Calculate travel distances for the nearest locations (optional)
            if nearest_places and travel_mode:
                try:
                    # For now, we'll just include straight-line distances
                    # Travel time calculation would require Distance Matrix API integration
                    for place in nearest_places:
                        place['travel_mode'] = travel_mode
                        place['travel_distance_note'] = "Travel distance calculation requires Distance Matrix API (not yet implemented)"

                except Exception as travel_error:
                    logger.warning("Could not calculate travel distances: %s", travel_error)

            result = {
                'origin_address': address,
                'origin_coordinates': {'latitude': origin_lat, 'longitude': origin_lng},
                'place_type': place_type,
                'search_radius_miles': radius_miles,
                'travel_mode': travel_mode,
                'nearest_locations': nearest_places,
                'total_found': len(nearest_places)
            }

            if nearest_places:
                closest = nearest_places[0]
                result['closest_location'] = {
                    'name': closest['name'],
                    'distance_miles': closest['straight_line_distance_miles'],
                    'address': closest['address']
                }

            logger.info("Found %d %s locations near %s", len(nearest_places), place_type, address)
            return result

        except LocationServiceError:
            raise
        except Exception as e:
            logger.error("Error finding distance to nearest %s from %s: %s", place_type, address, str(e))
            raise LocationServiceError(f"Failed to find nearest {place_type} from {address}: {str(e)}")


# Convenience functions
async def find_properties_near_location(location: str,
                                       radius_miles: float,
                                       reso_client,
                                       property_filters: Optional[Dict[str, Any]] = None,
                                       limit: int = 25) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Convenience function to find properties near a location.

    Args:
        location: Location string
        radius_miles: Search radius in miles
        reso_client: RESO API client instance
        property_filters: Additional property filters
        limit: Maximum number of results

    Returns:
        Tuple of (properties list, search metadata)
    """
    service = LocationService()
    return await service.find_properties_near_location(
        location=location,
        radius_miles=radius_miles,
        reso_client=reso_client,
        property_filters=property_filters,
        limit=limit
    )