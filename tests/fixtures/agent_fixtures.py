"""Agent and member data fixtures for comprehensive testing."""

from typing import Dict, Any, List, Optional
import random
from datetime import datetime, timedelta


class AgentDataFixtures:
    """Comprehensive agent and member data fixtures for testing."""
    
    def __init__(self):
        self.first_names = [
            "John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Emily",
            "William", "Jessica", "James", "Ashley", "Christopher", "Amanda", "Daniel", "Jennifer",
            "Matthew", "Stephanie", "Anthony", "Melissa", "Mark", "Nicole", "Steven", "Kimberly",
            "Andrew", "Donna", "Kenneth", "Carol", "Paul", "Sandra", "Joshua", "Ruth"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
            "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
            "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young"
        ]
        
        self.office_names = [
            "Premier Realty", "Best Homes", "Elite Properties", "Top Agents", "Prime Real Estate",
            "Century 21", "Keller Williams", "RE/MAX", "Coldwell Banker", "Berkshire Hathaway",
            "Compass", "Realty One Group", "eXp Realty", "Better Homes and Gardens", "Sotheby's International",
            "Douglas Elliman", "Corcoran Group", "BHHS PenFed Realty", "Windermere Real Estate",
            "Howard Hanna", "Long & Foster", "John L. Scott", "Weichert Realtors"
        ]
        
        self.cities = [
            "Austin", "Dallas", "Houston", "San Antonio", "Fort Worth", 
            "El Paso", "Arlington", "Corpus Christi", "Plano", "Lubbock",
            "Garland", "Irving", "Laredo", "Frisco", "McKinney",
            "Grand Prairie", "Brownsville", "Pasadena", "Mesquite", "McAllen"
        ]
        
        self.specializations = [
            "Luxury Homes", "First-Time Buyers", "Investment Properties", "New Construction",
            "Relocation Specialist", "Commercial Real Estate", "Farm and Ranch", "Waterfront Properties",
            "55+ Communities", "Condominiums", "Foreclosures", "Short Sales", "Vacation Homes",
            "Multi-Family Properties", "Land Development", "Property Management", "Leasing",
            "International Clients", "Military Relocation", "Equestrian Properties"
        ]
        
        self.designations = [
            "ABR", "ABRM", "AHWD", "ALHS", "ASP", "AT", "BPOR", "CCIM", "CRB", "CRS",
            "CIPS", "CRP", "CSDS", "e-PRO", "GRI", "MRP", "PSA", "RENE", "RSPS", "SFR",
            "SRES", "SRS", "CCDS", "CDPE", "CPRES", "GREEN", "NAR", "PMN", "RESE", "RCC"
        ]
        
        self.languages = [
            "English", "Spanish", "French", "German", "Chinese", "Japanese", "Portuguese",
            "Italian", "Russian", "Arabic", "Korean", "Hindi", "Vietnamese", "Tagalog"
        ]
    
    def create_basic_agent(self, member_key: str = None, **overrides) -> Dict[str, Any]:
        """Create a basic real estate agent with realistic data."""
        if not member_key:
            member_key = f"AGENT{random.randint(100000, 999999)}"
        
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        city = random.choice(self.cities)
        office = random.choice(self.office_names)
        
        # Generate realistic contact information
        area_codes = {"Austin": "512", "Dallas": "214", "Houston": "713", "San Antonio": "210"}
        area_code = area_codes.get(city, "512")
        
        agent_data = {
            "MemberKey": member_key,
            "MemberFirstName": first_name,
            "MemberLastName": last_name,
            "MemberFullName": f"{first_name} {last_name}",
            "MemberNickname": first_name,
            "MemberEmail": f"{first_name.lower()}.{last_name.lower()}@{office.lower().replace(' ', '').replace('&', '')}.com",
            "MemberDirectPhone": f"({area_code}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "MemberMobilePhone": f"({area_code}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "MemberOfficePhone": f"({area_code}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "MemberFax": f"({area_code}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "MemberOfficeName": office,
            "MemberOfficeKey": f"OFFICE{random.randint(1000, 9999)}",
            "MemberCity": city,
            "MemberStateOrProvince": "TX",
            "MemberPostalCode": f"7{random.randint(8000, 8999)}",
            "MemberAddress1": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Business', 'Commerce'])} St",
            "MemberStateLicense": f"TX{random.randint(100000, 999999)}",
            "MemberNationalAssociationId": f"NAR{random.randint(1000000, 9999999)}",
            "MemberType": random.choice(["REALTOR", "Appraiser", "Broker", "Sales Agent"]),
            "MemberStatus": random.choice(["Active", "Inactive", "Suspended"]),
            "MemberLanguages": random.choice(self.languages),
            "MemberSpecialty": random.choice(self.specializations),
            "MemberDesignation": random.choice(self.designations),
            "MemberPreferredPhone": random.choice(["Mobile", "Direct", "Office"]),
            "MemberLoginId": f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}",
            "MemberPassword": None,  # Never include actual passwords
            "ModificationTimestamp": datetime.now().isoformat(),
            "MemberMlsId": f"MLS{random.randint(100000, 999999)}"
        }
        
        # Apply any overrides
        agent_data.update(overrides)
        return agent_data
    
    def create_top_producer(self, member_key: str = None, **overrides) -> Dict[str, Any]:
        """Create a top-producing agent with premium credentials."""
        agent_data = self.create_basic_agent(member_key, **overrides)
        
        # Upgrade to top producer status
        top_producer_updates = {
            "MemberType": "REALTOR",
            "MemberStatus": "Active",
            "MemberDesignation": random.choice(["CRS", "GRI", "ABR", "CRB", "CIPS"]),
            "MemberSpecialty": random.choice(["Luxury Homes", "Investment Properties", "Commercial Real Estate"]),
            "MemberYearsOfExperience": random.randint(10, 30),
            "MemberVolumeSold": random.randint(50000000, 200000000),  # $50M - $200M
            "MemberTransactionsSold": random.randint(100, 500),
            "MemberAwards": random.choice([
                "Top Producer 2023", "Chairman's Circle", "President's Circle", 
                "Multi-Million Dollar Producer", "Platinum Producer"
            ]),
            "MemberWebsite": f"www.{agent_data['MemberFirstName'].lower()}{agent_data['MemberLastName'].lower()}.com",
            "MemberSocialMediaFacebook": f"facebook.com/{agent_data['MemberFirstName'].lower()}.{agent_data['MemberLastName'].lower()}",
            "MemberSocialMediaLinkedIn": f"linkedin.com/in/{agent_data['MemberFirstName'].lower()}-{agent_data['MemberLastName'].lower()}",
            "MemberBio": f"Top-producing {agent_data['MemberSpecialty']} specialist with {random.randint(10, 20)}+ years of experience in {agent_data['MemberCity']} real estate market."
        }
        
        agent_data.update(top_producer_updates)
        return agent_data
    
    def create_new_agent(self, member_key: str = None, **overrides) -> Dict[str, Any]:
        """Create a newly licensed agent."""
        agent_data = self.create_basic_agent(member_key, **overrides)
        
        # Adjust for new agent
        new_agent_updates = {
            "MemberYearsOfExperience": random.randint(0, 2),
            "MemberVolumeSold": random.randint(0, 5000000),  # $0 - $5M
            "MemberTransactionsSold": random.randint(0, 20),
            "MemberSpecialty": random.choice(["First-Time Buyers", "Residential Sales", "New Construction"]),
            "MemberDesignation": random.choice(["", "NAR", "e-PRO"]),  # Fewer designations
            "MemberBio": f"Dedicated new agent specializing in {agent_data['MemberSpecialty']}. Committed to providing exceptional service to clients in {agent_data['MemberCity']}.",
            "MemberMentorKey": f"MENTOR{random.randint(100000, 999999)}"
        }
        
        agent_data.update(new_agent_updates)
        return agent_data
    
    def create_broker(self, member_key: str = None, **overrides) -> Dict[str, Any]:
        """Create a broker with appropriate credentials."""
        agent_data = self.create_basic_agent(member_key, **overrides)
        
        # Upgrade to broker status
        broker_updates = {
            "MemberType": "Broker",
            "MemberStatus": "Active",
            "MemberYearsOfExperience": random.randint(15, 35),
            "MemberDesignation": random.choice(["CRB", "CRS", "CCIM", "GRI"]),
            "MemberSpecialty": random.choice(["Brokerage Management", "Commercial Real Estate", "Luxury Homes"]),
            "MemberVolumeSold": random.randint(100000000, 500000000),  # $100M - $500M
            "MemberTransactionsSold": random.randint(200, 1000),
            "MemberBrokerLicense": f"BROKER{random.randint(100000, 999999)}",
            "MemberOfficeManager": True,
            "MemberTeamLeader": True,
            "MemberBio": f"Experienced broker with {random.randint(15, 25)}+ years in real estate. Leading {agent_data['MemberOfficeName']} {agent_data['MemberCity']} office."
        }
        
        agent_data.update(broker_updates)
        return agent_data
    
    def create_team_member(self, team_leader_key: str, member_key: str = None, **overrides) -> Dict[str, Any]:
        """Create a team member associated with a team leader."""
        agent_data = self.create_basic_agent(member_key, **overrides)
        
        # Team member specific updates
        team_updates = {
            "MemberTeamLeaderKey": team_leader_key,
            "MemberTeamName": f"The {random.choice(['Elite', 'Premier', 'Top', 'Dynamic', 'Success'])} Team",
            "MemberType": "Sales Agent",
            "MemberSpecialty": random.choice([
                "Buyer Specialist", "Listing Specialist", "Transaction Coordinator", 
                "Marketing Coordinator", "Client Care Specialist"
            ]),
            "MemberYearsOfExperience": random.randint(2, 10),
            "MemberBio": f"Dedicated team member specializing in {agent_data['MemberSpecialty']}. Part of {agent_data['MemberTeamName']} serving {agent_data['MemberCity']} area."
        }
        
        agent_data.update(team_updates)
        return agent_data
    
    def create_commercial_agent(self, member_key: str = None, **overrides) -> Dict[str, Any]:
        """Create a commercial real estate specialist."""
        agent_data = self.create_basic_agent(member_key, **overrides)
        
        # Commercial specialist updates
        commercial_updates = {
            "MemberSpecialty": "Commercial Real Estate",
            "MemberDesignation": random.choice(["CCIM", "SIOR", "CRE", "MAI"]),
            "MemberType": random.choice(["REALTOR", "Broker"]),
            "MemberYearsOfExperience": random.randint(8, 25),
            "MemberVolumeSold": random.randint(25000000, 150000000),  # $25M - $150M
            "MemberTransactionsSold": random.randint(30, 200),
            "MemberCommercialPropertyTypes": random.choice([
                "Office, Retail", "Industrial, Warehouse", "Multi-Family", 
                "Hotel, Hospitality", "Land Development", "Investment Properties"
            ]),
            "MemberBio": f"Commercial real estate specialist with expertise in {agent_data['MemberCommercialPropertyTypes']}. Serving investors and businesses in {agent_data['MemberCity']} market."
        }
        
        agent_data.update(commercial_updates)
        return agent_data
    
    def create_agent_dataset(self, count: int, agent_types: List[str] = None) -> List[Dict[str, Any]]:
        """Create a dataset of diverse agents."""
        if agent_types is None:
            agent_types = ["basic", "top_producer", "new_agent", "broker", "commercial"]
        
        agents = []
        team_leaders = []  # Track team leaders for team member creation
        
        for i in range(count):
            agent_type = random.choice(agent_types)
            member_key = f"DATASET{i:06d}"
            
            if agent_type == "basic":
                agent = self.create_basic_agent(member_key)
            elif agent_type == "top_producer":
                agent = self.create_top_producer(member_key)
            elif agent_type == "new_agent":
                agent = self.create_new_agent(member_key)
            elif agent_type == "broker":
                agent = self.create_broker(member_key)
                team_leaders.append(member_key)  # Brokers can be team leaders
            elif agent_type == "commercial":
                agent = self.create_commercial_agent(member_key)
            elif agent_type == "team_member" and team_leaders:
                team_leader = random.choice(team_leaders)
                agent = self.create_team_member(team_leader, member_key)
            else:
                agent = self.create_basic_agent(member_key)
            
            agents.append(agent)
            
            # Randomly make some agents team leaders
            if agent_type in ["top_producer", "broker"] and random.random() < 0.3:
                team_leaders.append(member_key)
        
        return agents
    
    def create_office_data(self, office_key: str = None, **overrides) -> Dict[str, Any]:
        """Create office/brokerage data."""
        if not office_key:
            office_key = f"OFFICE{random.randint(1000, 9999)}"
        
        office_name = random.choice(self.office_names)
        city = random.choice(self.cities)
        area_codes = {"Austin": "512", "Dallas": "214", "Houston": "713", "San Antonio": "210"}
        area_code = area_codes.get(city, "512")
        
        office_data = {
            "OfficeKey": office_key,
            "OfficeName": office_name,
            "OfficePhone": f"({area_code}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "OfficeFax": f"({area_code}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "OfficeEmail": f"info@{office_name.lower().replace(' ', '').replace('&', '')}.com",
            "OfficeAddress1": f"{random.randint(100, 9999)} {random.choice(['Main', 'Business', 'Commerce', 'Professional'])} {random.choice(['St', 'Ave', 'Dr', 'Blvd'])}",
            "OfficeAddress2": random.choice(["", f"Suite {random.randint(100, 999)}", f"Floor {random.randint(1, 20)}"]),
            "OfficeCity": city,
            "OfficeStateOrProvince": "TX",
            "OfficePostalCode": f"7{random.randint(8000, 8999)}",
            "OfficeCountry": "US",
            "OfficeBrokerKey": f"BROKER{random.randint(100000, 999999)}",
            "OfficeManagerKey": f"MANAGER{random.randint(100000, 999999)}",
            "OfficeStatus": random.choice(["Active", "Inactive"]),
            "OfficeType": random.choice(["Main Office", "Branch Office", "Satellite Office"]),
            "OfficeWebsite": f"www.{office_name.lower().replace(' ', '').replace('&', '')}.com",
            "OfficeAffiliation": random.choice(["Independent", "Franchise", "Corporate"]),
            "OfficeAgentCount": random.randint(5, 150),
            "OfficeYearEstablished": random.randint(1970, 2020),
            "ModificationTimestamp": datetime.now().isoformat()
        }
        
        # Apply any overrides
        office_data.update(overrides)
        return office_data
    
    def get_agent_summary(self, agent_data: Dict[str, Any]) -> str:
        """Generate agent summary string."""
        name = f"{agent_data.get('MemberFirstName', '')} {agent_data.get('MemberLastName', '')}".strip()
        office = agent_data.get('MemberOfficeName', '')
        city = agent_data.get('MemberCity', '')
        state = agent_data.get('MemberStateOrProvince', '')
        specialty = agent_data.get('MemberSpecialty', '')
        phone = agent_data.get('MemberMobilePhone', agent_data.get('MemberDirectPhone', ''))
        
        return f"{name} | {office} | {city}, {state} | {specialty} | {phone}"