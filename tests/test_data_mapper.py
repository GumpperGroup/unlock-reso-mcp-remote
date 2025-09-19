"""Tests for RESO data mapping utilities."""

import pytest
from datetime import datetime

from src.utils.data_mapper import ResoDataMapper


class TestResoDataMapper:
    """Test cases for ResoDataMapper class."""
    
    @pytest.fixture
    def mapper(self):
        """Create data mapper instance."""
        return ResoDataMapper()
    
    @pytest.fixture
    def sample_reso_property(self):
        """Sample RESO property data."""
        return {
            "ListingId": "TEST123456",
            "ListingKey": "TEST123456-KEY", 
            "StandardStatus": "Active",
            "ListPrice": 450000,
            "OriginalListPrice": 475000,
            "ClosePrice": None,
            "BedroomsTotal": 3,
            "BathroomsTotalInteger": 2,
            "BathroomsFull": 2,
            "BathroomsHalf": 0,
            "LivingArea": 2100,
            "LotSizeAcres": 0.25,
            "LotSizeSquareFeet": 10890,
            "YearBuilt": 2018,
            "Stories": 2.0,
            "GarageSpaces": 2,
            "ParkingTotal": 2,
            "PropertyType": "Residential",
            "PropertySubType": "Single Family Residence",
            "StreetNumber": "1234",
            "StreetDirPrefix": "N",
            "StreetName": "Main",
            "StreetSuffix": "St",
            "StreetDirSuffix": "",
            "UnitNumber": "",
            "City": "Austin",
            "StateOrProvince": "TX",
            "PostalCode": "78701",
            "CountyOrParish": "Travis",
            "SubdivisionName": "Test Subdivision",
            "Latitude": 30.2672,
            "Longitude": -97.7431,
            "OnMarketDate": "2024-01-15T10:30:00Z",
            "ModificationTimestamp": "2024-01-16T14:45:00Z",
            "CloseDate": None,
            "ContractStatusChangeDate": None,
            "PoolFeatures": "Private",
            "FireplaceFeatures": "Gas Log",
            "WaterBodyName": None,
            "View": "City",
            "ElementarySchool": "Test Elementary",
            "MiddleOrJuniorSchool": "Test Middle",
            "HighSchool": "Test High",
            "ListAgentFirstName": "John",
            "ListAgentLastName": "Doe",
            "ListAgentFullName": "John Doe",
            "ListOfficeName": "Test Realty",
            "ListAgentDirectPhone": "512-555-0123",
            "ListAgentEmail": "john.doe@testrealty.com",
            "PublicRemarks": "Beautiful home in great neighborhood!",
            "PrivateRemarks": "Seller motivated",
            "ShowingInstructions": "Call listing agent"
        }
    
    def test_initialization(self, mapper):
        """Test mapper initialization."""
        assert isinstance(mapper, ResoDataMapper)
        assert hasattr(mapper, 'STATUS_MAPPING')
        assert hasattr(mapper, 'PROPERTY_TYPE_MAPPING')
    
    def test_map_property_basic_fields(self, mapper, sample_reso_property):
        """Test mapping of basic property fields."""
        result = mapper.map_property(sample_reso_property)
        
        assert result["listing_id"] == "TEST123456"
        assert result["listing_key"] == "TEST123456-KEY"
        assert result["mls_number"] == "TEST123456"
        assert result["status"] == "active"
        assert result["list_price"] == 450000
        assert result["original_list_price"] == 475000
        assert result["bedrooms"] == 3
        assert result["bathrooms"] == 2.0
        assert result["square_feet"] == 2100
        assert result["property_type"] == "single_family"
    
    def test_map_property_location_fields(self, mapper, sample_reso_property):
        """Test mapping of location fields."""
        result = mapper.map_property(sample_reso_property)
        
        assert result["address"] == "1234 N Main St"
        assert result["city"] == "Austin"
        assert result["state"] == "TX"
        assert result["zip_code"] == "78701"
        assert result["county"] == "Travis"
        assert result["subdivision"] == "Test Subdivision"
        assert result["latitude"] == 30.2672
        assert result["longitude"] == -97.7431
    
    def test_map_property_dates(self, mapper, sample_reso_property):
        """Test mapping of date fields."""
        result = mapper.map_property(sample_reso_property)
        
        assert result["list_date"] == "2024-01-15"
        assert result["modification_date"] == "2024-01-16"
        assert "sold_date" not in result  # Should be excluded when None
        assert "contract_date" not in result
    
    def test_map_property_features(self, mapper, sample_reso_property):
        """Test mapping of property features."""
        result = mapper.map_property(sample_reso_property)
        
        assert result["pool"] is True
        assert result["fireplace"] is True
        assert "waterfront" not in result  # Should be excluded when None
        assert result["view"] == "City"
        assert result["elementary_school"] == "Test Elementary"
    
    def test_map_property_agent_info(self, mapper, sample_reso_property):
        """Test mapping of agent information."""
        result = mapper.map_property(sample_reso_property)
        
        assert result["listing_agent_name"] == "John Doe"
        assert result["listing_office"] == "Test Realty"
        assert result["listing_agent_phone"] == "512-555-0123"
        assert result["listing_agent_email"] == "john.doe@testrealty.com"
    
    def test_map_property_empty_input(self, mapper):
        """Test mapping with empty input."""
        result = mapper.map_property({})
        assert result == {}
        
        result = mapper.map_property(None)
        assert result == {}
    
    def test_map_properties_list(self, mapper, sample_reso_property):
        """Test mapping multiple properties."""
        properties = [sample_reso_property, sample_reso_property.copy()]
        results = mapper.map_properties(properties)
        
        assert len(results) == 2
        assert all("listing_id" in prop for prop in results)
    
    def test_map_properties_empty_list(self, mapper):
        """Test mapping empty properties list."""
        result = mapper.map_properties([])
        assert result == []
        
        result = mapper.map_properties(None)
        assert result == []
    
    def test_format_address_complete(self, mapper):
        """Test address formatting with all components."""
        property_data = {
            "StreetNumber": "1234",
            "StreetDirPrefix": "N",
            "StreetName": "Main",
            "StreetSuffix": "St",
            "StreetDirSuffix": "NW",
            "UnitNumber": "A"
        }
        
        address = mapper._format_address(property_data)
        assert address == "1234 N Main St NW Unit A"
    
    def test_format_address_minimal(self, mapper):
        """Test address formatting with minimal components."""
        property_data = {
            "StreetNumber": "123",
            "StreetName": "Oak",
            "StreetSuffix": "Ave"
        }
        
        address = mapper._format_address(property_data)
        assert address == "123 Oak Ave"
    
    def test_format_address_empty(self, mapper):
        """Test address formatting with no components."""
        address = mapper._format_address({})
        assert address is None
    
    def test_format_price_valid(self, mapper):
        """Test price formatting with valid inputs."""
        assert mapper._format_price(450000) == 450000
        assert mapper._format_price("450000") == 450000
        assert mapper._format_price("$450,000") == 450000
        assert mapper._format_price(450000.99) == 450000
    
    def test_format_price_invalid(self, mapper):
        """Test price formatting with invalid inputs."""
        assert mapper._format_price(None) is None
        assert mapper._format_price("") is None
        assert mapper._format_price("invalid") is None
    
    def test_format_date_valid(self, mapper):
        """Test date formatting with valid inputs."""
        assert mapper._format_date("2024-01-15T10:30:00Z") == "2024-01-15"
        assert mapper._format_date("2024-01-15T10:30:00") == "2024-01-15"
        assert mapper._format_date("2024-01-15") == "2024-01-15"
        
        dt = datetime(2024, 1, 15)
        assert mapper._format_date(dt) == "2024-01-15"
    
    def test_format_date_invalid(self, mapper):
        """Test date formatting with invalid inputs."""
        assert mapper._format_date(None) is None
        assert mapper._format_date("") is None
        assert mapper._format_date("invalid") is None
    
    def test_format_agent_name_complete(self, mapper):
        """Test agent name formatting with first and last name."""
        property_data = {
            "ListAgentFirstName": "John",
            "ListAgentLastName": "Doe"
        }
        
        name = mapper._format_agent_name(property_data)
        assert name == "John Doe"
    
    def test_format_agent_name_last_only(self, mapper):
        """Test agent name formatting with last name only."""
        property_data = {
            "ListAgentLastName": "Doe"
        }
        
        name = mapper._format_agent_name(property_data)
        assert name == "Doe"
    
    def test_format_agent_name_full_name_fallback(self, mapper):
        """Test agent name formatting with full name fallback."""
        property_data = {
            "ListAgentFullName": "John Doe"
        }
        
        name = mapper._format_agent_name(property_data)
        assert name == "John Doe"
    
    def test_map_status_valid(self, mapper):
        """Test status mapping with valid statuses."""
        assert mapper._map_status("Active") == "active"
        assert mapper._map_status("Pending") == "pending"
        assert mapper._map_status("Sold") == "sold"
    
    def test_map_status_invalid(self, mapper):
        """Test status mapping with invalid/unknown statuses."""
        assert mapper._map_status("Unknown") == "unknown"
        assert mapper._map_status(None) is None
    
    def test_map_property_type_valid(self, mapper):
        """Test property type mapping with valid types."""
        assert mapper._map_property_type("Residential") == "residential"
        assert mapper._map_property_type("Condominium") == "condo"
        assert mapper._map_property_type("Single Family Residence") == "single_family"
    
    def test_map_property_type_invalid(self, mapper):
        """Test property type mapping with invalid types."""
        assert mapper._map_property_type("Unknown") == "unknown"
        assert mapper._map_property_type(None) is None
    
    def test_has_feature_valid(self, mapper):
        """Test feature detection with valid inputs."""
        assert mapper._has_feature("Private") is True
        assert mapper._has_feature("Gas Log") is True
        assert mapper._has_feature("None") is False
        assert mapper._has_feature("N/A") is False
        assert mapper._has_feature("No") is False
    
    def test_has_feature_invalid(self, mapper):
        """Test feature detection with invalid inputs."""
        assert mapper._has_feature(None) is None
        assert mapper._has_feature("") is None
    
    def test_safe_conversions(self, mapper):
        """Test safe type conversions."""
        # Test safe_int
        assert mapper._safe_int(123) == 123
        assert mapper._safe_int("123") == 123
        assert mapper._safe_int("123.5") == 123
        assert mapper._safe_int(None) is None
        assert mapper._safe_int("invalid") is None
        
        # Test safe_float
        assert mapper._safe_float(123.5) == 123.5
        assert mapper._safe_float("123.5") == 123.5
        assert mapper._safe_float(123) == 123.0
        assert mapper._safe_float(None) is None
        assert mapper._safe_float("invalid") is None
    
    def test_get_property_summary(self, mapper, sample_reso_property):
        """Test property summary generation."""
        mapped_property = mapper.map_property(sample_reso_property)
        summary = mapper.get_property_summary(mapped_property)
        
        assert "3BR/2.0BA" in summary
        assert "2,100 sqft" in summary
        assert "Single Family" in summary
        assert "Austin TX" in summary
        assert "$450,000" in summary
    
    def test_original_data_preservation(self, mapper, sample_reso_property):
        """Test that original data is preserved in mapping."""
        result = mapper.map_property(sample_reso_property)
        
        assert "_original" in result
        assert result["_original"] == sample_reso_property
    
    def test_none_value_exclusion(self, mapper):
        """Test that None values are excluded from mapped data."""
        property_data = {
            "ListingId": "TEST123",
            "ListPrice": None,
            "City": "Austin",
            "EmptyField": None
        }
        
        result = mapper.map_property(property_data)
        
        assert "listing_id" in result
        assert "city" in result
        assert "list_price" not in result
        assert "EmptyField" not in result