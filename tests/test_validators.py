"""Tests for input validation and natural language query parsing."""

import pytest

from src.utils.validators import QueryValidator, ValidationError


class TestQueryValidator:
    """Test cases for QueryValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Create validator instance."""
        return QueryValidator()
    
    def test_initialization(self, validator):
        """Test validator initialization."""
        assert isinstance(validator, QueryValidator)
        assert hasattr(validator, 'VALID_STATUSES')
        assert hasattr(validator, 'VALID_PROPERTY_TYPES')
        assert hasattr(validator, 'US_STATES')
    
    def test_validate_search_filters_basic(self, validator):
        """Test basic filter validation."""
        filters = {
            "city": "Austin",
            "state": "TX",
            "min_price": 300000,
            "max_price": 500000,
            "min_bedrooms": 3,
            "min_bathrooms": 2.0
        }
        
        result = validator.validate_search_filters(filters)
        
        assert result["city"] == "Austin"
        assert result["state"] == "TX"
        assert result["min_price"] == 300000
        assert result["max_price"] == 500000
        assert result["min_bedrooms"] == 3
        assert result["min_bathrooms"] == 2.0
    
    def test_validate_search_filters_invalid_input(self, validator):
        """Test validation with invalid input type."""
        with pytest.raises(ValidationError, match="Filters must be a dictionary"):
            validator.validate_search_filters("not a dict")
    
    def test_validate_city_valid(self, validator):
        """Test city validation with valid inputs."""
        assert validator._validate_city("Austin") == "Austin"
        assert validator._validate_city("new york") == "New York"
        assert validator._validate_city("San Francisco") == "San Francisco"
        assert validator._validate_city("O'Fallon") == "O'Fallon"
        assert validator._validate_city("Winston-Salem") == "Winston-Salem"
    
    def test_validate_city_invalid(self, validator):
        """Test city validation with invalid inputs."""
        with pytest.raises(ValidationError, match="City must be a string"):
            validator._validate_city(123)
        
        with pytest.raises(ValidationError, match="City name must be at least 2 characters"):
            validator._validate_city("A")
        
        with pytest.raises(ValidationError, match="City name too long"):
            validator._validate_city("A" * 101)
        
        with pytest.raises(ValidationError, match="City name contains invalid characters"):
            validator._validate_city("Austin123")
    
    def test_validate_state_valid(self, validator):
        """Test state validation with valid inputs."""
        assert validator._validate_state("TX") == "TX"
        assert validator._validate_state("tx") == "TX"
        assert validator._validate_state("  CA  ") == "CA"
    
    def test_validate_state_invalid(self, validator):
        """Test state validation with invalid inputs."""
        with pytest.raises(ValidationError, match="State must be a string"):
            validator._validate_state(123)
        
        with pytest.raises(ValidationError, match="Invalid state abbreviation"):
            validator._validate_state("XX")
        
        with pytest.raises(ValidationError, match="Invalid state abbreviation"):
            validator._validate_state("Texas")
    
    def test_validate_zip_code_valid(self, validator):
        """Test ZIP code validation with valid inputs."""
        assert validator._validate_zip_code("78701") == "78701"
        assert validator._validate_zip_code("78701-1234") == "78701-1234"
        assert validator._validate_zip_code("787011234") == "787011234"
        assert validator._validate_zip_code(78701) == "78701"
    
    def test_validate_zip_code_invalid(self, validator):
        """Test ZIP code validation with invalid inputs."""
        with pytest.raises(ValidationError, match="ZIP code must be a string or number"):
            validator._validate_zip_code([])
        
        with pytest.raises(ValidationError, match="Invalid ZIP code format"):
            validator._validate_zip_code("1234")
        
        with pytest.raises(ValidationError, match="Invalid ZIP code format"):
            validator._validate_zip_code("78701-12")
    
    def test_validate_price_valid(self, validator):
        """Test price validation with valid inputs."""
        assert validator._validate_price(450000) == 450000
        assert validator._validate_price("450000") == 450000
        assert validator._validate_price("$450,000") == 450000
        assert validator._validate_price(450000.99) == 450000
    
    def test_validate_price_invalid(self, validator):
        """Test price validation with invalid inputs."""
        with pytest.raises(ValidationError, match="Price cannot be negative"):
            validator._validate_price(-1000)
        
        with pytest.raises(ValidationError, match="Price too high"):
            validator._validate_price(200000000)
        
        with pytest.raises(ValidationError, match="Invalid price format"):
            validator._validate_price("not a price")
    
    def test_validate_room_count_valid(self, validator):
        """Test room count validation with valid inputs."""
        assert validator._validate_room_count(3, "bedrooms") == 3
        assert validator._validate_room_count("3", "bedrooms") == 3
        assert validator._validate_room_count(0, "bedrooms") == 0
    
    def test_validate_room_count_invalid(self, validator):
        """Test room count validation with invalid inputs."""
        with pytest.raises(ValidationError, match="Bedrooms count cannot be negative"):
            validator._validate_room_count(-1, "bedrooms")
        
        with pytest.raises(ValidationError, match="Bedrooms count too high"):
            validator._validate_room_count(25, "bedrooms")
        
        with pytest.raises(ValidationError, match="Invalid bedrooms count"):
            validator._validate_room_count("not a number", "bedrooms")
    
    def test_validate_bathroom_count_valid(self, validator):
        """Test bathroom count validation with valid inputs."""
        assert validator._validate_bathroom_count(2.5) == 2.5
        assert validator._validate_bathroom_count("2.5") == 2.5
        assert validator._validate_bathroom_count(2.3) == 2.5  # Rounded to nearest 0.5
        assert validator._validate_bathroom_count(2.7) == 2.5
        assert validator._validate_bathroom_count(3.0) == 3.0
    
    def test_validate_bathroom_count_invalid(self, validator):
        """Test bathroom count validation with invalid inputs."""
        with pytest.raises(ValidationError, match="Bathroom count cannot be negative"):
            validator._validate_bathroom_count(-1)
        
        with pytest.raises(ValidationError, match="Bathroom count too high"):
            validator._validate_bathroom_count(25)
    
    def test_validate_sqft_valid(self, validator):
        """Test square footage validation with valid inputs."""
        assert validator._validate_sqft(2100) == 2100
        assert validator._validate_sqft("2100") == 2100
        assert validator._validate_sqft("2,100") == 2100
        assert validator._validate_sqft(2100.5) == 2100
    
    def test_validate_sqft_invalid(self, validator):
        """Test square footage validation with invalid inputs."""
        with pytest.raises(ValidationError, match="Square footage cannot be negative"):
            validator._validate_sqft(-1)
        
        with pytest.raises(ValidationError, match="Square footage too high"):
            validator._validate_sqft(100000)
    
    def test_validate_property_type_valid(self, validator):
        """Test property type validation with valid inputs."""
        assert validator._validate_property_type("residential") == "residential"
        assert validator._validate_property_type("CONDO") == "condo"
        assert validator._validate_property_type("  single_family  ") == "single_family"
    
    def test_validate_property_type_invalid(self, validator):
        """Test property type validation with invalid inputs."""
        with pytest.raises(ValidationError, match="Property type must be a string"):
            validator._validate_property_type(123)
        
        with pytest.raises(ValidationError, match="Invalid property type"):
            validator._validate_property_type("mansion")
    
    def test_validate_status_valid(self, validator):
        """Test status validation with valid inputs."""
        assert validator._validate_status("active") == "active"
        assert validator._validate_status("PENDING") == "pending"
        assert validator._validate_status("  sold  ") == "sold"
    
    def test_validate_status_invalid(self, validator):
        """Test status validation with invalid inputs."""
        with pytest.raises(ValidationError, match="Status must be a string"):
            validator._validate_status(123)
        
        with pytest.raises(ValidationError, match="Invalid status"):
            validator._validate_status("unknown_status")
    
    def test_validate_listing_id_valid(self, validator):
        """Test listing ID validation with valid inputs."""
        assert validator._validate_listing_id("TEST123") == "TEST123"
        assert validator._validate_listing_id(123456) == "123456"
        assert validator._validate_listing_id("  TEST123  ") == "TEST123"
    
    def test_validate_listing_id_invalid(self, validator):
        """Test listing ID validation with invalid inputs."""
        with pytest.raises(ValidationError, match="Listing ID must be a string or number"):
            validator._validate_listing_id([])
        
        with pytest.raises(ValidationError, match="Listing ID cannot be empty"):
            validator._validate_listing_id("")
        
        with pytest.raises(ValidationError, match="Listing ID too long"):
            validator._validate_listing_id("A" * 51)
    
    def test_price_range_consistency(self, validator):
        """Test price range consistency validation."""
        with pytest.raises(ValidationError, match="Minimum price must be less than maximum price"):
            validator.validate_search_filters({
                "min_price": 500000,
                "max_price": 300000
            })
    
    def test_sqft_range_consistency(self, validator):
        """Test square footage range consistency validation."""
        with pytest.raises(ValidationError, match="Minimum square footage must be less than maximum"):
            validator.validate_search_filters({
                "min_sqft": 3000,
                "max_sqft": 2000
            })
    
    def test_parse_natural_language_query_basic(self, validator):
        """Test basic natural language query parsing."""
        query = "3 bedroom house under $500k in Austin TX"
        result = validator.parse_natural_language_query(query)
        
        assert result["min_bedrooms"] == 3
        assert result["max_price"] == 500000
        assert result["city"] == "Austin"
        assert result["state"] == "TX"
        assert result["property_type"] == "single_family"
    
    def test_parse_natural_language_query_price_patterns(self, validator):
        """Test price pattern extraction from natural language."""
        # Under/below/less than
        result = validator.parse_natural_language_query("houses under $400k")
        assert result["max_price"] == 400000
        
        result = validator.parse_natural_language_query("homes below 450000")
        assert result["max_price"] == 450000
        
        result = validator.parse_natural_language_query("properties less than $350k")
        assert result["max_price"] == 350000
        
        # Over/above/more than
        result = validator.parse_natural_language_query("houses over $600k")
        assert result["min_price"] == 600000
        
        result = validator.parse_natural_language_query("homes above 700000")
        assert result["min_price"] == 700000
        
        # Price ranges
        result = validator.parse_natural_language_query("homes $300k-$500k")
        assert result["min_price"] == 300000
        assert result["max_price"] == 500000
        
        result = validator.parse_natural_language_query("between $400k and $600k")
        assert result["min_price"] == 400000
        assert result["max_price"] == 600000
    
    def test_parse_natural_language_query_bedroom_patterns(self, validator):
        """Test bedroom pattern extraction."""
        result = validator.parse_natural_language_query("3 bedroom house")
        assert result["min_bedrooms"] == 3
        
        result = validator.parse_natural_language_query("4br home")
        assert result["min_bedrooms"] == 4
        
        result = validator.parse_natural_language_query("5 bed property")
        assert result["min_bedrooms"] == 5
    
    def test_parse_natural_language_query_bathroom_patterns(self, validator):
        """Test bathroom pattern extraction."""
        result = validator.parse_natural_language_query("2.5 bathroom house")
        assert result["min_bathrooms"] == 2.5
        
        result = validator.parse_natural_language_query("3ba home")
        assert result["min_bathrooms"] == 3.0
        
        result = validator.parse_natural_language_query("2 bath property")
        assert result["min_bathrooms"] == 2.0
    
    def test_parse_natural_language_query_sqft_patterns(self, validator):
        """Test square footage pattern extraction."""
        result = validator.parse_natural_language_query("2000 sqft house")
        assert result["sqft"] == 2000
        
        result = validator.parse_natural_language_query("over 2500 sq ft")
        assert result["min_sqft"] == 2500
        
        result = validator.parse_natural_language_query("under 1800 square feet")
        assert result["max_sqft"] == 1800
        
        result = validator.parse_natural_language_query("3000 sf home")
        assert result["sqft"] == 3000
    
    def test_parse_natural_language_query_property_types(self, validator):
        """Test property type pattern extraction."""
        result = validator.parse_natural_language_query("single family home")
        assert result["property_type"] == "single_family"
        
        result = validator.parse_natural_language_query("condo in downtown")
        assert result["property_type"] == "condo"
        
        result = validator.parse_natural_language_query("townhouse for sale")
        assert result["property_type"] == "townhouse"
        
        result = validator.parse_natural_language_query("commercial property")
        assert result["property_type"] == "commercial"
    
    def test_parse_natural_language_query_location(self, validator):
        """Test location extraction from natural language."""
        result = validator.parse_natural_language_query("house in Austin")
        assert result["city"] == "Austin"
        
        result = validator.parse_natural_language_query("homes in San Antonio TX")
        assert result["city"] == "San Antonio"
        assert result["state"] == "TX"
        
        result = validator.parse_natural_language_query("property in Houston, TX")
        assert result["city"] == "Houston"
        assert result["state"] == "TX"
    
    def test_parse_natural_language_query_complex(self, validator):
        """Test complex natural language query parsing."""
        query = "3 bedroom 2.5 bath single family house in Austin TX under $500k with over 2000 sqft"
        result = validator.parse_natural_language_query(query)
        
        assert result["min_bedrooms"] == 3
        assert result["min_bathrooms"] == 2.5
        assert result["property_type"] == "single_family"
        assert result["city"] == "Austin"
        assert result["state"] == "TX"
        assert result["max_price"] == 500000
        assert result["min_sqft"] == 2000
    
    def test_parse_natural_language_query_invalid_input(self, validator):
        """Test natural language parsing with invalid input."""
        with pytest.raises(ValidationError, match="Query must be a string"):
            validator.parse_natural_language_query(123)
    
    def test_extract_price_info_k_suffix(self, validator):
        """Test price extraction with 'k' suffix."""
        result = validator._extract_price_info("under 500k")
        assert result["max_price"] == 500000
        
        result = validator._extract_price_info("over 750k")
        assert result["min_price"] == 750000
    
    def test_parse_price_value_with_commas(self, validator):
        """Test price parsing with commas."""
        assert validator._parse_price_value("450,000") == 450000
        assert validator._parse_price_value("1,200,000") == 1200000
        assert validator._parse_price_value("500k") == 500000
    
    def test_parse_price_value_invalid(self, validator):
        """Test price parsing with invalid values."""
        assert validator._parse_price_value("invalid") is None
        assert validator._parse_price_value("") is None
    
    def test_empty_query_parsing(self, validator):
        """Test parsing of empty or minimal queries."""
        result = validator.parse_natural_language_query("")
        assert result == {}
        
        result = validator.parse_natural_language_query("   ")
        assert result == {}
        
        result = validator.parse_natural_language_query("house")
        # Should still parse as single family even with minimal query
        assert result.get("property_type") == "single_family"