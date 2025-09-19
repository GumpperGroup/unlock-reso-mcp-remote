"""Property data fixtures for comprehensive testing."""

from typing import Dict, Any, List, Optional
import random
from datetime import datetime, timedelta


class PropertyDataFixtures:
    """Comprehensive property data fixtures for all testing scenarios."""
    
    def __init__(self):
        self.cities = [
            "Austin", "Dallas", "Houston", "San Antonio", "Fort Worth", 
            "El Paso", "Arlington", "Corpus Christi", "Plano", "Lubbock"
        ]
        
        self.zip_codes = {
            "Austin": ["78701", "78702", "78703", "78704", "78705", "78729", "78730", "78731"],
            "Dallas": ["75201", "75202", "75203", "75204", "75205", "75206", "75207", "75208"],
            "Houston": ["77001", "77002", "77003", "77004", "77005", "77006", "77007", "77008"],
            "San Antonio": ["78201", "78202", "78203", "78204", "78205", "78206", "78207", "78208"]
        }
        
        self.property_types = ["Residential", "Condo", "Townhouse", "Multi-Family", "Land", "Commercial"]
        self.property_subtypes = {
            "Residential": ["Single Family Residence", "Single Family Detached", "Single Family Attached"],
            "Condo": ["Condominium", "High Rise Condo", "Garden Condo", "Loft"],
            "Townhouse": ["Townhouse", "Row House", "Patio Home"],
            "Multi-Family": ["Duplex", "Triplex", "Fourplex", "Multi-Family"],
            "Land": ["Vacant Land", "Farm/Ranch", "Residential Lot"],
            "Commercial": ["Office", "Retail", "Industrial", "Mixed Use"]
        }
        
        self.statuses = [
            "Active", "Under Contract", "Pending", "Sold", "Closed", 
            "Expired", "Withdrawn", "Cancelled", "Hold"
        ]
        
        self.pool_features = ["Private", "Community", "None", "Lap Pool", "Infinity", "Salt Water"]
        self.waterfront_types = ["Lake", "River", "Ocean", "Creek", "Pond", "None"]
        self.view_types = ["City", "Water", "Mountain", "Golf Course", "Garden", "None"]
        
        # Realistic price ranges by property type and city
        self.price_ranges = {
            "Austin": {"Residential": (300000, 800000), "Condo": (200000, 600000), "Townhouse": (250000, 500000)},
            "Dallas": {"Residential": (250000, 700000), "Condo": (150000, 500000), "Townhouse": (200000, 450000)},
            "Houston": {"Residential": (200000, 650000), "Condo": (120000, 400000), "Townhouse": (180000, 400000)},
            "San Antonio": {"Residential": (180000, 550000), "Condo": (100000, 350000), "Townhouse": (150000, 350000)}
        }
    
    def create_basic_property(self, listing_id: str = None, **overrides) -> Dict[str, Any]:
        """Create a basic property with realistic defaults."""
        if not listing_id:
            listing_id = f"PROP{random.randint(100000, 999999)}"
        
        city = random.choice(self.cities)
        property_type = random.choice(["Residential", "Condo", "Townhouse"])
        
        # Get realistic price range
        price_range = self.price_ranges.get(city, {}).get(property_type, (200000, 600000))
        list_price = random.randint(price_range[0], price_range[1])
        
        # Calculate other attributes based on price
        bedrooms = random.choices([2, 3, 4, 5], weights=[20, 40, 30, 10])[0]
        bathrooms = random.choices([1, 2, 3, 4], weights=[10, 50, 30, 10])[0]
        living_area = random.randint(1200, 4000)
        
        property_data = {
            "ListingId": listing_id,
            "StandardStatus": random.choice(["Active", "Under Contract", "Pending"]),
            "ListPrice": list_price,
            "OriginalListPrice": list_price + random.randint(-50000, 50000),
            "BedroomsTotal": bedrooms,
            "BathroomsTotalInteger": bathrooms,
            "BathroomsFull": max(1, bathrooms - random.randint(0, 1)),
            "BathroomsHalf": random.randint(0, 1),
            "LivingArea": living_area,
            "PropertyType": property_type,
            "PropertySubType": random.choice(self.property_subtypes[property_type]),
            "City": city,
            "StateOrProvince": "TX",
            "PostalCode": random.choice(self.zip_codes.get(city, ["78701"])),
            "UnparsedAddress": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Cedar', 'Elm'])} {random.choice(['St', 'Ave', 'Dr', 'Ln', 'Ct'])}",
            "YearBuilt": random.randint(1980, 2023),
            "LotSizeAcres": round(random.uniform(0.1, 2.0), 2),
            "GarageSpaces": random.randint(0, 3),
            "PoolFeatures": random.choice(self.pool_features),
            "WaterfrontFeatures": random.choice(self.waterfront_types),
            "View": random.choice(self.view_types),
            "PublicRemarks": f"Beautiful {property_type.lower()} in {city} with {bedrooms} bedrooms and {bathrooms} bathrooms. Perfect for families!",
            "ListingContractDate": (datetime.now() - timedelta(days=random.randint(1, 180))).isoformat(),
            "OnMarketDate": (datetime.now() - timedelta(days=random.randint(1, 200))).isoformat(),
            "ModificationTimestamp": datetime.now().isoformat(),
            "ListAgentFirstName": random.choice(["John", "Jane", "Michael", "Sarah", "David", "Lisa"]),
            "ListAgentLastName": random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]),
            "ListOfficeName": random.choice(["Premier Realty", "Best Homes", "Elite Properties", "Top Agents"]),
            "ListOfficePhone": f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
        }
        
        # Apply any overrides
        property_data.update(overrides)
        return property_data
    
    def create_sold_property(self, listing_id: str = None, **overrides) -> Dict[str, Any]:
        """Create a sold property with sale information."""
        property_data = self.create_basic_property(listing_id, **overrides)
        
        # Convert to sold property
        list_price = property_data["ListPrice"]
        close_price = list_price + random.randint(-50000, 20000)  # Slightly favor below list
        
        sold_updates = {
            "StandardStatus": "Sold",
            "ClosePrice": close_price,
            "CloseDate": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
            "ContractDate": (datetime.now() - timedelta(days=random.randint(30, 180))).isoformat(),
            "DaysOnMarket": random.randint(1, 180),
            "CumulativeDaysOnMarket": random.randint(1, 200)
        }
        
        property_data.update(sold_updates)
        return property_data
    
    def create_luxury_property(self, listing_id: str = None, **overrides) -> Dict[str, Any]:
        """Create a luxury property with premium features."""
        property_data = self.create_basic_property(listing_id, **overrides)
        
        # Upgrade to luxury specifications
        luxury_updates = {
            "ListPrice": random.randint(800000, 2000000),
            "OriginalListPrice": property_data["ListPrice"] + random.randint(0, 100000),
            "BedroomsTotal": random.randint(4, 6),
            "BathroomsTotalInteger": random.randint(3, 5),
            "BathroomsFull": random.randint(3, 4),
            "BathroomsHalf": random.randint(1, 2),
            "LivingArea": random.randint(3500, 8000),
            "LotSizeAcres": round(random.uniform(1.0, 5.0), 2),
            "GarageSpaces": random.randint(2, 4),
            "PoolFeatures": random.choice(["Private", "Infinity", "Salt Water", "Lap Pool"]),
            "WaterfrontFeatures": random.choice(["Lake", "River", "Ocean"]),
            "View": random.choice(["City", "Water", "Mountain", "Golf Course"]),
            "PublicRemarks": "Stunning luxury estate with premium finishes, gourmet kitchen, master suite with spa-like bathroom, and resort-style backyard. Perfect for entertaining!",
            "Fireplaces": random.randint(1, 3),
            "PatioAndPorchFeatures": "Covered Patio, Outdoor Kitchen, Fireplace",
            "SecurityFeatures": "Security System, Gated Community"
        }
        
        property_data.update(luxury_updates)
        return property_data
    
    def create_condo_property(self, listing_id: str = None, **overrides) -> Dict[str, Any]:
        """Create a condominium property with specific condo features."""
        property_data = self.create_basic_property(listing_id, **overrides)
        
        condo_updates = {
            "PropertyType": "Condo",
            "PropertySubType": random.choice(["Condominium", "High Rise Condo", "Garden Condo", "Loft"]),
            "BedroomsTotal": random.randint(1, 3),
            "BathroomsTotalInteger": random.randint(1, 2),
            "LivingArea": random.randint(800, 2200),
            "GarageSpaces": random.randint(0, 2),
            "LotSizeAcres": 0,  # Condos don't have individual lots
            "PoolFeatures": "Community",
            "AssociationFee": random.randint(200, 800),
            "AssociationFeeFrequency": "Monthly",
            "BuildingAreaTotal": random.randint(50000, 200000),
            "BuildingName": f"The {random.choice(['Plaza', 'Tower', 'Gardens', 'Residence', 'Metropolitan'])}",
            "FloorNumber": random.randint(1, 30),
            "TotalActualRent": random.randint(1500, 4000),
            "PublicRemarks": f"Beautiful condo in {property_data['City']} with modern amenities and great location. Building features pool, fitness center, and concierge services."
        }
        
        property_data.update(condo_updates)
        return property_data
    
    def create_new_construction(self, listing_id: str = None, **overrides) -> Dict[str, Any]:
        """Create a new construction property."""
        property_data = self.create_basic_property(listing_id, **overrides)
        
        new_construction_updates = {
            "YearBuilt": random.choice([2023, 2024, None]),  # None for under construction
            "StandardStatus": random.choice(["Active", "Under Contract"]),
            "NewConstructionYN": True,
            "OriginalListPrice": property_data["ListPrice"],  # Same as list for new construction
            "BuilderName": random.choice(["KB Home", "Lennar", "Pulte", "DR Horton", "David Weekley"]),
            "PublicRemarks": "Brand new construction home with modern design, energy-efficient features, and builder warranty. Ready for immediate occupancy!",
            "ConstructionMaterials": "Brick, Fiber Cement Siding",
            "Heating": "Central Air, Electric",
            "Cooling": "Central Air",
            "AppliancesIncluded": "Dishwasher, Disposal, Microwave, Range Electric, Refrigerator",
            "LaundryFeatures": "Electric Connections, Washer/Dryer Connections"
        }
        
        property_data.update(new_construction_updates)
        return property_data
    
    def create_investment_property(self, listing_id: str = None, **overrides) -> Dict[str, Any]:
        """Create an investment property with rental information."""
        property_data = self.create_basic_property(listing_id, **overrides)
        
        # Calculate rental yield based on price
        list_price = property_data["ListPrice"]
        monthly_rent = int(list_price * 0.008)  # Rough 0.8% monthly yield
        
        investment_updates = {
            "PropertyType": random.choice(["Multi-Family", "Residential"]),
            "PropertySubType": random.choice(["Duplex", "Triplex", "Single Family Residence"]),
            "TotalActualRent": monthly_rent,
            "RentIncludes": "None",
            "LeaseExpiration": (datetime.now() + timedelta(days=random.randint(90, 730))).isoformat(),
            "CurrentFinancing": "Conventional",
            "PossibleUse": "Rental, Investment",
            "PublicRemarks": f"Excellent investment opportunity! Currently generating ${monthly_rent}/month in rental income. Great cash flow property in desirable {property_data['City']} location.",
            "YearBuilt": random.randint(1970, 2010),  # Older properties common for investment
            "PropertyCondition": random.choice(["Excellent", "Good", "Average"])
        }
        
        property_data.update(investment_updates)
        return property_data
    
    def create_price_reduced_property(self, listing_id: str = None, **overrides) -> Dict[str, Any]:
        """Create a property with price reduction history."""
        property_data = self.create_basic_property(listing_id, **overrides)
        
        # Create price reduction scenario
        current_price = property_data["ListPrice"]
        original_price = current_price + random.randint(25000, 100000)
        
        price_reduced_updates = {
            "OriginalListPrice": original_price,
            "ListPrice": current_price,
            "PriceChangeTimestamp": (datetime.now() - timedelta(days=random.randint(7, 60))).isoformat(),
            "DaysOnMarket": random.randint(60, 200),
            "CumulativeDaysOnMarket": random.randint(60, 250),
            "PublicRemarks": f"PRICE REDUCED! Motivated seller. Beautiful {property_data['PropertyType'].lower()} reduced from ${original_price:,} to ${current_price:,}. Don't miss this opportunity!",
            "ListingTerms": "Cash, Conventional, FHA, VA"
        }
        
        property_data.update(price_reduced_updates)
        return property_data
    
    def create_property_dataset(self, count: int, property_types: List[str] = None) -> List[Dict[str, Any]]:
        """Create a dataset of diverse properties."""
        if property_types is None:
            property_types = ["basic", "luxury", "condo", "investment", "new_construction", "sold", "price_reduced"]
        
        properties = []
        for i in range(count):
            property_type = random.choice(property_types)
            listing_id = f"DATASET{i:06d}"
            
            if property_type == "basic":
                prop = self.create_basic_property(listing_id)
            elif property_type == "luxury":
                prop = self.create_luxury_property(listing_id)
            elif property_type == "condo":
                prop = self.create_condo_property(listing_id)
            elif property_type == "investment":
                prop = self.create_investment_property(listing_id)
            elif property_type == "new_construction":
                prop = self.create_new_construction(listing_id)
            elif property_type == "sold":
                prop = self.create_sold_property(listing_id)
            elif property_type == "price_reduced":
                prop = self.create_price_reduced_property(listing_id)
            else:
                prop = self.create_basic_property(listing_id)
            
            properties.append(prop)
        
        return properties
    
    def create_mapped_property(self, reso_property: Dict[str, Any]) -> Dict[str, Any]:
        """Create mapped property data from RESO property data."""
        return {
            "listing_id": reso_property.get("ListingId"),
            "status": reso_property.get("StandardStatus", "").lower().replace(" ", "_"),
            "list_price": reso_property.get("ListPrice"),
            "original_list_price": reso_property.get("OriginalListPrice"),
            "sold_price": reso_property.get("ClosePrice"),
            "bedrooms": reso_property.get("BedroomsTotal"),
            "bathrooms": float(reso_property.get("BathroomsTotalInteger", 0)),
            "full_bathrooms": reso_property.get("BathroomsFull"),
            "half_bathrooms": reso_property.get("BathroomsHalf"),
            "square_feet": reso_property.get("LivingArea"),
            "lot_size": reso_property.get("LotSizeAcres"),
            "year_built": reso_property.get("YearBuilt"),
            "property_type": reso_property.get("PropertySubType", "").lower().replace(" ", "_"),
            "city": reso_property.get("City"),
            "state": reso_property.get("StateOrProvince"),
            "zip_code": reso_property.get("PostalCode"),
            "address": reso_property.get("UnparsedAddress"),
            "garage_spaces": reso_property.get("GarageSpaces"),
            "pool": reso_property.get("PoolFeatures") not in ["None", None],
            "waterfront": reso_property.get("WaterfrontFeatures") not in ["None", None],
            "view": reso_property.get("View"),
            "listing_agent_name": f"{reso_property.get('ListAgentFirstName', '')} {reso_property.get('ListAgentLastName', '')}".strip(),
            "listing_office": reso_property.get("ListOfficeName"),
            "remarks": reso_property.get("PublicRemarks"),
            "days_on_market": reso_property.get("DaysOnMarket"),
            "listing_date": reso_property.get("OnMarketDate"),
            "sold_date": reso_property.get("CloseDate")
        }
    
    def get_property_summary(self, mapped_property: Dict[str, Any]) -> str:
        """Generate property summary string."""
        bedrooms = mapped_property.get("bedrooms", 0)
        bathrooms = mapped_property.get("bathrooms", 0)
        sqft = mapped_property.get("square_feet", 0)
        prop_type = mapped_property.get("property_type", "").replace("_", " ").title()
        city = mapped_property.get("city", "")
        state = mapped_property.get("state", "")
        price = mapped_property.get("list_price", 0)
        
        return f"{bedrooms}BR/{bathrooms}BA | {sqft:,} sqft | {prop_type} | {city} {state} | ${price:,}"