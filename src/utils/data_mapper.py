"""RESO data mapping utilities for standardizing property data format."""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal
import logging

from ..config.logging_config import setup_logging

logger = setup_logging(__name__)


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
    
    # Standard fields to always include in mapped data
    STANDARD_FIELDS = [
        "ListingId", "ListingKey", "StandardStatus", "ListPrice",
        "BedroomsTotal", "BathroomsTotalInteger", "LivingArea",
        "PropertyType", "PropertySubType", "City", "StateOrProvince",
        "PostalCode", "ModificationTimestamp", "OnMarketDate"
    ]
    
    def __init__(self):
        """Initialize the data mapper."""
        logger.info("ResoDataMapper initialized")
    
    def map_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map a single property record to standardized format.
        
        Args:
            property_data: Raw RESO property data
            
        Returns:
            Standardized property data
        """
        if not property_data:
            return {}
        
        logger.debug("Mapping property: %s", property_data.get("ListingId", "unknown"))
        
        mapped = {
            # Basic identifiers
            "listing_id": property_data.get("ListingId"),
            "listing_key": property_data.get("ListingKey"),
            "mls_number": property_data.get("ListingId"),  # Alias for compatibility
            
            # Status and pricing
            "status": self._map_status(property_data.get("StandardStatus")),
            "list_price": self._format_price(property_data.get("ListPrice")),
            "original_list_price": self._format_price(property_data.get("OriginalListPrice")),
            "sold_price": self._format_price(property_data.get("ClosePrice")),
            
            # Property details
            "bedrooms": self._safe_int(property_data.get("BedroomsTotal")),
            "bathrooms": self._safe_float(property_data.get("BathroomsTotalInteger")),
            "full_bathrooms": self._safe_int(property_data.get("BathroomsFull")),
            "half_bathrooms": self._safe_int(property_data.get("BathroomsHalf")),
            "square_feet": self._safe_int(property_data.get("LivingArea")),
            "lot_size": self._safe_float(property_data.get("LotSizeAcres")),
            "lot_size_sqft": self._safe_int(property_data.get("LotSizeSquareFeet")),
            "year_built": self._safe_int(property_data.get("YearBuilt")),
            "stories": self._safe_float(property_data.get("Stories")),
            "garage_spaces": self._safe_int(property_data.get("GarageSpaces")),
            "parking_total": self._safe_int(property_data.get("ParkingTotal")),
            
            # Property type
            "property_type": self._map_property_type(
                property_data.get("PropertyType"), 
                property_data.get("PropertySubType")
            ),
            "property_subtype": property_data.get("PropertySubType"),
            
            # Location
            "address": self._format_address(property_data),
            "city": property_data.get("City"),
            "state": property_data.get("StateOrProvince"), 
            "zip_code": property_data.get("PostalCode"),
            "county": property_data.get("CountyOrParish"),
            "subdivision": property_data.get("SubdivisionName"),
            
            # Geographic coordinates
            "latitude": self._safe_float(property_data.get("Latitude")),
            "longitude": self._safe_float(property_data.get("Longitude")),
            
            # Dates
            "list_date": self._format_date(property_data.get("OnMarketDate")),
            "modification_date": self._format_date(property_data.get("ModificationTimestamp")),
            "sold_date": self._format_date(property_data.get("CloseDate")),
            "contract_date": self._format_date(property_data.get("ContractStatusChangeDate")),
            
            # Features and amenities
            "pool": self._has_feature(property_data.get("PoolFeatures")),
            "fireplace": self._has_feature(property_data.get("FireplaceFeatures")),
            "waterfront": self._has_feature(property_data.get("WaterBodyName")),
            "view": property_data.get("View"),
            "elementary_school": property_data.get("ElementarySchool"),
            "middle_school": property_data.get("MiddleOrJuniorSchool"),
            "high_school": property_data.get("HighSchool"),
            
            # Agent and office information
            "listing_agent_name": self._format_agent_name(property_data),
            "listing_office": property_data.get("ListOfficeName"),
            "listing_agent_phone": property_data.get("ListAgentDirectPhone"),
            "listing_agent_email": property_data.get("ListAgentEmail"),
            
            # Additional data
            "remarks": property_data.get("PublicRemarks"),
            "private_remarks": property_data.get("PrivateRemarks"),
            "showing_instructions": property_data.get("ShowingInstructions"),
            
            # Keep original data for reference
            "_original": property_data
        }
        
        # Remove None values
        mapped = {k: v for k, v in mapped.items() if v is not None}
        
        logger.debug("Property mapped successfully: %s", mapped.get("listing_id"))
        return mapped
    
    def map_properties(self, properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Map multiple property records.
        
        Args:
            properties: List of raw RESO property data
            
        Returns:
            List of standardized property data
        """
        if not properties:
            return []
        
        logger.info("Mapping %d properties", len(properties))
        mapped_properties = []
        
        for prop in properties:
            try:
                mapped = self.map_property(prop)
                if mapped:
                    mapped_properties.append(mapped)
            except Exception as e:
                logger.error("Error mapping property %s: %s", prop.get("ListingId", "unknown"), e)
                continue
        
        logger.info("Successfully mapped %d/%d properties", len(mapped_properties), len(properties))
        return mapped_properties
    
    def _format_address(self, property_data: Dict[str, Any]) -> Optional[str]:
        """
        Format address from individual components.
        
        Args:
            property_data: Property data containing address components
            
        Returns:
            Formatted address string or None
        """
        components = []
        
        # Street number and name
        street_number = property_data.get("StreetNumber", "").strip()
        street_dir_prefix = property_data.get("StreetDirPrefix", "").strip()
        street_name = property_data.get("StreetName", "").strip()
        street_suffix = property_data.get("StreetSuffix", "").strip()
        street_dir_suffix = property_data.get("StreetDirSuffix", "").strip()
        
        # Combine street components
        street_parts = [street_number, street_dir_prefix, street_name, street_suffix, street_dir_suffix]
        street_address = " ".join([part for part in street_parts if part])
        
        if street_address:
            components.append(street_address)
        
        # Unit number
        unit_number = property_data.get("UnitNumber", "").strip()
        if unit_number:
            components.append(f"Unit {unit_number}")
        
        return " ".join(components) if components else None
    
    def _format_price(self, price: Any) -> Optional[int]:
        """
        Format price as integer.
        
        Args:
            price: Price value
            
        Returns:
            Formatted price as integer or None
        """
        if price is None:
            return None
        
        try:
            if isinstance(price, str):
                # Remove currency symbols and commas
                price = re.sub(r'[^\d.]', '', price)
            
            return int(float(price))
        except (ValueError, TypeError):
            return None
    
    def _format_date(self, date_value: Any) -> Optional[str]:
        """
        Format date to ISO string.
        
        Args:
            date_value: Date value
            
        Returns:
            ISO formatted date string or None
        """
        if not date_value:
            return None
        
        try:
            if isinstance(date_value, str):
                # Parse common date formats
                for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]:
                    try:
                        dt = datetime.strptime(date_value.replace('Z', ''), fmt)
                        return dt.strftime("%Y-%m-%d")
                    except ValueError:
                        continue
            elif isinstance(date_value, datetime):
                return date_value.strftime("%Y-%m-%d")
        except Exception:
            pass
        
        return None
    
    def _format_agent_name(self, property_data: Dict[str, Any]) -> Optional[str]:
        """
        Format agent name from components.
        
        Args:
            property_data: Property data containing agent info
            
        Returns:
            Formatted agent name or None
        """
        first_name = property_data.get("ListAgentFirstName", "").strip()
        last_name = property_data.get("ListAgentLastName", "").strip()
        
        if first_name and last_name:
            return f"{first_name} {last_name}"
        elif last_name:
            return last_name
        elif first_name:
            return first_name
        else:
            return property_data.get("ListAgentFullName")
    
    def _map_status(self, status: Optional[str]) -> Optional[str]:
        """Map RESO status to standardized status."""
        if not status:
            return None
        return self.STATUS_MAPPING.get(status, status.lower())
    
    def _map_property_type(self, prop_type: Optional[str], prop_subtype: Optional[str] = None) -> Optional[str]:
        """Map RESO property type to standardized type."""
        if not prop_type:
            return None
        
        # Check subtype first for more specific mapping
        if prop_subtype:
            mapped_subtype = self.PROPERTY_TYPE_MAPPING.get(prop_subtype)
            if mapped_subtype:
                return mapped_subtype
        
        # Fall back to main property type
        return self.PROPERTY_TYPE_MAPPING.get(prop_type, prop_type.lower())
    
    def _has_feature(self, feature_value: Any) -> Optional[bool]:
        """
        Check if property has a specific feature.
        
        Args:
            feature_value: Feature value from RESO data
            
        Returns:
            True if feature exists, False if explicitly none, None if unknown
        """
        if not feature_value:
            return None
        
        if isinstance(feature_value, str):
            feature_lower = feature_value.lower()
            if feature_lower in ["none", "no", "n/a", "not applicable"]:
                return False
            else:
                return True
        
        return bool(feature_value)
    
    def _safe_int(self, value: Any) -> Optional[int]:
        """Safely convert value to integer."""
        if value is None:
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None
    
    def _safe_float(self, value: Any) -> Optional[float]:
        """Safely convert value to float."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def get_property_summary(self, property_data: Dict[str, Any]) -> str:
        """
        Generate a human-readable property summary.
        
        Args:
            property_data: Mapped property data
            
        Returns:
            Property summary string
        """
        parts = []
        
        # Basic info
        if property_data.get("bedrooms") and property_data.get("bathrooms"):
            parts.append(f"{property_data['bedrooms']}BR/{property_data['bathrooms']}BA")
        
        if property_data.get("square_feet"):
            parts.append(f"{property_data['square_feet']:,} sqft")
        
        if property_data.get("property_type"):
            parts.append(property_data["property_type"].replace("_", " ").title())
        
        # Location
        location_parts = []
        if property_data.get("city"):
            location_parts.append(property_data["city"])
        if property_data.get("state"):
            location_parts.append(property_data["state"])
        
        if location_parts:
            parts.append(" ".join(location_parts))
        
        # Price
        if property_data.get("list_price"):
            parts.append(f"${property_data['list_price']:,}")
        
        return " | ".join(parts)