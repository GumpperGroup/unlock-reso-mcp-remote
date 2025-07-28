"""Input validation and natural language query parsing for RESO searches."""

import re
from typing import Dict, List, Optional, Any, Union, Tuple
from decimal import Decimal, InvalidOperation
import logging

from ..config.logging_config import setup_logging

logger = setup_logging(__name__)


class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


class QueryValidator:
    """Validates and parses user inputs for property searches."""
    
    # Valid property statuses
    VALID_STATUSES = [
        "active", "under_contract", "pending", "sold", "closed", 
        "expired", "withdrawn", "cancelled", "hold"
    ]
    
    # Valid property types
    VALID_PROPERTY_TYPES = [
        "residential", "condo", "townhouse", "single_family", "multi_family",
        "manufactured", "land", "commercial", "business"
    ]
    
    # State abbreviations for validation
    US_STATES = {
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    }
    
    # Price range patterns for natural language parsing
    PRICE_PATTERNS = [
        (r'under\s+\$?(\d{1,3}(?:,?\d{3})*k?)', 'max_price'),
        (r'below\s+\$?(\d{1,3}(?:,?\d{3})*k?)', 'max_price'),
        (r'less\s+than\s+\$?(\d{1,3}(?:,?\d{3})*k?)', 'max_price'),
        (r'over\s+\$?(\d{1,3}(?:,?\d{3})*k?)', 'min_price'),
        (r'above\s+\$?(\d{1,3}(?:,?\d{3})*k?)', 'min_price'),
        (r'more\s+than\s+\$?(\d{1,3}(?:,?\d{3})*k?)', 'min_price'),
        (r'\$?(\d{1,3}(?:,?\d{3})*k?)\s*-\s*\$?(\d{1,3}(?:,?\d{3})*k?)', 'price_range'),
        (r'between\s+\$?(\d{1,3}(?:,?\d{3})*k?)\s+and\s+\$?(\d{1,3}(?:,?\d{3})*k?)', 'price_range'),
    ]
    
    # Bedroom/bathroom patterns
    BEDROOM_PATTERNS = [
        (r'(\d+)\s*(?:br|bed|bedroom)s?', 'bedrooms'),
        (r'(\d+)\s*bed', 'bedrooms'),
    ]
    
    BATHROOM_PATTERNS = [
        (r'(\d+(?:\.\d+)?)\s*(?:ba|bath|bathroom)s?', 'bathrooms'),
        (r'(\d+(?:\.\d+)?)\s*bath', 'bathrooms'),
    ]
    
    # Square footage patterns
    SQFT_PATTERNS = [
        (r'over\s+(\d{1,3}(?:,?\d{3})*)\s*(?:sq\s*ft|sqft|square\s*feet)', 'min_sqft'),
        (r'under\s+(\d{1,3}(?:,?\d{3})*)\s*(?:sq\s*ft|sqft|square\s*feet)', 'max_sqft'),
        (r'(\d{1,3}(?:,?\d{3})*)\s*(?:sq\s*ft|sqft|square\s*feet)', 'sqft'),
        (r'(\d{1,3}(?:,?\d{3})*)\s*sf', 'sqft'),
    ]
    
    # Property type patterns
    PROPERTY_TYPE_PATTERNS = [
        (r'\b(?:single\s*family|sfr|house|home)\b', 'single_family'),
        (r'\bcondo(?:minium)?\b', 'condo'),
        (r'\btownhouse\b', 'townhouse'),
        (r'\bmulti\s*family\b', 'multi_family'),
        (r'\bmanufactured\b', 'manufactured'),
        (r'\bcommercial\b', 'commercial'),
        (r'\bland\b', 'land'),
    ]
    
    def __init__(self):
        """Initialize the query validator."""
        logger.info("QueryValidator initialized")
    
    def validate_search_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize search filters.
        
        Args:
            filters: Raw search filters
            
        Returns:
            Validated and sanitized filters
            
        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(filters, dict):
            raise ValidationError("Filters must be a dictionary")
        
        validated = {}
        
        # Validate location filters
        if "city" in filters:
            validated["city"] = self._validate_city(filters["city"])
        
        if "state" in filters:
            validated["state"] = self._validate_state(filters["state"])
        
        if "zip_code" in filters:
            validated["zip_code"] = self._validate_zip_code(filters["zip_code"])
        
        # Validate price filters
        if "min_price" in filters:
            validated["min_price"] = self._validate_price(filters["min_price"])
        
        if "max_price" in filters:
            validated["max_price"] = self._validate_price(filters["max_price"])
        
        # Validate price range consistency
        if "min_price" in validated and "max_price" in validated:
            if validated["min_price"] >= validated["max_price"]:
                raise ValidationError("Minimum price must be less than maximum price")
        
        # Validate bedroom/bathroom counts
        if "min_bedrooms" in filters:
            validated["min_bedrooms"] = self._validate_room_count(filters["min_bedrooms"], "bedrooms")
        
        if "max_bedrooms" in filters:
            validated["max_bedrooms"] = self._validate_room_count(filters["max_bedrooms"], "bedrooms")
        
        if "min_bathrooms" in filters:
            validated["min_bathrooms"] = self._validate_bathroom_count(filters["min_bathrooms"])
        
        if "max_bathrooms" in filters:
            validated["max_bathrooms"] = self._validate_bathroom_count(filters["max_bathrooms"])
        
        # Validate square footage
        if "min_sqft" in filters:
            validated["min_sqft"] = self._validate_sqft(filters["min_sqft"])
        
        if "max_sqft" in filters:
            validated["max_sqft"] = self._validate_sqft(filters["max_sqft"])
        
        # Validate sqft range consistency
        if "min_sqft" in validated and "max_sqft" in validated:
            if validated["min_sqft"] >= validated["max_sqft"]:
                raise ValidationError("Minimum square footage must be less than maximum")
        
        # Validate property type and status
        if "property_type" in filters:
            validated["property_type"] = self._validate_property_type(filters["property_type"])
        
        if "status" in filters:
            validated["status"] = self._validate_status(filters["status"])
        
        # Validate listing ID
        if "listing_id" in filters:
            validated["listing_id"] = self._validate_listing_id(filters["listing_id"])
        
        logger.debug("Filters validated: %s", validated)
        return validated
    
    def parse_natural_language_query(self, query: str) -> Dict[str, Any]:
        """
        Parse natural language property search query.
        
        Args:
            query: Natural language search query
            
        Returns:
            Parsed search filters
        """
        if not isinstance(query, str):
            raise ValidationError("Query must be a string")
        
        query = query.lower().strip()
        filters = {}
        
        logger.debug("Parsing natural language query: %s", query)
        
        # Extract price information
        price_filters = self._extract_price_info(query)
        filters.update(price_filters)
        
        # Extract bedroom information
        bedroom_filters = self._extract_bedroom_info(query)
        filters.update(bedroom_filters)
        
        # Extract bathroom information
        bathroom_filters = self._extract_bathroom_info(query)
        filters.update(bathroom_filters)
        
        # Extract square footage information
        sqft_filters = self._extract_sqft_info(query)
        filters.update(sqft_filters)
        
        # Extract property type
        property_type = self._extract_property_type(query)
        if property_type:
            filters["property_type"] = property_type
        
        # Extract location (basic city detection)
        location_filters = self._extract_location_info(query)
        filters.update(location_filters)
        
        logger.debug("Parsed filters: %s", filters)
        return filters
    
    def _validate_city(self, city: Any) -> str:
        """Validate city name."""
        if not isinstance(city, str):
            raise ValidationError("City must be a string")
        
        city = city.strip()
        if len(city) < 2:
            raise ValidationError("City name must be at least 2 characters")
        
        if len(city) > 100:
            raise ValidationError("City name too long")
        
        # Basic sanitization - allow letters, spaces, hyphens, apostrophes
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", city):
            raise ValidationError("City name contains invalid characters")
        
        return city.title()
    
    def _validate_state(self, state: Any) -> str:
        """Validate state abbreviation."""
        if not isinstance(state, str):
            raise ValidationError("State must be a string")
        
        state = state.upper().strip()
        if state not in self.US_STATES:
            raise ValidationError(f"Invalid state abbreviation: {state}")
        
        return state
    
    def _validate_zip_code(self, zip_code: Any) -> str:
        """Validate ZIP code."""
        if isinstance(zip_code, int):
            zip_code = str(zip_code)
        
        if not isinstance(zip_code, str):
            raise ValidationError("ZIP code must be a string or number")
        
        zip_code = zip_code.strip()
        
        # Support 5-digit and 9-digit ZIP codes
        if not re.match(r'^\d{5}(?:-?\d{4})?$', zip_code):
            raise ValidationError("Invalid ZIP code format")
        
        return zip_code
    
    def _validate_price(self, price: Any) -> int:
        """Validate price value."""
        try:
            if isinstance(price, str):
                # Remove currency symbols and commas
                price = re.sub(r'[^\d.]', '', price)
            
            price_val = int(float(price))
            
            if price_val < 0:
                raise ValidationError("Price cannot be negative")
            
            if price_val > 100000000:  # $100M limit
                raise ValidationError("Price too high")
            
            return price_val
            
        except (ValueError, TypeError):
            raise ValidationError("Invalid price format")
    
    def _validate_room_count(self, count: Any, room_type: str) -> int:
        """Validate room count (bedrooms)."""
        try:
            count = int(count)
            
            if count < 0:
                raise ValidationError(f"{room_type.title()} count cannot be negative")
            
            if count > 20:
                raise ValidationError(f"{room_type.title()} count too high")
            
            return count
            
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid {room_type} count")
    
    def _validate_bathroom_count(self, count: Any) -> float:
        """Validate bathroom count (allows half baths)."""
        try:
            count = float(count)
            
            if count < 0:
                raise ValidationError("Bathroom count cannot be negative")
            
            if count > 20:
                raise ValidationError("Bathroom count too high")
            
            # Round to nearest 0.5
            return round(count * 2) / 2
            
        except (ValueError, TypeError):
            raise ValidationError("Invalid bathroom count")
    
    def _validate_sqft(self, sqft: Any) -> int:
        """Validate square footage."""
        try:
            if isinstance(sqft, str):
                sqft = re.sub(r'[^\d.]', '', sqft)
            
            sqft_val = int(float(sqft))
            
            if sqft_val < 0:
                raise ValidationError("Square footage cannot be negative")
            
            if sqft_val > 50000:  # 50,000 sqft limit
                raise ValidationError("Square footage too high")
            
            return sqft_val
            
        except (ValueError, TypeError):
            raise ValidationError("Invalid square footage")
    
    def _validate_property_type(self, prop_type: Any) -> str:
        """Validate property type."""
        if not isinstance(prop_type, str):
            raise ValidationError("Property type must be a string")
        
        prop_type = prop_type.lower().strip()
        
        if prop_type not in self.VALID_PROPERTY_TYPES:
            raise ValidationError(f"Invalid property type: {prop_type}")
        
        return prop_type
    
    def _validate_status(self, status: Any) -> str:
        """Validate property status."""
        if not isinstance(status, str):
            raise ValidationError("Status must be a string")
        
        status = status.lower().strip()
        
        if status not in self.VALID_STATUSES:
            raise ValidationError(f"Invalid status: {status}")
        
        return status
    
    def _validate_listing_id(self, listing_id: Any) -> str:
        """Validate listing ID."""
        if isinstance(listing_id, int):
            listing_id = str(listing_id)
        
        if not isinstance(listing_id, str):
            raise ValidationError("Listing ID must be a string or number")
        
        listing_id = listing_id.strip()
        
        if not listing_id:
            raise ValidationError("Listing ID cannot be empty")
        
        if len(listing_id) > 50:
            raise ValidationError("Listing ID too long")
        
        return listing_id
    
    def _extract_price_info(self, query: str) -> Dict[str, int]:
        """Extract price information from natural language query."""
        filters = {}
        
        for pattern, filter_type in self.PRICE_PATTERNS:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                if filter_type == 'price_range':
                    # Handle price range (two values)
                    min_price = self._parse_price_value(match.group(1))
                    max_price = self._parse_price_value(match.group(2))
                    if min_price and max_price:
                        filters['min_price'] = min(min_price, max_price)
                        filters['max_price'] = max(min_price, max_price)
                else:
                    # Handle single price value
                    price = self._parse_price_value(match.group(1))
                    if price:
                        filters[filter_type] = price
                break
        
        return filters
    
    def _extract_bedroom_info(self, query: str) -> Dict[str, int]:
        """Extract bedroom information from query."""
        filters = {}
        
        for pattern, filter_type in self.BEDROOM_PATTERNS:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                bedrooms = int(match.group(1))
                filters['min_bedrooms'] = bedrooms
                break
        
        return filters
    
    def _extract_bathroom_info(self, query: str) -> Dict[str, float]:
        """Extract bathroom information from query."""
        filters = {}
        
        for pattern, filter_type in self.BATHROOM_PATTERNS:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                bathrooms = float(match.group(1))
                filters['min_bathrooms'] = bathrooms
                break
        
        return filters
    
    def _extract_sqft_info(self, query: str) -> Dict[str, int]:
        """Extract square footage information from query."""
        filters = {}
        
        for pattern, filter_type in self.SQFT_PATTERNS:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                sqft = int(match.group(1).replace(',', ''))
                filters[filter_type] = sqft
                break
        
        return filters
    
    def _extract_property_type(self, query: str) -> Optional[str]:
        """Extract property type from query."""
        for pattern, prop_type in self.PROPERTY_TYPE_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return prop_type
        
        return None
    
    def _extract_location_info(self, query: str) -> Dict[str, str]:
        """Extract basic location information from query."""
        filters = {}
        
        # Look for state abbreviations first (more specific)
        state_matches = re.findall(r'\b([A-Z]{2})\b', query.upper())
        for state in state_matches:
            if state in self.US_STATES and state != 'IN':  # Exclude 'IN' as it's a common word
                filters['state'] = state
                break
        
        # Look for "in [city]" patterns with various formats
        city_patterns = [
            # "in San Antonio TX" - city followed by state
            rf'\bin\s+([a-zA-Z\s\-\'\.]+?)\s+([A-Z]{{2}})\b',
            # "in Houston, TX" - city with comma before state  
            rf'\bin\s+([a-zA-Z\s\-\'\.]+?),\s*([A-Z]{{2}})\b',
            # "in Austin" - city only
            rf'\bin\s+([a-zA-Z\s\-\'\.]+?)(?:\s|$|,)'
        ]
        
        for pattern in city_patterns:
            city_match = re.search(pattern, query, re.IGNORECASE)
            if city_match:
                if len(city_match.groups()) == 2:
                    # Pattern with state
                    city_candidate = city_match.group(1).strip()
                    state_candidate = city_match.group(2).upper()
                    if state_candidate in self.US_STATES:
                        filters['state'] = state_candidate
                else:
                    # Pattern without state
                    city_candidate = city_match.group(1).strip()
                
                # Clean up the city name
                city_words = city_candidate.split()
                clean_words = []
                for word in city_words:
                    if len(word) > 1 and word.upper() not in self.US_STATES:
                        clean_words.append(word)
                    if len(clean_words) >= 3:  # Limit city name length
                        break
                
                if clean_words:
                    city_candidate = ' '.join(clean_words)
                    try:
                        if len(city_candidate) >= 2:
                            filters['city'] = self._validate_city(city_candidate)
                            break  # Stop after first successful match
                    except ValidationError:
                        continue  # Try next pattern
        
        return filters
    
    def _parse_price_value(self, price_str: str) -> Optional[int]:
        """Parse price value from string (handles 'k' suffix)."""
        try:
            price_str = price_str.replace(',', '').lower()
            
            if price_str.endswith('k'):
                return int(float(price_str[:-1]) * 1000)
            else:
                return int(float(price_str))
        except (ValueError, TypeError):
            return None