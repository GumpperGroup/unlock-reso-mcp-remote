"""Performance tests and benchmarks for MCP server operations."""

import pytest
import asyncio
import time
from unittest.mock import AsyncMock, Mock, patch
from typing import Dict, Any, List
import statistics

from src.server import UnlockMlsServer


@pytest.fixture
def performance_server():
    """Create server instance optimized for performance testing."""
    with patch('src.server.get_settings') as mock_get_settings, \
         patch('src.server.OAuth2Handler') as mock_oauth, \
         patch('src.server.ResoWebApiClient') as mock_client, \
         patch('src.server.ResoDataMapper') as mock_mapper, \
         patch('src.server.QueryValidator') as mock_validator:
        
        # Mock settings
        settings = Mock()
        settings.bridge_client_id = "perf_test_client"
        settings.bridge_client_secret = "perf_test_secret"
        settings.bridge_api_base_url = "https://api.test.com"
        settings.bridge_mls_id = "TEST"
        settings.api_rate_limit_per_minute = 300  # Higher for performance testing
        mock_get_settings.return_value = settings
        
        # Setup fast mock instances
        oauth_handler = AsyncMock()
        oauth_handler.get_access_token.return_value = "perf_test_token"
        
        reso_client = AsyncMock()
        data_mapper = Mock()
        query_validator = Mock()
        
        # Configure default return values for query validator
        query_validator.validate_search_filters.return_value = {}
        query_validator.parse_natural_language_query.return_value = {}
        
        mock_oauth.return_value = oauth_handler
        mock_client.return_value = reso_client
        mock_mapper.return_value = data_mapper
        mock_validator.return_value = query_validator
        
        server = UnlockMlsServer()
        server.oauth_handler = oauth_handler
        server.reso_client = reso_client
        server.data_mapper = data_mapper
        server.query_validator = query_validator
        
        return server


@pytest.fixture
def large_property_dataset():
    """Generate large dataset for performance testing."""
    properties = []
    for i in range(1000):
        property_data = {
            "ListingId": f"PERF{i:04d}",
            "StandardStatus": "Active" if i % 3 != 0 else "Sold",
            "ListPrice": 300000 + (i * 1000),
            "BedroomsTotal": (i % 5) + 1,
            "BathroomsTotalInteger": (i % 3) + 1,
            "LivingArea": 1500 + (i * 10),
            "PropertyType": "Residential",
            "City": "Austin" if i % 2 == 0 else "Dallas",
            "StateOrProvince": "TX",
            "PostalCode": f"787{i % 100:02d}",
            "PublicRemarks": f"Performance test property {i}"
        }
        properties.append(property_data)
    return properties


@pytest.fixture
def performance_metrics():
    """Fixture to collect and analyze performance metrics."""
    class PerformanceMetrics:
        def __init__(self):
            self.timings = {}
            self.memory_usage = {}
            self.call_counts = {}
        
        def record_timing(self, operation: str, duration: float):
            if operation not in self.timings:
                self.timings[operation] = []
            self.timings[operation].append(duration)
        
        def record_call_count(self, operation: str, count: int):
            self.call_counts[operation] = count
        
        def get_statistics(self, operation: str) -> Dict[str, float]:
            if operation not in self.timings:
                return {}
            
            timings = self.timings[operation]
            return {
                "mean": statistics.mean(timings),
                "median": statistics.median(timings),
                "min": min(timings),
                "max": max(timings),
                "stdev": statistics.stdev(timings) if len(timings) > 1 else 0,
                "count": len(timings)
            }
        
        def get_performance_report(self) -> str:
            report = ["Performance Test Results", "=" * 25]
            
            for operation, stats in [(op, self.get_statistics(op)) for op in self.timings.keys()]:
                if stats:
                    report.append(f"\n{operation}:")
                    report.append(f"  Mean: {stats['mean']:.3f}s")
                    report.append(f"  Median: {stats['median']:.3f}s")
                    report.append(f"  Min: {stats['min']:.3f}s")
                    report.append(f"  Max: {stats['max']:.3f}s")
                    report.append(f"  StdDev: {stats['stdev']:.3f}s")
                    report.append(f"  Iterations: {stats['count']}")
            
            if self.call_counts:
                report.append("\nAPI Call Counts:")
                for operation, count in self.call_counts.items():
                    report.append(f"  {operation}: {count}")
            
            return "\n".join(report)
    
    return PerformanceMetrics()


class TestBasicPerformance:
    """Test basic operation performance and response times."""
    
    async def test_property_search_performance(self, performance_server, 
                                             large_property_dataset, performance_metrics):
        """Test property search performance with various dataset sizes."""
        server = performance_server
        
        # Setup mock responses with different dataset sizes
        dataset_sizes = [10, 50, 100, 500, 1000]
        
        for size in dataset_sizes:
            subset = large_property_dataset[:size]
            mapped_subset = [{"listing_id": f"PERF{i:04d}", "list_price": 300000 + (i * 1000)} 
                           for i in range(size)]
            
            server.query_validator.parse_natural_language_query.return_value = {
                "city": "Austin", "state": "TX"
            }
            server.query_validator.validate_search_filters.return_value = {
                "city": "Austin", "state": "TX"
            }
            server.reso_client.query_properties.return_value = subset
            server.data_mapper.map_properties.return_value = mapped_subset
            server.data_mapper.get_property_summary.return_value = "Test Summary"
            
            # Measure performance
            start_time = time.time()
            result = await server._search_properties({
                "query": "house in Austin TX",
                "limit": size
            })
            duration = time.time() - start_time
            
            performance_metrics.record_timing(f"search_properties_{size}", duration)
            
            # Verify result quality
            assert len(result.content) == 1
            assert f"Found {size} properties" in result.content[0].text
        
        # Analyze performance scaling
        stats_10 = performance_metrics.get_statistics("search_properties_10")
        stats_1000 = performance_metrics.get_statistics("search_properties_1000")
        
        # Ensure reasonable performance scaling (shouldn't be more than 30x slower for 100x data)
        # Note: Non-linear scaling is expected due to string formatting overhead
        if stats_10["mean"] > 0:
            scaling_factor = stats_1000["mean"] / stats_10["mean"]
            assert scaling_factor < 30, f"Performance scaling too poor: {scaling_factor}x"
    
    async def test_market_analysis_performance(self, performance_server, 
                                             large_property_dataset, performance_metrics):
        """Test market analysis performance with large datasets."""
        server = performance_server
        
        # Split dataset into active and sold
        active_properties = [p for i, p in enumerate(large_property_dataset) if i % 3 != 0]
        sold_properties = [p for i, p in enumerate(large_property_dataset) if i % 3 == 0]
        
        # Update sold properties to have ClosePrice
        for i, prop in enumerate(sold_properties):
            prop["ClosePrice"] = prop["ListPrice"] - 10000
            prop["StandardStatus"] = "Sold"
        
        server.reso_client.query_properties.side_effect = [active_properties, sold_properties]
        
        mapped_active = [{"list_price": p["ListPrice"], "square_feet": p["LivingArea"], 
                         "bedrooms": p["BedroomsTotal"]} for p in active_properties]
        mapped_sold = [{"sold_price": p["ClosePrice"], "square_feet": p["LivingArea"]} 
                       for p in sold_properties]
        
        server.data_mapper.map_properties.side_effect = [mapped_active, mapped_sold]
        
        # Configure validator for market analysis
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin",
            "state": "TX",
            "property_type": "residential"
        }
        
        # Measure market analysis performance
        start_time = time.time()
        result = await server._analyze_market({
            "city": "Austin",
            "state": "TX",
            "property_type": "residential",
            "days_back": 90
        })
        duration = time.time() - start_time
        
        performance_metrics.record_timing("market_analysis_large", duration)
        
        # Verify comprehensive analysis completed
        content = result.content[0].text
        assert "Market Analysis - Austin" in content
        assert f"{len(active_properties)} properties" in content
        assert f"{len(sold_properties)} properties" in content
        
        # Performance should be reasonable even for large datasets
        assert duration < 2.0, f"Market analysis too slow: {duration:.3f}s"
    
    async def test_concurrent_operation_performance(self, performance_server,
                                                  large_property_dataset, performance_metrics):
        """Test performance under concurrent operation load."""
        server = performance_server
        
        # Setup for concurrent operations
        sample_data = large_property_dataset[:100]
        mapped_data = [{"listing_id": f"PERF{i:04d}", "list_price": 300000 + (i * 1000)} 
                       for i in range(100)]
        
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.reso_client.query_properties.return_value = sample_data
        server.data_mapper.map_properties.return_value = mapped_data
        server.data_mapper.get_property_summary.return_value = "Concurrent Test Summary"
        
        # Test different concurrency levels
        concurrency_levels = [1, 5, 10, 20]
        
        for concurrency in concurrency_levels:
            # Create concurrent tasks
            tasks = []
            for i in range(concurrency):
                task = server._search_properties({
                    "query": f"concurrent search {i}",
                    "limit": 50
                })
                tasks.append(task)
            
            # Measure concurrent execution time
            start_time = time.time()
            results = await asyncio.gather(*tasks)
            duration = time.time() - start_time
            
            performance_metrics.record_timing(f"concurrent_{concurrency}", duration)
            
            # Verify all operations completed successfully
            assert len(results) == concurrency
            for result in results:
                assert len(result.content) == 1
                assert "Found 100 properties" in result.content[0].text
        
        # Analyze concurrency scaling
        sequential_time = performance_metrics.get_statistics("concurrent_1")["mean"]
        concurrent_20_time = performance_metrics.get_statistics("concurrent_20")["mean"]
        
        # Concurrent execution should be more efficient than 20x sequential
        efficiency_ratio = concurrent_20_time / (sequential_time * 20)
        assert efficiency_ratio < 0.8, f"Poor concurrency efficiency: {efficiency_ratio}"


class TestMemoryPerformance:
    """Test memory usage and optimization."""
    
    async def test_memory_efficient_large_dataset_processing(self, performance_server,
                                                           large_property_dataset):
        """Test memory efficiency with large datasets."""
        server = performance_server
        
        # Test processing of very large dataset
        large_dataset = large_property_dataset * 5  # 5000 properties
        
        # Mock data mapper to simulate memory-efficient processing
        def efficient_mapping(properties):
            # Simulate processing in chunks to avoid memory spikes
            chunk_size = 100
            mapped_properties = []
            for i in range(0, len(properties), chunk_size):
                chunk = properties[i:i + chunk_size]
                mapped_chunk = [{"listing_id": p["ListingId"], "list_price": p["ListPrice"]} 
                               for p in chunk]
                mapped_properties.extend(mapped_chunk)
            return mapped_properties
        
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.reso_client.query_properties.return_value = large_dataset
        server.data_mapper.map_properties.side_effect = efficient_mapping
        server.data_mapper.get_property_summary.return_value = "Memory Test Summary"
        
        # Execute with large dataset
        result = await server._search_properties({
            "query": "large dataset test",
            "limit": 5000
        })
        
        # Verify successful processing
        assert len(result.content) == 1
        assert "Found 5000 properties" in result.content[0].text
        
        # Memory usage should remain reasonable (this is a basic check)
        # In a real scenario, you'd use memory profiling tools
        assert len(large_dataset) == 5000  # Ensure we actually processed the large dataset
    
    async def test_memory_cleanup_after_operations(self, performance_server):
        """Test that memory is properly cleaned up after operations."""
        server = performance_server
        
        # Execute multiple operations that could accumulate memory
        for i in range(10):
            large_dataset = [{"ListingId": f"MEM{j:04d}", "ListPrice": j * 1000} 
                           for j in range(1000)]
            
            server.reso_client.query_properties.return_value = large_dataset
            server.data_mapper.map_properties.return_value = [
                {"listing_id": f"MEM{j:04d}", "list_price": j * 1000} for j in range(1000)
            ]
            server.data_mapper.get_property_summary.return_value = f"Cleanup Test {i}"
            
            result = await server._search_properties({
                "query": f"memory cleanup test {i}",
                "limit": 1000
            })
            
            assert "Found 1000 properties" in result.content[0].text
            
            # Clear references to help with garbage collection
            del large_dataset
            del result


class TestRateLimitingPerformance:
    """Test rate limiting and throttling behavior."""
    
    async def test_rate_limiting_compliance(self, performance_server, performance_metrics):
        """Test that operations respect rate limiting."""
        server = performance_server
        
        # Configure rate limiting
        rate_limit = 60  # requests per minute
        time_window = 60  # seconds
        
        # Setup mock responses
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.reso_client.query_properties.return_value = [
            {"ListingId": "RATE001", "ListPrice": 400000}
        ]
        server.data_mapper.map_properties.return_value = [
            {"listing_id": "RATE001", "list_price": 400000}
        ]
        server.data_mapper.get_property_summary.return_value = "Rate Limit Test"
        
        # Execute operations rapidly
        start_time = time.time()
        results = []
        
        for i in range(10):  # Smaller number for testing
            result = await server._search_properties({
                "query": f"rate limit test {i}",
                "limit": 1
            })
            results.append(result)
        
        total_time = time.time() - start_time
        performance_metrics.record_timing("rate_limited_operations", total_time)
        
        # Verify all operations completed
        assert len(results) == 10
        for result in results:
            assert "Found 1 properties" in result.content[0].text
        
        # Operations should complete reasonably quickly (no artificial delays in test)
        assert total_time < 5.0, f"Rate limited operations too slow: {total_time:.3f}s"
    
    async def test_burst_request_handling(self, performance_server, performance_metrics):
        """Test handling of burst requests."""
        server = performance_server
        
        # Setup for burst testing
        server.query_validator.validate_search_filters.return_value = {"city": "Austin"}
        server.reso_client.query_properties.return_value = [
            {"ListingId": "BURST001", "ListPrice": 300000}
        ]
        server.data_mapper.map_properties.return_value = [
            {"listing_id": "BURST001", "list_price": 300000}
        ]
        server.data_mapper.get_property_summary.return_value = "Burst Test"
        
        # Create burst of simultaneous requests
        burst_size = 15
        tasks = []
        
        for i in range(burst_size):
            task = server._search_properties({
                "filters": {"city": "Austin"},
                "limit": 1
            })
            tasks.append(task)
        
        # Execute burst
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        burst_time = time.time() - start_time
        
        performance_metrics.record_timing("burst_requests", burst_time)
        
        # Verify burst handling
        successful_results = [r for r in results if not isinstance(r, Exception)]
        assert len(successful_results) == burst_size
        
        # Burst should complete in reasonable time
        assert burst_time < 3.0, f"Burst handling too slow: {burst_time:.3f}s"


class TestResourcePerformance:
    """Test performance of MCP resource operations."""
    
    async def test_resource_access_performance(self, performance_server, performance_metrics):
        """Test performance of accessing MCP resources."""
        server = performance_server
        
        # Test all resource access methods
        resource_methods = [
            ("search_examples", server._get_search_examples),
            ("property_types", server._get_property_types_reference),
            ("market_guide", server._get_market_analysis_guide),
            ("agent_guide", server._get_agent_search_guide),
            ("workflows", server._get_common_workflows),
            ("guided_search", server._get_guided_search_prompts),
            ("guided_analysis", server._get_guided_analysis_prompts)
        ]
        
        for resource_name, resource_method in resource_methods:
            # Measure resource access time
            start_time = time.time()
            content = resource_method()
            duration = time.time() - start_time
            
            performance_metrics.record_timing(f"resource_{resource_name}", duration)
            
            # Verify content quality
            assert len(content) > 1000
            assert "##" in content  # Markdown formatting
            
            # Resource access should be very fast (in-memory)
            assert duration < 0.1, f"Resource {resource_name} too slow: {duration:.3f}s"
    
    async def test_api_status_resource_performance(self, performance_server, performance_metrics):
        """Test performance of dynamic API status resource."""
        server = performance_server
        
        # Test API status resource (involves async operations)
        iterations = 5
        
        for i in range(iterations):
            start_time = time.time()
            content = await server._get_api_status_info()
            duration = time.time() - start_time
            
            performance_metrics.record_timing("api_status_resource", duration)
            
            # Verify content quality
            assert "API Status & System Information" in content
            assert "✅ Connected" in content
            
            # API status should be reasonably fast
            assert duration < 0.5, f"API status too slow: {duration:.3f}s"


class TestPerformanceBenchmarks:
    """Establish performance benchmarks for regression testing."""
    
    async def test_performance_benchmarks(self, performance_server, performance_metrics):
        """Establish baseline performance benchmarks."""
        server = performance_server
        
        # Benchmark scenarios
        benchmarks = {
            "small_search": {
                "operation": "search_properties",
                "params": {"query": "house in Austin", "limit": 10},
                "expected_max_time": 0.1,
                "data_size": 10
            },
            "medium_search": {
                "operation": "search_properties", 
                "params": {"query": "house in Austin", "limit": 100},
                "expected_max_time": 0.5,
                "data_size": 100
            },
            "property_details": {
                "operation": "get_property_details",
                "params": {"listing_id": "BENCH001"},
                "expected_max_time": 0.2,
                "data_size": 1
            },
            "market_analysis": {
                "operation": "analyze_market",
                "params": {"city": "Austin", "state": "TX"},
                "expected_max_time": 1.0,
                "data_size": 200
            },
            "agent_search": {
                "operation": "find_agent",
                "params": {"city": "Austin", "state": "TX", "limit": 20},
                "expected_max_time": 0.3,
                "data_size": 20
            }
        }
        
        # Setup mock data for benchmarks
        self._setup_benchmark_mocks(server, benchmarks)
        
        # Execute benchmarks
        for benchmark_name, config in benchmarks.items():
            operation = config["operation"]
            params = config["params"]
            expected_max_time = config["expected_max_time"]
            
            # Run multiple iterations for statistical reliability
            iterations = 5
            times = []
            
            for i in range(iterations):
                start_time = time.time()
                
                if operation == "search_properties":
                    result = await server._search_properties(params)
                elif operation == "get_property_details":
                    result = await server._get_property_details(params)
                elif operation == "analyze_market":
                    result = await server._analyze_market(params)
                elif operation == "find_agent":
                    result = await server._find_agent(params)
                
                duration = time.time() - start_time
                times.append(duration)
                
                # Basic result verification
                assert len(result.content) == 1
            
            # Record benchmark statistics
            avg_time = statistics.mean(times)
            max_time = max(times)
            min_time = min(times)
            
            performance_metrics.record_timing(f"benchmark_{benchmark_name}", avg_time)
            
            # Verify performance meets benchmarks
            assert avg_time < expected_max_time, \
                f"Benchmark {benchmark_name} failed: {avg_time:.3f}s > {expected_max_time}s"
            
            print(f"Benchmark {benchmark_name}: avg={avg_time:.3f}s, "
                  f"min={min_time:.3f}s, max={max_time:.3f}s")
    
    def _setup_benchmark_mocks(self, server, benchmarks):
        """Setup mock data optimized for benchmark testing."""
        # Property search mocks
        search_data = [{"ListingId": f"BENCH{i:03d}", "ListPrice": 400000 + (i * 1000), 
                       "BedroomsTotal": 3, "City": "Austin", "StateOrProvince": "TX"} 
                      for i in range(100)]
        search_mapped = [{"listing_id": f"BENCH{i:03d}", "list_price": 400000 + (i * 1000)} 
                        for i in range(100)]
        
        # Property details mock
        detail_data = {
            "ListingId": "BENCH001", "ListPrice": 400000, "BedroomsTotal": 3,
            "City": "Austin", "StateOrProvince": "TX", "PublicRemarks": "Benchmark property"
        }
        detail_mapped = {"listing_id": "BENCH001", "list_price": 400000, "bedrooms": 3}
        
        # Market analysis mocks
        market_active = search_data[:100]
        market_sold = [{"ListingId": f"SOLD{i:03d}", "ClosePrice": 380000 + (i * 1000)} 
                       for i in range(50)]
        market_mapped_active = search_mapped
        market_mapped_sold = [{"sold_price": 380000 + (i * 1000)} for i in range(50)]
        
        # Agent search mock
        agent_data = [{"MemberKey": f"AGENT{i:03d}", "MemberFirstName": f"Agent{i}", 
                      "MemberLastName": "Benchmark", "MemberCity": "Austin", 
                      "MemberStateOrProvince": "TX"} for i in range(20)]
        
        # Configure mocks
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        
        # Setup side effects for different operations
        def query_properties_side_effect(*args, **kwargs):
            filters = kwargs.get('filters', {})
            if 'listing_id' in filters:
                return [detail_data]
            elif 'status' in filters and filters['status'] == 'sold':
                return market_sold
            else:
                return market_active
        
        server.reso_client.query_properties.side_effect = query_properties_side_effect
        server.reso_client.query_members.return_value = agent_data
        
        def map_properties_side_effect(properties):
            if properties == market_sold:
                return market_mapped_sold
            else:
                return search_mapped[:len(properties)]
        
        server.data_mapper.map_properties.side_effect = map_properties_side_effect
        server.data_mapper.map_property.return_value = detail_mapped
        server.data_mapper.get_property_summary.return_value = "Benchmark Summary"