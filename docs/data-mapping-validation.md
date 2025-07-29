# Data Mapping and Validation Documentation

## Overview

The UNLOCK MLS MCP Server includes comprehensive data mapping and validation utilities that transform raw RESO API data into user-friendly formats and validate user inputs. These utilities ensure data consistency, security, and usability across the entire system.

## Architecture

### System Design

```
Raw RESO Data → ResoDataMapper → Standardized Format → User Interface
User Input → QueryValidator → Sanitized Filters → RESO API Query
Natural Language → NLP Parser → Structured Filters → API Request
```

### Core Components

1. **ResoDataMapper**: Transforms RESO fields to user-friendly formats
2. **QueryValidator**: Validates and sanitizes user inputs
3. **Natural Language Processor**: Parses conversational queries
4. **Field Mappers**: Specialized mapping for different data types
5. **Input Sanitizers**: Security and validation filters

## ResoDataMapper

### Purpose

The `ResoDataMapper` class standardizes RESO API responses into consistent, user-friendly formats that are easier to understand and work with.

### Implementation

```python
class ResoDataMapper:
    """Maps and formats RESO data into standardized, user-friendly formats."""
    
    # Property status mappings
    STATUS_MAPPING = {
        "Active": "active",
        "Active Under Contract": "under_contract", 
        "Pending": "pending",
        "Sold": "sold",
        "Closed": "sold",
        "Expired": "expired",
        "Withdrawn": "withdrawn",
        "Cancelled": "cancelled",
        "Hold": "hold"
    }
    
    # Property type mappings
    PROPERTY_TYPE_MAPPING = {
        "Residential": "residential",
        "Condominium": "condo",
        "Townhouse": "townhouse", 
        "Single Family Residence": "single_family",
        "Multi-Family": "multi_family",
        "Manufactured": "manufactured",
        "Land": "land",
        "Commercial": "commercial",
        "Business Opportunity": "business"
    }
```

### Field Mapping

#### Basic Property Fields

```python
def map_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
    """Map a single property record to standardized format."""
    
    mapped = {
        # Basic identifiers
        "listing_id": property_data.get("ListingId"),
        "listing_key": property_data.get("ListingKey"),
        "mls_number": property_data.get("ListingId"),
        
        # Status and pricing
        "status": self._map_status(property_data.get("StandardStatus")),
        "list_price": self._format_price(property_data.get("ListPrice")),
        "original_list_price": self._format_price(property_data.get("OriginalListPrice")),
        "sold_price": self._format_price(property_data.get("ClosePrice")),
        
        # Property details
        "bedrooms": self._safe_int(property_data.get("BedroomsTotal")),
        "bathrooms": self._safe_float(property_data.get("BathroomsTotalInteger")),
        "square_feet": self._safe_int(property_data.get("LivingArea")),
        "lot_size": self._safe_float(property_data.get("LotSizeAcres")),
        "year_built": self._safe_int(property_data.get("YearBuilt")),
        
        # Property type
        "property_type": self._map_property_type(
            property_data.get("PropertyType"), 
            property_data.get("PropertySubType")
        ),
        
        # Location
        "address": self._format_address(property_data),
        "city": property_data.get("City"),
        "state": property_data.get("StateOrProvince"),
        "zip_code": property_data.get("PostalCode"),
        "county": property_data.get("CountyOrParish"),
        
        # Dates
        "list_date": self._format_date(property_data.get("OnMarketDate")),
        "sold_date": self._format_date(property_data.get("CloseDate")),
        "modification_date": self._format_date(property_data.get("ModificationTimestamp")),
        
        # Additional details
        "remarks": self._clean_text(property_data.get("PublicRemarks")),
        "listing_agent_name": property_data.get("ListAgentFullName"),
        "listing_office": property_data.get("ListOfficeName")
    }
    
    return {k: v for k, v in mapped.items() if v is not None}
```

#### Type-Safe Data Conversion

```python
def _safe_int(self, value: Any) -> Optional[int]:
    """Safely convert value to integer."""
    if value is None:
        return None
    
    try:
        if isinstance(value, str):
            value = value.replace(',', '').strip()
            if not value:
                return None
        return int(float(value))
    except (ValueError, TypeError):
        logger.warning("Failed to convert to int: %s", value)
        return None

def _safe_float(self, value: Any) -> Optional[float]:
    """Safely convert value to float."""
    if value is None:
        return None
    
    try:
        if isinstance(value, str):
            value = value.replace(',', '').strip()
            if not value:
                return None
        return float(value)
    except (ValueError, TypeError):
        logger.warning("Failed to convert to float: %s", value)
        return None

def _format_price(self, price: Any) -> Optional[int]:
    """Format price as integer."""
    if price is None:
        return None
    
    try:
        if isinstance(price, str):
            # Remove currency symbols and commas
            price = re.sub(r'[$,]', '', price).strip()
            if not price:
                return None
        
        price_float = float(price)
        return int(price_float) if price_float > 0 else None
    except (ValueError, TypeError):
        logger.warning("Failed to format price: %s", price)
        return None
```

### Address Formatting

```python
def _format_address(self, property_data: Dict[str, Any]) -> Optional[str]:
    """Format property address components into single string."""
    
    address_parts = []
    
    # Street number and name
    street_number = property_data.get("StreetNumber")
    street_name = property_data.get("StreetName")
    
    if street_number and street_name:
        address_parts.append(f"{street_number} {street_name}")
    elif street_name:
        address_parts.append(street_name)
    
    # Unit number
    unit_number = property_data.get("UnitNumber")
    if unit_number:
        address_parts.append(f"Unit {unit_number}")
    
    # City, State, ZIP
    city = property_data.get("City")
    state = property_data.get("StateOrProvince")
    zip_code = property_data.get("PostalCode")
    
    if city and state:
        if zip_code:
            address_parts.append(f"{city}, {state} {zip_code}")
        else:
            address_parts.append(f"{city}, {state}")
    
    return ", ".join(address_parts) if address_parts else None
```

### Date Formatting

```python
def _format_date(self, date_value: Any) -> Optional[str]:
    """Format date value to consistent string format."""
    if not date_value:
        return None
    
    try:
        if isinstance(date_value, str):
            # Parse various date formats
            from datetime import datetime
            
            # Try common RESO date formats
            date_formats = [
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ", 
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%m/%d/%Y",
                "%m-%d-%Y"
            ]
            
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_value, fmt)
                    return parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    continue
            
            logger.warning("Unable to parse date format: %s", date_value)
            return date_value
        
        # Handle datetime objects
        elif hasattr(date_value, 'strftime'):
            return date_value.strftime("%Y-%m-%d")
        
        return str(date_value)
        
    except Exception as e:
        logger.warning("Date formatting error: %s", e)
        return None
```

### Text Cleaning

```python
def _clean_text(self, text: Any) -> Optional[str]:
    """Clean and format text content."""
    if not text:
        return None
    
    text = str(text).strip()
    
    if not text:
        return None
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove HTML tags if present
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,!?()"]', '', text)
    
    return text if text else None
```

### Property Summary Generation

```python
def get_property_summary(self, property_data: Dict[str, Any]) -> str:
    """Generate a concise property summary string."""
    
    parts = []
    
    # Price
    if property_data.get("list_price"):
        parts.append(f"${property_data['list_price']:,}")
    
    # Bedrooms and bathrooms
    bedrooms = property_data.get("bedrooms")
    bathrooms = property_data.get("bathrooms")
    
    if bedrooms and bathrooms:
        parts.append(f"{bedrooms} BR, {bathrooms} BA")
    elif bedrooms:
        parts.append(f"{bedrooms} BR")
    
    # Square footage
    sqft = property_data.get("square_feet")
    if sqft:
        parts.append(f"{sqft:,} sq ft")
    
    # Property type
    prop_type = property_data.get("property_type")
    if prop_type:
        type_display = prop_type.replace('_', ' ').title()
        parts.append(type_display)
    
    return " | ".join(parts) if parts else "Property details available"
```

## QueryValidator

### Purpose

The `QueryValidator` class validates user inputs, sanitizes data for security, and parses natural language queries into structured filters.

### Implementation

```python
class QueryValidator:
    """Validates and parses user inputs for property searches."""
    
    # Valid property statuses - RESO API values
    VALID_STATUSES = [
        "Active", "Under Contract", "Pending", "Sold", "Closed", 
        "Expired", "Withdrawn", "Cancelled", "Hold"
    ]
    
    # Valid property types - RESO API values
    VALID_PROPERTY_TYPES = [
        "Residential", "Residential Lease", "Land", "Farm", "Commercial", "Business"
    ]
    
    # US State abbreviations for validation
    US_STATES = {
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    }
```

### Input Validation

```python
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
    
    # Validate location fields
    if "city" in filters:
        validated["city"] = self._validate_city(filters["city"])
    
    if "state" in filters:
        validated["state"] = self._validate_state(filters["state"])
    
    if "zip_code" in filters:
        validated["zip_code"] = self._validate_zip_code(filters["zip_code"])
    
    # Validate price fields
    for field in ["min_price", "max_price"]:
        if field in filters:
            validated[field] = self._validate_price(filters[field], field)
    
    # Validate bedroom/bathroom counts
    for field in ["min_bedrooms", "max_bedrooms"]:
        if field in filters:
            validated[field] = self._validate_room_count(filters[field], field)
    
    for field in ["min_bathrooms", "max_bathrooms"]:
        if field in filters:
            validated[field] = self._validate_bathroom_count(filters[field], field)
    
    # Validate square footage
    for field in ["min_sqft", "max_sqft"]:
        if field in filters:
            validated[field] = self._validate_sqft(filters[field], field)
    
    # Validate property type and status
    if "property_type" in filters:
        validated["property_type"] = self._validate_property_type(filters["property_type"])
    
    if "status" in filters:
        validated["status"] = self._validate_status(filters["status"])
    
    # Validate listing ID
    if "listing_id" in filters:
        validated["listing_id"] = self._validate_listing_id(filters["listing_id"])
    
    # Check for valid price ranges
    self._validate_price_range(validated)
    
    return validated

def _validate_city(self, city: Any) -> str:
    """Validate city name."""
    if not city:
        raise ValidationError("City cannot be empty")
    
    city = str(city).strip().title()
    
    if len(city) < 2:
        raise ValidationError("City name too short")
    
    if len(city) > 50:
        raise ValidationError("City name too long")
    
    # Basic sanitization - allow letters, spaces, hyphens, apostrophes
    if not re.match(r"^[A-Za-z\s\-'\.]+$", city):
        raise ValidationError("Invalid characters in city name")
    
    return city

def _validate_state(self, state: Any) -> str:
    """Validate state abbreviation."""
    if not state:
        raise ValidationError("State cannot be empty")
    
    state = str(state).strip().upper()
    
    if state not in self.US_STATES:
        raise ValidationError(f"Invalid state abbreviation: {state}")
    
    return state

def _validate_price(self, price: Any, field_name: str) -> int:
    """Validate price value."""
    try:
        if isinstance(price, str):
            # Remove common formatting
            price = re.sub(r'[$,\s]', '', price)
        
        price_value = int(float(price))
        
        if price_value < 0:
            raise ValidationError(f"{field_name} cannot be negative")
        
        if price_value > 100_000_000:  # $100M limit
            raise ValidationError(f"{field_name} exceeds maximum value")
        
        return price_value
        
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid {field_name}: must be a number")
```

### Natural Language Processing

```python
def parse_natural_language_query(self, query: str) -> Dict[str, Any]:
    """
    Parse natural language query into structured filters.
    
    Args:
        query: Natural language search query
        
    Returns:
        Dictionary of parsed filters
    """
    if not query or not isinstance(query, str):
        return {}
    
    query = query.lower().strip()
    logger.debug("Parsing natural language query: %s", query)
    
    parsed_filters = {}
    
    # Extract price information
    price_filters = self._extract_price_patterns(query)
    parsed_filters.update(price_filters)
    
    # Extract bedroom/bathroom information
    room_filters = self._extract_room_patterns(query)
    parsed_filters.update(room_filters)
    
    # Extract square footage information
    sqft_filters = self._extract_sqft_patterns(query)
    parsed_filters.update(sqft_filters)
    
    # Extract property type
    property_type = self._extract_property_type(query)
    if property_type:
        parsed_filters["property_type"] = property_type
    
    # Extract location information
    location_filters = self._extract_location_patterns(query)
    parsed_filters.update(location_filters)
    
    # Extract amenities and features
    features = self._extract_features(query)
    if features:
        parsed_filters["features"] = features
    
    logger.debug("Parsed filters: %s", parsed_filters)
    return parsed_filters

def _extract_price_patterns(self, query: str) -> Dict[str, int]:
    """Extract price information from query."""
    price_filters = {}
    
    for pattern, filter_type in self.PRICE_PATTERNS:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            if filter_type == 'price_range':
                # Handle price range (e.g., "$300k-$500k")
                min_price = self._parse_price_value(match.group(1))
                max_price = self._parse_price_value(match.group(2))
                if min_price and max_price:
                    price_filters["min_price"] = min_price
                    price_filters["max_price"] = max_price
            else:
                # Handle single price bound
                price_value = self._parse_price_value(match.group(1))
                if price_value:
                    price_filters[filter_type] = price_value
            break  # Use first match
    
    return price_filters

def _parse_price_value(self, price_str: str) -> Optional[int]:
    """Parse price string into integer value."""
    try:
        # Remove common formatting
        price_str = re.sub(r'[$,\s]', '', price_str.lower())
        
        # Handle 'k' suffix for thousands
        if price_str.endswith('k'):
            price_str = price_str[:-1]
            multiplier = 1000
        else:
            multiplier = 1
        
        price_value = int(float(price_str) * multiplier)
        return price_value if price_value > 0 else None
        
    except (ValueError, TypeError):
        logger.warning("Failed to parse price: %s", price_str)
        return None

def _extract_location_patterns(self, query: str) -> Dict[str, str]:
    """Extract location information from query."""
    location_filters = {}
    
    # Pattern for "in [City], [State]" or "in [City] [State]"
    city_state_pattern = r'\bin\s+([A-Za-z\s\-\'\.]+?)(?:,\s*)?([A-Z]{2})\b'
    match = re.search(city_state_pattern, query, re.IGNORECASE)
    
    if match:
        city = match.group(1).strip().title()
        state = match.group(2).upper()
        
        if state in self.US_STATES:
            location_filters["city"] = city
            location_filters["state"] = state
    else:
        # Try to find just city pattern
        city_pattern = r'\bin\s+([A-Za-z\s\-\'\.]+)\b'
        match = re.search(city_pattern, query, re.IGNORECASE)
        if match:
            location_filters["city"] = match.group(1).strip().title()
    
    # Look for ZIP code pattern
    zip_pattern = r'\b(\d{5}(?:-\d{4})?)\b'
    match = re.search(zip_pattern, query)
    if match:
        location_filters["zip_code"] = match.group(1)
    
    return location_filters

def _extract_features(self, query: str) -> List[str]:
    """Extract property features and amenities."""
    features = []
    
    feature_patterns = {
        r'\bpool\b': 'pool',
        r'\bfireplace\b': 'fireplace', 
        r'\bgarage\b': 'garage',
        r'\bwaterfront\b': 'waterfront',
        r'\bbasement\b': 'basement',
        r'\bdeck\b': 'deck',
        r'\bpatio\b': 'patio',
        r'\bbalcony\b': 'balcony'
    }
    
    for pattern, feature in feature_patterns.items():
        if re.search(pattern, query, re.IGNORECASE):
            features.append(feature)
    
    return features
```

### Security and Sanitization

```python
def _sanitize_string_input(self, value: Any, field_name: str, max_length: int = 100) -> str:
    """Sanitize string input for security."""
    if not value:
        raise ValidationError(f"{field_name} cannot be empty")
    
    value = str(value).strip()
    
    if len(value) > max_length:
        raise ValidationError(f"{field_name} exceeds maximum length of {max_length}")
    
    # Check for potential injection patterns
    dangerous_patterns = [
        r'[<>"\']',  # HTML/XML tags and quotes
        r'[;&|`$()]',  # Shell metacharacters
        r'(union|select|insert|update|delete|drop|create|alter)',  # SQL keywords
        r'(script|javascript|vbscript)',  # Script injection
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError(f"Invalid characters detected in {field_name}")
    
    return value

def _validate_listing_id(self, listing_id: Any) -> str:
    """Validate listing ID format."""
    if not listing_id:
        raise ValidationError("Listing ID cannot be empty")
    
    listing_id = str(listing_id).strip()
    
    # Typical MLS listing ID patterns
    if not re.match(r'^[A-Za-z0-9\-_]{3,50}$', listing_id):
        raise ValidationError("Invalid listing ID format")
    
    return listing_id

def _validate_price_range(self, filters: Dict[str, Any]):
    """Validate that price ranges are logical."""
    min_price = filters.get("min_price")
    max_price = filters.get("max_price")
    
    if min_price and max_price:
        if min_price >= max_price:
            raise ValidationError("Minimum price must be less than maximum price")
        
        if max_price - min_price < 10000:
            raise ValidationError("Price range too narrow (minimum $10,000 difference)")
```

## Testing and Validation

### Unit Testing

```python
import pytest
from unittest.mock import patch

class TestResoDataMapper:
    
    def test_property_mapping(self):
        """Test basic property data mapping."""
        raw_data = {
            "ListingId": "TEST123",
            "ListPrice": 450000,
            "BedroomsTotal": 3,
            "BathroomsTotalInteger": 2,
            "LivingArea": 1850,
            "City": "Austin",
            "StateOrProvince": "TX",
            "StandardStatus": "Active"
        }
        
        mapper = ResoDataMapper()
        mapped = mapper.map_property(raw_data)
        
        assert mapped["listing_id"] == "TEST123"
        assert mapped["list_price"] == 450000
        assert mapped["bedrooms"] == 3
        assert mapped["bathrooms"] == 2
        assert mapped["square_feet"] == 1850
        assert mapped["city"] == "Austin"
        assert mapped["state"] == "TX"
        assert mapped["status"] == "active"
    
    def test_price_formatting(self):
        """Test price formatting edge cases."""
        mapper = ResoDataMapper()
        
        # Test various price formats
        assert mapper._format_price("$450,000") == 450000
        assert mapper._format_price("450000.00") == 450000
        assert mapper._format_price("") is None
        assert mapper._format_price(None) is None
        assert mapper._format_price("invalid") is None

class TestQueryValidator:
    
    def test_natural_language_parsing(self):
        """Test natural language query parsing."""
        validator = QueryValidator()
        
        # Test basic query
        query = "3 bedroom house under $500k in Austin TX"
        parsed = validator.parse_natural_language_query(query)
        
        assert parsed["min_bedrooms"] == 3
        assert parsed["max_price"] == 500000
        assert parsed["city"] == "Austin"
        assert parsed["state"] == "TX"
    
    def test_input_validation(self):
        """Test input validation and sanitization."""
        validator = QueryValidator()
        
        # Test valid filters
        filters = {
            "city": "Austin",
            "state": "TX",
            "min_price": 300000,
            "max_price": 500000,
            "min_bedrooms": 3
        }
        
        validated = validator.validate_search_filters(filters)
        assert validated["city"] == "Austin"
        assert validated["state"] == "TX"
        assert validated["min_price"] == 300000
        
        # Test invalid state
        with pytest.raises(ValidationError):
            validator.validate_search_filters({"state": "XX"})
        
        # Test invalid price range
        with pytest.raises(ValidationError):
            validator.validate_search_filters({
                "min_price": 500000,
                "max_price": 300000
            })
    
    def test_security_sanitization(self):
        """Test security input sanitization."""
        validator = QueryValidator()
        
        # Test injection attempts
        with pytest.raises(ValidationError):
            validator._sanitize_string_input("Austin'; DROP TABLE--", "city")
        
        with pytest.raises(ValidationError):
            validator._sanitize_string_input("<script>alert('xss')</script>", "city")
        
        # Test valid input
        result = validator._sanitize_string_input("Austin", "city")
        assert result == "Austin"
```

### Integration Testing

```python
@pytest.mark.integration
class TestDataMappingIntegration:
    
    def test_full_mapping_pipeline(self):
        """Test complete data mapping pipeline."""
        # Simulate real RESO API response
        raw_property = {
            "ListingId": "ACTRIS12345",
            "ListPrice": 575000,
            "BedroomsTotal": 4,
            "BathroomsTotalInteger": 3,
            "LivingArea": 2400,
            "LotSizeAcres": 0.25,
            "YearBuilt": 2018,
            "PropertyType": "Residential",
            "PropertySubType": "Single Family Residence",
            "StandardStatus": "Active",
            "City": "Cedar Park",
            "StateOrProvince": "TX",
            "PostalCode": "78613",
            "StreetNumber": "1234",
            "StreetName": "Oak Hill Drive",
            "PublicRemarks": "Beautiful home with upgrades throughout!",
            "ListAgentFullName": "John Smith",
            "ListOfficeName": "Austin Realty Group"
        }
        
        mapper = ResoDataMapper()
        mapped = mapper.map_property(raw_property)
        
        # Verify complete mapping
        assert mapped["listing_id"] == "ACTRIS12345"
        assert mapped["list_price"] == 575000
        assert mapped["bedrooms"] == 4
        assert mapped["bathrooms"] == 3
        assert mapped["square_feet"] == 2400
        assert mapped["property_type"] == "single_family"
        assert mapped["status"] == "active"
        assert "Cedar Park, TX 78613" in mapped["address"]
        assert mapped["remarks"] == "Beautiful home with upgrades throughout!"
        
        # Test summary generation
        summary = mapper.get_property_summary(mapped)
        assert "$575,000" in summary
        assert "4 BR, 3 BA" in summary
        assert "2,400 sq ft" in summary
```

## Performance Optimization

### Caching Strategies

```python
from functools import lru_cache
from typing import Dict, Any

class CachedDataMapper(ResoDataMapper):
    """Data mapper with caching for improved performance."""
    
    @lru_cache(maxsize=1000)
    def _cached_property_type_mapping(self, property_type: str, property_subtype: str) -> str:
        """Cache property type mappings."""
        return self._map_property_type(property_type, property_subtype)
    
    @lru_cache(maxsize=500)
    def _cached_status_mapping(self, status: str) -> str:
        """Cache status mappings."""
        return self._map_status(status)

class BatchDataMapper:
    """Optimized mapper for batch operations."""
    
    def map_properties_batch(self, properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map multiple properties efficiently."""
        mapper = ResoDataMapper()
        
        # Pre-compile common patterns
        results = []
        
        for property_data in properties:
            try:
                mapped = mapper.map_property(property_data)
                results.append(mapped)
            except Exception as e:
                logger.warning("Failed to map property %s: %s", 
                             property_data.get("ListingId", "unknown"), e)
                # Continue with partial data
                results.append({"listing_id": property_data.get("ListingId"), "error": str(e)})
        
        return results
```

This comprehensive data mapping and validation system ensures data quality, security, and usability while providing flexible natural language processing capabilities for user-friendly interaction with real estate data.