"""Market analysis data fixtures for comprehensive testing."""

from typing import Dict, Any, List, Optional, Tuple
import random
from datetime import datetime, timedelta
import statistics


class MarketDataFixtures:
    """Comprehensive market analysis data fixtures for testing."""
    
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
        
        # Market characteristics by city
        self.market_profiles = {
            "Austin": {
                "avg_price": 550000,
                "price_range": (350000, 900000),
                "growth_rate": 0.08,  # 8% annual
                "inventory_days": 45,
                "market_temp": "hot"
            },
            "Dallas": {
                "avg_price": 450000,
                "price_range": (280000, 750000),
                "growth_rate": 0.06,  # 6% annual
                "inventory_days": 60,
                "market_temp": "balanced"
            },
            "Houston": {
                "avg_price": 400000,
                "price_range": (250000, 650000),
                "growth_rate": 0.04,  # 4% annual
                "inventory_days": 75,
                "market_temp": "buyer"
            },
            "San Antonio": {
                "avg_price": 350000,
                "price_range": (220000, 550000),
                "growth_rate": 0.05,  # 5% annual
                "inventory_days": 65,
                "market_temp": "balanced"
            }
        }
        
        self.property_types = ["single_family", "condo", "townhouse", "multi_family"]
        self.bedroom_distribution = [1, 2, 3, 4, 5, 6]
        self.bedroom_weights = [5, 15, 35, 30, 12, 3]  # Percentages
    
    def create_market_snapshot(self, city: str, property_type: str = "residential", 
                             days_back: int = 90) -> Dict[str, Any]:
        """Create a comprehensive market snapshot for a location."""
        profile = self.market_profiles.get(city, self.market_profiles["Austin"])
        
        # Generate active listings
        active_count = random.randint(50, 300)
        active_properties = self._generate_active_listings(city, active_count, profile)
        
        # Generate sold properties
        sold_count = random.randint(30, 200)
        sold_properties = self._generate_sold_listings(city, sold_count, profile, days_back)
        
        # Generate pending properties
        pending_count = random.randint(10, 50)
        pending_properties = self._generate_pending_listings(city, pending_count, profile)
        
        # Calculate market statistics
        market_stats = self._calculate_market_statistics(
            active_properties, sold_properties, pending_properties, profile
        )
        
        return {
            "location": city,
            "property_type": property_type,
            "analysis_period_days": days_back,
            "snapshot_date": datetime.now().isoformat(),
            "active_listings": active_properties,
            "sold_properties": sold_properties,
            "pending_properties": pending_properties,
            "market_statistics": market_stats
        }
    
    def create_zip_code_analysis(self, zip_code: str, property_type: str = "residential",
                                days_back: int = 90) -> Dict[str, Any]:
        """Create market analysis for a specific ZIP code."""
        # Determine city from ZIP code
        city = "Austin"  # Default
        for c, zips in self.zip_codes.items():
            if zip_code in zips:
                city = c
                break
        
        profile = self.market_profiles.get(city, self.market_profiles["Austin"])
        
        # ZIP code specific adjustments
        zip_multiplier = random.uniform(0.8, 1.3)  # ZIP codes vary from city average
        adjusted_profile = {
            "avg_price": int(profile["avg_price"] * zip_multiplier),
            "price_range": (int(profile["price_range"][0] * zip_multiplier), 
                          int(profile["price_range"][1] * zip_multiplier)),
            "growth_rate": profile["growth_rate"] * random.uniform(0.7, 1.4),
            "inventory_days": int(profile["inventory_days"] * random.uniform(0.8, 1.2)),
            "market_temp": profile["market_temp"]
        }
        
        # Generate smaller dataset for ZIP code
        active_count = random.randint(10, 50)
        sold_count = random.randint(5, 30)
        pending_count = random.randint(2, 15)
        
        active_properties = self._generate_active_listings(city, active_count, adjusted_profile)
        sold_properties = self._generate_sold_listings(city, sold_count, adjusted_profile, days_back)
        pending_properties = self._generate_pending_listings(city, pending_count, adjusted_profile)
        
        # Update ZIP codes
        for prop in active_properties + sold_properties + pending_properties:
            prop["PostalCode"] = zip_code
        
        market_stats = self._calculate_market_statistics(
            active_properties, sold_properties, pending_properties, adjusted_profile
        )
        
        return {
            "location": zip_code,
            "city": city,
            "property_type": property_type,
            "analysis_period_days": days_back,
            "snapshot_date": datetime.now().isoformat(),
            "active_listings": active_properties,
            "sold_properties": sold_properties,
            "pending_properties": pending_properties,
            "market_statistics": market_stats
        }
    
    def create_comparative_market_analysis(self, locations: List[str]) -> Dict[str, Any]:
        """Create comparative analysis across multiple locations."""
        location_analyses = {}
        
        for location in locations:
            if len(location) == 5 and location.isdigit():
                # ZIP code
                analysis = self.create_zip_code_analysis(location)
            else:
                # City
                analysis = self.create_market_snapshot(location)
            
            location_analyses[location] = analysis
        
        # Create comparison metrics
        comparison = self._create_market_comparison(location_analyses)
        
        return {
            "analysis_type": "comparative_market_analysis",
            "locations": locations,
            "analysis_date": datetime.now().isoformat(),
            "individual_analyses": location_analyses,
            "comparison_metrics": comparison
        }
    
    def create_seasonal_trends(self, city: str, months: int = 12) -> Dict[str, Any]:
        """Create seasonal market trend data."""
        profile = self.market_profiles.get(city, self.market_profiles["Austin"])
        monthly_data = []
        
        base_date = datetime.now() - timedelta(days=months * 30)
        
        for month in range(months):
            month_date = base_date + timedelta(days=month * 30)
            
            # Seasonal adjustments
            month_num = month_date.month
            seasonal_multiplier = self._get_seasonal_multiplier(month_num)
            
            # Generate monthly statistics
            monthly_stats = {
                "month": month_date.strftime("%Y-%m"),
                "avg_price": int(profile["avg_price"] * seasonal_multiplier * random.uniform(0.95, 1.05)),
                "median_price": int(profile["avg_price"] * 0.92 * seasonal_multiplier * random.uniform(0.95, 1.05)),
                "inventory_days": int(profile["inventory_days"] * seasonal_multiplier * random.uniform(0.8, 1.2)),
                "homes_sold": random.randint(80, 200),
                "new_listings": random.randint(90, 220),
                "price_per_sqft": random.randint(180, 280),
                "absorption_rate": round(random.uniform(1.2, 4.5), 1)
            }
            
            monthly_data.append(monthly_stats)
        
        return {
            "location": city,
            "trend_period_months": months,
            "analysis_date": datetime.now().isoformat(),
            "monthly_trends": monthly_data,
            "trend_summary": self._calculate_trend_summary(monthly_data)
        }
    
    def create_price_trend_analysis(self, city: str, property_type: str = "residential") -> Dict[str, Any]:
        """Create detailed price trend analysis."""
        profile = self.market_profiles.get(city, self.market_profiles["Austin"])
        
        # Generate historical price points
        price_history = []
        base_date = datetime.now() - timedelta(days=365)
        
        for week in range(52):  # Weekly data for past year
            date = base_date + timedelta(weeks=week)
            
            # Apply growth trend with some volatility
            growth_factor = (1 + profile["growth_rate"]) ** (week / 52)
            volatility = random.uniform(0.98, 1.02)
            
            weekly_price = int(profile["avg_price"] * growth_factor * volatility)
            
            price_history.append({
                "date": date.isoformat(),
                "avg_price": weekly_price,
                "median_price": int(weekly_price * 0.92),
                "price_per_sqft": random.randint(160, 300)
            })
        
        # Calculate trend metrics
        trend_metrics = self._calculate_price_trends(price_history, profile)
        
        return {
            "location": city,
            "property_type": property_type,
            "analysis_date": datetime.now().isoformat(),
            "price_history": price_history,
            "trend_metrics": trend_metrics
        }
    
    def _generate_active_listings(self, city: str, count: int, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate active listing data."""
        properties = []
        
        for i in range(count):
            bedrooms = random.choices(self.bedroom_distribution, weights=self.bedroom_weights)[0]
            bathrooms = random.randint(1, min(bedrooms + 1, 4))
            
            # Price based on profile with some variation
            base_price = profile["avg_price"]
            bedroom_adjustment = (bedrooms - 3) * 50000  # Adjust for bedroom count
            price_variation = random.uniform(0.8, 1.3)
            list_price = int((base_price + bedroom_adjustment) * price_variation)
            
            # Keep within reasonable range
            list_price = max(profile["price_range"][0], 
                           min(list_price, profile["price_range"][1]))
            
            living_area = random.randint(1200, 4000)
            
            property_data = {
                "ListingId": f"ACTIVE{i:06d}",
                "StandardStatus": "Active",
                "ListPrice": list_price,
                "BedroomsTotal": bedrooms,
                "BathroomsTotalInteger": bathrooms,
                "LivingArea": living_area,
                "PropertyType": "Residential",
                "City": city,
                "StateOrProvince": "TX",
                "PostalCode": random.choice(self.zip_codes.get(city, ["78701"])),
                "DaysOnMarket": random.randint(1, 180),
                "OnMarketDate": (datetime.now() - timedelta(days=random.randint(1, 180))).isoformat(),
                "PricePerSquareFoot": round(list_price / living_area, 2)
            }
            
            properties.append(property_data)
        
        return properties
    
    def _generate_sold_listings(self, city: str, count: int, profile: Dict[str, Any], 
                               days_back: int) -> List[Dict[str, Any]]:
        """Generate sold property data."""
        properties = []
        
        for i in range(count):
            bedrooms = random.choices(self.bedroom_distribution, weights=self.bedroom_weights)[0]
            bathrooms = random.randint(1, min(bedrooms + 1, 4))
            
            # Sold prices typically slightly below list prices
            base_price = profile["avg_price"]
            bedroom_adjustment = (bedrooms - 3) * 50000
            price_variation = random.uniform(0.75, 1.25)
            sold_price = int((base_price + bedroom_adjustment) * price_variation)
            
            # Keep within reasonable range
            sold_price = max(profile["price_range"][0] * 0.8, 
                           min(sold_price, profile["price_range"][1] * 1.1))
            
            living_area = random.randint(1200, 4000)
            days_on_market = random.randint(1, min(days_back, 180))
            close_date = datetime.now() - timedelta(days=random.randint(1, days_back))
            
            property_data = {
                "ListingId": f"SOLD{i:06d}",
                "StandardStatus": "Sold",
                "ClosePrice": sold_price,
                "BedroomsTotal": bedrooms,
                "BathroomsTotalInteger": bathrooms,
                "LivingArea": living_area,
                "PropertyType": "Residential",
                "City": city,
                "StateOrProvince": "TX",
                "PostalCode": random.choice(self.zip_codes.get(city, ["78701"])),
                "DaysOnMarket": days_on_market,
                "CloseDate": close_date.isoformat(),
                "PricePerSquareFoot": round(sold_price / living_area, 2)
            }
            
            properties.append(property_data)
        
        return properties
    
    def _generate_pending_listings(self, city: str, count: int, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate pending property data."""
        properties = []
        
        for i in range(count):
            bedrooms = random.choices(self.bedroom_distribution, weights=self.bedroom_weights)[0]
            bathrooms = random.randint(1, min(bedrooms + 1, 4))
            
            base_price = profile["avg_price"]
            bedroom_adjustment = (bedrooms - 3) * 50000
            price_variation = random.uniform(0.85, 1.2)
            list_price = int((base_price + bedroom_adjustment) * price_variation)
            
            living_area = random.randint(1200, 4000)
            
            property_data = {
                "ListingId": f"PENDING{i:06d}",
                "StandardStatus": "Pending",
                "ListPrice": list_price,
                "BedroomsTotal": bedrooms,
                "BathroomsTotalInteger": bathrooms,
                "LivingArea": living_area,
                "PropertyType": "Residential",
                "City": city,
                "StateOrProvince": "TX",
                "PostalCode": random.choice(self.zip_codes.get(city, ["78701"])),
                "DaysOnMarket": random.randint(1, 90),
                "ContractDate": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                "PricePerSquareFoot": round(list_price / living_area, 2)
            }
            
            properties.append(property_data)
        
        return properties
    
    def _calculate_market_statistics(self, active: List[Dict], sold: List[Dict], 
                                   pending: List[Dict], profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive market statistics."""
        
        # Active listing statistics
        active_prices = [p["ListPrice"] for p in active]
        active_stats = {
            "count": len(active),
            "avg_price": int(statistics.mean(active_prices)) if active_prices else 0,
            "median_price": int(statistics.median(active_prices)) if active_prices else 0,
            "min_price": min(active_prices) if active_prices else 0,
            "max_price": max(active_prices) if active_prices else 0,
            "avg_days_on_market": int(statistics.mean([p["DaysOnMarket"] for p in active])) if active else 0
        }
        
        # Sold property statistics
        sold_prices = [p["ClosePrice"] for p in sold]
        sold_stats = {
            "count": len(sold),
            "avg_price": int(statistics.mean(sold_prices)) if sold_prices else 0,
            "median_price": int(statistics.median(sold_prices)) if sold_prices else 0,
            "min_price": min(sold_prices) if sold_prices else 0,
            "max_price": max(sold_prices) if sold_prices else 0,
            "avg_days_on_market": int(statistics.mean([p["DaysOnMarket"] for p in sold])) if sold else 0
        }
        
        # Pending statistics
        pending_prices = [p["ListPrice"] for p in pending]
        pending_stats = {
            "count": len(pending),
            "avg_price": int(statistics.mean(pending_prices)) if pending_prices else 0
        }
        
        # Bedroom distribution
        all_properties = active + sold + pending
        bedroom_dist = {}
        for bedrooms in self.bedroom_distribution:
            count = len([p for p in all_properties if p["BedroomsTotal"] == bedrooms])
            if count > 0:
                bedroom_dist[f"{bedrooms}_br"] = count
        
        # Price trends
        price_trend = "stable"
        if active_stats["avg_price"] > 0 and sold_stats["avg_price"] > 0:
            price_diff_pct = (active_stats["avg_price"] - sold_stats["avg_price"]) / sold_stats["avg_price"]
            if price_diff_pct > 0.05:
                price_trend = "rising"
            elif price_diff_pct < -0.05:
                price_trend = "declining"
        
        # Market tempo
        market_tempo = profile["market_temp"]
        if active_stats["avg_days_on_market"] < 30:
            market_tempo = "hot"
        elif active_stats["avg_days_on_market"] > 90:
            market_tempo = "slow"
        
        return {
            "active_listings": active_stats,
            "sold_properties": sold_stats,
            "pending_properties": pending_stats,
            "bedroom_distribution": bedroom_dist,
            "price_trend": price_trend,
            "market_tempo": market_tempo,
            "absorption_rate": round(len(sold) / max(len(active), 1), 2),
            "supply_demand_ratio": round(len(active) / max(len(sold), 1), 2)
        }
    
    def _create_market_comparison(self, analyses: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Create comparison metrics across locations."""
        comparison = {
            "price_comparison": {},
            "market_tempo_comparison": {},
            "inventory_comparison": {},
            "highest_prices": [],
            "lowest_prices": [],
            "hottest_markets": [],
            "slowest_markets": []
        }
        
        # Extract comparison data
        location_data = []
        for location, analysis in analyses.items():
            stats = analysis["market_statistics"]
            location_data.append({
                "location": location,
                "avg_price": stats["active_listings"]["avg_price"],
                "market_tempo": stats["market_tempo"],
                "days_on_market": stats["active_listings"]["avg_days_on_market"],
                "active_count": stats["active_listings"]["count"]
            })
        
        # Sort and rank
        by_price = sorted(location_data, key=lambda x: x["avg_price"], reverse=True)
        by_speed = sorted(location_data, key=lambda x: x["days_on_market"])
        
        comparison["highest_prices"] = [{"location": x["location"], "avg_price": x["avg_price"]} for x in by_price[:3]]
        comparison["lowest_prices"] = [{"location": x["location"], "avg_price": x["avg_price"]} for x in by_price[-3:]]
        comparison["hottest_markets"] = [{"location": x["location"], "days_on_market": x["days_on_market"]} for x in by_speed[:3]]
        comparison["slowest_markets"] = [{"location": x["location"], "days_on_market": x["days_on_market"]} for x in by_speed[-3:]]
        
        return comparison
    
    def _get_seasonal_multiplier(self, month: int) -> float:
        """Get seasonal adjustment multiplier for given month."""
        # Real estate seasonal patterns
        seasonal_factors = {
            1: 0.85,   # January - slow
            2: 0.90,   # February
            3: 1.00,   # March - spring market starts
            4: 1.10,   # April
            5: 1.15,   # May - peak spring
            6: 1.12,   # June
            7: 1.05,   # July - summer
            8: 1.00,   # August
            9: 1.08,   # September - fall market
            10: 1.05,  # October
            11: 0.95,  # November - slowing
            12: 0.80   # December - holiday slow
        }
        return seasonal_factors.get(month, 1.0)
    
    def _calculate_trend_summary(self, monthly_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate trend summary from monthly data."""
        if len(monthly_data) < 2:
            return {"trend": "insufficient_data"}
        
        prices = [month["avg_price"] for month in monthly_data]
        first_half = prices[:len(prices)//2]
        second_half = prices[len(prices)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        price_change_pct = (second_avg - first_avg) / first_avg * 100
        
        trend_direction = "stable"
        if price_change_pct > 5:
            trend_direction = "rising"
        elif price_change_pct < -5:
            trend_direction = "declining"
        
        return {
            "trend_direction": trend_direction,
            "price_change_percent": round(price_change_pct, 1),
            "avg_price_first_half": int(first_avg),
            "avg_price_second_half": int(second_avg),
            "volatility": round(statistics.stdev(prices) / statistics.mean(prices) * 100, 1)
        }
    
    def _calculate_price_trends(self, price_history: List[Dict[str, Any]], 
                               profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed price trend metrics."""
        prices = [point["avg_price"] for point in price_history]
        
        # Calculate trend metrics
        first_price = prices[0]
        last_price = prices[-1]
        annual_growth = (last_price - first_price) / first_price * 100
        
        # Volatility
        volatility = statistics.stdev(prices) / statistics.mean(prices) * 100
        
        # Trend consistency
        positive_months = sum(1 for i in range(1, len(prices)) if prices[i] > prices[i-1])
        trend_consistency = positive_months / (len(prices) - 1) * 100
        
        return {
            "annual_growth_percent": round(annual_growth, 1),
            "volatility_percent": round(volatility, 1),
            "trend_consistency_percent": round(trend_consistency, 1),
            "price_appreciation": last_price - first_price,
            "highest_price": max(prices),
            "lowest_price": min(prices),
            "current_vs_high_percent": round((last_price - max(prices)) / max(prices) * 100, 1)
        }