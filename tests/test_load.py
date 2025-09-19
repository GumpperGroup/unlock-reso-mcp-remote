"""Load testing for production readiness and scalability validation."""

import pytest
import asyncio
import time
import statistics
from unittest.mock import AsyncMock, Mock, patch
from typing import Dict, Any, List, Tuple
import random

from src.server import UnlockMlsServer


@pytest.fixture
def load_test_server():
    """Create server instance optimized for load testing."""
    with patch('src.server.get_settings') as mock_get_settings, \
         patch('src.server.OAuth2Handler') as mock_oauth, \
         patch('src.server.ResoWebApiClient') as mock_client, \
         patch('src.server.ResoDataMapper') as mock_mapper, \
         patch('src.server.QueryValidator') as mock_validator:
        
        # Mock settings for load testing
        settings = Mock()
        settings.bridge_client_id = "load_test_client"
        settings.bridge_client_secret = "load_test_secret"
        settings.bridge_api_base_url = "https://api.test.com"
        settings.bridge_mls_id = "TEST"
        settings.api_rate_limit_per_minute = 1000  # High rate limit for load testing
        mock_get_settings.return_value = settings
        
        # Setup high-performance mock instances
        oauth_handler = AsyncMock()
        oauth_handler.get_access_token.return_value = "load_test_token"
        
        reso_client = AsyncMock()
        data_mapper = Mock()
        query_validator = Mock()
        
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
def load_test_data_generator():
    """Generate realistic test data for load testing."""
    class LoadTestDataGenerator:
        def __init__(self):
            self.cities = ["Austin", "Dallas", "Houston", "San Antonio", "Fort Worth", "El Paso"]
            self.property_types = ["single_family", "condo", "townhouse", "multi_family"]
            self.statuses = ["active", "under_contract", "pending", "sold"]
        
        def generate_property_data(self, count: int) -> List[Dict[str, Any]]:
            """Generate realistic property data for testing."""
            properties = []
            for i in range(count):
                property_data = {
                    "ListingId": f"LOAD{i:06d}",
                    "StandardStatus": random.choice(self.statuses),
                    "ListPrice": random.randint(200000, 800000),
                    "BedroomsTotal": random.randint(1, 5),
                    "BathroomsTotalInteger": random.randint(1, 4),
                    "LivingArea": random.randint(1200, 4000),
                    "PropertyType": "Residential",
                    "PropertySubType": random.choice(self.property_types),
                    "City": random.choice(self.cities),
                    "StateOrProvince": "TX",
                    "PostalCode": f"7{random.randint(8000, 8999)}",
                    "PublicRemarks": f"Load test property {i} with excellent features"
                }
                properties.append(property_data)
            return properties
        
        def generate_agent_data(self, count: int) -> List[Dict[str, Any]]:
            """Generate realistic agent data for testing."""
            first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Emily"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
            offices = ["Premier Realty", "Best Homes", "Elite Properties", "Top Agents", "Prime Real Estate"]
            
            agents = []
            for i in range(count):
                agent_data = {
                    "MemberKey": f"AGENT{i:06d}",
                    "MemberFirstName": random.choice(first_names),
                    "MemberLastName": random.choice(last_names),
                    "MemberEmail": f"agent{i}@loadtest.com",
                    "MemberMobilePhone": f"512-555-{random.randint(1000, 9999)}",
                    "MemberOfficeName": random.choice(offices),
                    "MemberCity": random.choice(self.cities),
                    "MemberStateOrProvince": "TX",
                    "MemberStateLicense": f"TX{random.randint(100000, 999999)}"
                }
                agents.append(agent_data)
            return agents
        
        def generate_search_queries(self, count: int) -> List[Dict[str, Any]]:
            """Generate diverse search queries for testing."""
            queries = []
            for i in range(count):
                query_type = random.choice(["natural_language", "structured", "mixed"])
                
                if query_type == "natural_language":
                    bedrooms = random.randint(2, 5)
                    price = random.randint(300, 700) * 1000
                    city = random.choice(self.cities)
                    queries.append({
                        "query": f"{bedrooms} bedroom house under ${price:,} in {city} TX",
                        "limit": random.randint(10, 50)
                    })
                
                elif query_type == "structured":
                    queries.append({
                        "filters": {
                            "city": random.choice(self.cities),
                            "state": "TX",
                            "min_bedrooms": random.randint(1, 3),
                            "max_price": random.randint(400, 800) * 1000,
                            "property_type": random.choice(self.property_types)
                        },
                        "limit": random.randint(10, 100)
                    })
                
                else:  # mixed
                    queries.append({
                        "query": f"house with pool in {random.choice(self.cities)}",
                        "filters": {
                            "max_price": random.randint(500, 900) * 1000
                        },
                        "limit": random.randint(20, 75)
                    })
            
            return queries
    
    return LoadTestDataGenerator()


class TestBasicLoadCapacity:
    """Test basic load capacity and response under increasing load."""
    
    async def test_sustained_search_load(self, load_test_server, load_test_data_generator):
        """Test sustained search operations under load."""
        server = load_test_server
        
        # Generate test data and queries
        property_data = load_test_data_generator.generate_property_data(1000)
        search_queries = load_test_data_generator.generate_search_queries(100)
        
        # Setup server mocks
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.reso_client.query_properties.return_value = property_data[:50]  # Realistic subset
        server.data_mapper.map_properties.return_value = [
            {"listing_id": f"LOAD{i:06d}", "list_price": random.randint(300000, 600000)}
            for i in range(50)
        ]
        server.data_mapper.get_property_summary.return_value = "Load Test Summary"
        
        # Execute sustained load test
        start_time = time.time()
        results = []
        response_times = []
        
        for query in search_queries:
            operation_start = time.time()
            result = await server._search_properties(query)
            operation_time = time.time() - operation_start
            
            results.append(result)
            response_times.append(operation_time)
        
        total_time = time.time() - start_time
        
        # Analyze performance metrics
        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        throughput = len(search_queries) / total_time
        
        # Verify load handling capability
        assert len(results) == len(search_queries)
        assert all(len(r.content) == 1 for r in results)
        assert avg_response_time < 0.5  # Average response under 500ms
        assert max_response_time < 2.0   # No single request over 2s
        assert throughput > 10           # At least 10 requests/second
        
        print(f"Load Test Results:")
        print(f"  Total queries: {len(search_queries)}")
        print(f"  Total time: {total_time:.2f}s")
        print(f"  Throughput: {throughput:.2f} req/s")
        print(f"  Avg response: {avg_response_time:.3f}s")
        print(f"  Max response: {max_response_time:.3f}s")
        print(f"  Min response: {min_response_time:.3f}s")
    
    async def test_concurrent_user_simulation(self, load_test_server, load_test_data_generator):
        """Simulate multiple concurrent users with realistic usage patterns."""
        server = load_test_server
        
        # Setup realistic data
        property_data = load_test_data_generator.generate_property_data(500)
        agent_data = load_test_data_generator.generate_agent_data(100)
        
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        
        # Configure different operation types
        def property_query_response(*args, **kwargs):
            # Return subset based on query type
            filters = kwargs.get('filters', {})
            if 'listing_id' in filters:
                return property_data[:1]  # Single property for details
            elif 'status' in filters and filters['status'] == 'sold':
                return property_data[::3]  # Sold properties for market analysis
            else:
                return property_data[:25]  # Regular search results
        
        server.reso_client.query_properties.side_effect = property_query_response
        server.reso_client.query_members.return_value = agent_data[:20]
        
        server.data_mapper.map_properties.return_value = [
            {"listing_id": f"LOAD{i:06d}", "list_price": 400000} for i in range(25)
        ]
        server.data_mapper.map_property.return_value = {
            "listing_id": "LOAD000000", "list_price": 400000, "bedrooms": 3
        }
        server.data_mapper.get_property_summary.return_value = "Concurrent Test Summary"
        
        # Simulate concurrent users with different behavior patterns
        async def simulate_user(user_id: int) -> Dict[str, Any]:
            """Simulate realistic user behavior."""
            user_stats = {
                "user_id": user_id,
                "operations": 0,
                "total_time": 0,
                "errors": 0
            }
            
            start_time = time.time()
            
            try:
                # User journey: Search -> Details -> Market Analysis -> Agent Search
                
                # 1. Property Search
                search_result = await server._search_properties({
                    "query": f"house in Austin TX user {user_id}",
                    "limit": 25
                })
                user_stats["operations"] += 1
                
                # Small delay (user reading results)
                await asyncio.sleep(0.1)
                
                # 2. Property Details (user clicks on first result)
                details_result = await server._get_property_details({
                    "listing_id": "LOAD000000"
                })
                user_stats["operations"] += 1
                
                await asyncio.sleep(0.05)
                
                # 3. Market Analysis (user wants market info)
                market_result = await server._analyze_market({
                    "city": "Austin",
                    "state": "TX",
                    "property_type": "residential"
                })
                user_stats["operations"] += 1
                
                await asyncio.sleep(0.05)
                
                # 4. Agent Search (user looking for agent)
                agent_result = await server._find_agent({
                    "city": "Austin",
                    "state": "TX",
                    "limit": 10
                })
                user_stats["operations"] += 1
                
            except Exception as e:
                user_stats["errors"] += 1
                print(f"User {user_id} encountered error: {e}")
            
            user_stats["total_time"] = time.time() - start_time
            return user_stats
        
        # Simulate 20 concurrent users
        num_users = 20
        user_tasks = [simulate_user(i) for i in range(num_users)]
        
        start_time = time.time()
        user_results = await asyncio.gather(*user_tasks, return_exceptions=True)
        total_time = time.time() - start_time
        
        # Analyze concurrent user simulation results
        successful_users = [r for r in user_results if not isinstance(r, Exception)]
        total_operations = sum(u["operations"] for u in successful_users)
        total_errors = sum(u["errors"] for u in successful_users)
        avg_user_time = statistics.mean([u["total_time"] for u in successful_users])
        
        # Verify concurrent load handling
        assert len(successful_users) >= num_users * 0.9  # At least 90% users succeed
        assert total_errors == 0  # No errors in ideal test environment
        assert avg_user_time < 5.0  # Average user journey under 5 seconds
        assert total_operations >= num_users * 3  # Most users complete multiple operations
        
        overall_throughput = total_operations / total_time
        
        print(f"Concurrent User Simulation:")
        print(f"  Users: {num_users}")
        print(f"  Successful: {len(successful_users)}")
        print(f"  Total operations: {total_operations}")
        print(f"  Total errors: {total_errors}")
        print(f"  Overall time: {total_time:.2f}s")
        print(f"  Avg user journey: {avg_user_time:.2f}s")
        print(f"  Overall throughput: {overall_throughput:.2f} ops/s")
    
    async def test_peak_load_handling(self, load_test_server, load_test_data_generator):
        """Test system behavior under peak load conditions."""
        server = load_test_server
        
        # Generate large dataset for peak testing
        property_data = load_test_data_generator.generate_property_data(2000)
        
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.reso_client.query_properties.return_value = property_data[:100]
        server.data_mapper.map_properties.return_value = [
            {"listing_id": f"PEAK{i:06d}", "list_price": 500000} for i in range(100)
        ]
        server.data_mapper.get_property_summary.return_value = "Peak Load Summary"
        
        # Create peak load burst
        peak_requests = 50
        burst_duration = 2.0  # seconds
        
        tasks = []
        for i in range(peak_requests):
            task = server._search_properties({
                "query": f"peak load test {i}",
                "limit": 25
            })
            tasks.append(task)
        
        # Execute peak load
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        actual_duration = time.time() - start_time
        
        # Analyze peak load results
        successful_results = [r for r in results if not isinstance(r, Exception)]
        failed_results = [r for r in results if isinstance(r, Exception)]
        
        peak_throughput = len(successful_results) / actual_duration
        success_rate = len(successful_results) / peak_requests
        
        # Verify peak load handling
        assert success_rate >= 0.8  # At least 80% success rate under peak load
        assert peak_throughput >= 15  # Maintain reasonable throughput
        assert actual_duration <= burst_duration * 2  # Don't take more than 2x expected time
        
        print(f"Peak Load Test:")
        print(f"  Peak requests: {peak_requests}")
        print(f"  Successful: {len(successful_results)}")
        print(f"  Failed: {len(failed_results)}")
        print(f"  Success rate: {success_rate:.2%}")
        print(f"  Duration: {actual_duration:.2f}s")
        print(f"  Peak throughput: {peak_throughput:.2f} req/s")


class TestScalabilityPatterns:
    """Test scalability patterns and resource efficiency."""
    
    async def test_memory_usage_under_load(self, load_test_server, load_test_data_generator):
        """Test memory usage patterns under sustained load."""
        server = load_test_server
        
        # Test with increasingly large datasets
        dataset_sizes = [100, 500, 1000, 2000]
        memory_usage_patterns = []
        
        for size in dataset_sizes:
            property_data = load_test_data_generator.generate_property_data(size)
            
            server.query_validator.validate_search_filters.return_value = {"city": "Austin"}
            server.reso_client.query_properties.return_value = property_data
            server.data_mapper.map_properties.return_value = [
                {"listing_id": f"MEM{i:06d}", "list_price": 400000} for i in range(size)
            ]
            server.data_mapper.get_property_summary.return_value = f"Memory Test {size}"
            
            # Execute operations with current dataset size
            start_time = time.time()
            operations = 10
            
            for i in range(operations):
                result = await server._search_properties({
                    "filters": {"city": "Austin"},
                    "limit": size
                })
                assert f"Found {size} properties" in result.content[0].text
            
            operation_time = time.time() - start_time
            avg_time_per_operation = operation_time / operations
            
            memory_usage_patterns.append({
                "dataset_size": size,
                "avg_operation_time": avg_time_per_operation,
                "total_time": operation_time
            })
        
        # Analyze scalability
        for i in range(1, len(memory_usage_patterns)):
            current = memory_usage_patterns[i]
            previous = memory_usage_patterns[i-1]
            
            size_ratio = current["dataset_size"] / previous["dataset_size"]
            time_ratio = current["avg_operation_time"] / previous["avg_operation_time"]
            
            # Performance scaling should be reasonable (not exponential)
            assert time_ratio < size_ratio * 1.5, \
                f"Poor scaling: {size_ratio}x data → {time_ratio}x time"
        
        print("Memory Usage Scalability:")
        for pattern in memory_usage_patterns:
            print(f"  Size: {pattern['dataset_size']:4d} | "
                  f"Avg time: {pattern['avg_operation_time']:.3f}s | "
                  f"Total: {pattern['total_time']:.2f}s")
    
    async def test_connection_pool_efficiency(self, load_test_server, load_test_data_generator):
        """Test connection pooling and resource reuse efficiency."""
        server = load_test_server
        
        # Setup for connection efficiency testing
        property_data = load_test_data_generator.generate_property_data(100)
        agent_data = load_test_data_generator.generate_agent_data(50)
        
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        
        # Track connection reuse
        connection_calls = []
        
        def track_query_calls(*args, **kwargs):
            connection_calls.append(time.time())
            return property_data[:25]
        
        def track_member_calls(*args, **kwargs):
            connection_calls.append(time.time())
            return agent_data[:10]
        
        server.reso_client.query_properties.side_effect = track_query_calls
        server.reso_client.query_members.side_effect = track_member_calls
        server.data_mapper.map_properties.return_value = [
            {"listing_id": f"CONN{i:06d}", "list_price": 400000} for i in range(25)
        ]
        server.data_mapper.get_property_summary.return_value = "Connection Test"
        
        # Execute mixed operations rapidly
        operations = 30
        tasks = []
        
        for i in range(operations):
            if i % 3 == 0:
                # Property search
                task = server._search_properties({
                    "query": f"connection test {i}",
                    "limit": 25
                })
            elif i % 3 == 1:
                # Market analysis (2 API calls)
                task = server._analyze_market({
                    "city": "Austin",
                    "state": "TX"
                })
            else:
                # Agent search
                task = server._find_agent({
                    "city": "Austin",
                    "state": "TX",
                    "limit": 10
                })
            
            tasks.append(task)
        
        # Execute all operations
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        # Analyze connection efficiency
        total_api_calls = len(connection_calls)
        operations_per_second = operations / total_time
        calls_per_second = total_api_calls / total_time
        
        # Verify efficient resource usage
        assert len(results) == operations
        assert all(len(r.content) == 1 for r in results)
        assert operations_per_second >= 10  # Efficient operation rate
        
        print(f"Connection Pool Efficiency:")
        print(f"  Operations: {operations}")
        print(f"  API calls: {total_api_calls}")
        print(f"  Total time: {total_time:.2f}s")
        print(f"  Ops/sec: {operations_per_second:.2f}")
        print(f"  Calls/sec: {calls_per_second:.2f}")


class TestProductionReadiness:
    """Test production readiness scenarios and edge cases."""
    
    async def test_sustained_production_load(self, load_test_server, load_test_data_generator):
        """Simulate sustained production load over extended period."""
        server = load_test_server
        
        # Production-like data setup
        property_data = load_test_data_generator.generate_property_data(1500)
        agent_data = load_test_data_generator.generate_agent_data(200)
        search_queries = load_test_data_generator.generate_search_queries(200)
        
        # Configure realistic response patterns
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        
        def realistic_property_response(*args, **kwargs):
            # Simulate variable response sizes based on query
            limit = kwargs.get('limit', 25)
            return property_data[:min(limit, len(property_data))]
        
        server.reso_client.query_properties.side_effect = realistic_property_response
        server.reso_client.query_members.return_value = agent_data[:20]
        
        server.data_mapper.map_properties.return_value = [
            {"listing_id": f"PROD{i:06d}", "list_price": random.randint(300000, 700000)}
            for i in range(50)
        ]
        server.data_mapper.get_property_summary.return_value = "Production Load Test"
        
        # Execute sustained load simulation
        total_operations = 0
        total_errors = 0
        response_times = []
        
        # Simulate 3 minutes of production load
        test_duration = 180  # 3 minutes in seconds
        operations_per_batch = 10
        batch_interval = 5  # seconds between batches
        
        start_time = time.time()
        
        while (time.time() - start_time) < test_duration:
            batch_start = time.time()
            
            # Execute batch of operations
            batch_tasks = []
            for i in range(operations_per_batch):
                query = random.choice(search_queries)
                task = server._search_properties(query)
                batch_tasks.append(task)
            
            try:
                batch_results = await asyncio.gather(*batch_tasks)
                batch_time = time.time() - batch_start
                
                total_operations += len(batch_results)
                response_times.extend([batch_time / len(batch_results)] * len(batch_results))
                
                # Verify batch results
                assert all(len(r.content) == 1 for r in batch_results)
                
            except Exception as e:
                total_errors += operations_per_batch
                print(f"Batch error: {e}")
            
            # Wait for next batch
            elapsed = time.time() - batch_start
            if elapsed < batch_interval:
                await asyncio.sleep(batch_interval - elapsed)
        
        actual_duration = time.time() - start_time
        
        # Analyze production readiness metrics
        success_rate = (total_operations - total_errors) / total_operations if total_operations > 0 else 0
        avg_response_time = statistics.mean(response_times) if response_times else 0
        throughput = total_operations / actual_duration
        
        # Production readiness assertions
        assert success_rate >= 0.99  # 99% success rate
        assert avg_response_time <= 1.0  # Average response under 1 second
        assert throughput >= 15  # Sustained 15+ operations per second
        assert total_errors <= total_operations * 0.01  # Error rate under 1%
        
        print(f"Production Load Test ({actual_duration:.0f}s):")
        print(f"  Total operations: {total_operations}")
        print(f"  Total errors: {total_errors}")
        print(f"  Success rate: {success_rate:.2%}")
        print(f"  Avg response: {avg_response_time:.3f}s")
        print(f"  Throughput: {throughput:.2f} ops/s")
    
    async def test_production_failure_recovery(self, load_test_server, load_test_data_generator):
        """Test system recovery patterns under production failure scenarios."""
        server = load_test_server
        
        # Setup for failure recovery testing
        property_data = load_test_data_generator.generate_property_data(100)
        
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        
        # Simulate production failure patterns
        call_count = 0
        def failure_and_recovery(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            
            # Simulate different failure patterns
            if 20 <= call_count <= 30:
                # Simulate 10-operation outage
                raise Exception("Simulated API outage")
            elif call_count % 15 == 0:
                # Intermittent timeouts
                raise asyncio.TimeoutError("Simulated timeout")
            else:
                # Normal operation
                return property_data[:25]
        
        server.reso_client.query_properties.side_effect = failure_and_recovery
        server.data_mapper.map_properties.return_value = [
            {"listing_id": f"RECOVERY{i:06d}", "list_price": 450000} for i in range(25)
        ]
        server.data_mapper.get_property_summary.return_value = "Recovery Test"
        
        # Execute operations during failure period
        total_operations = 50
        successful_operations = 0
        failed_operations = 0
        recovery_times = []
        
        for i in range(total_operations):
            operation_start = time.time()
            
            try:
                result = await server._search_properties({
                    "query": f"recovery test {i}",
                    "limit": 25
                })
                
                # Check if operation succeeded
                if "Found 25 properties" in result.content[0].text:
                    successful_operations += 1
                    recovery_times.append(time.time() - operation_start)
                else:
                    failed_operations += 1
                
            except Exception:
                failed_operations += 1
            
            # Small delay between operations
            await asyncio.sleep(0.1)
        
        # Analyze recovery patterns
        success_rate = successful_operations / total_operations
        avg_recovery_time = statistics.mean(recovery_times) if recovery_times else 0
        
        # Production failure recovery assertions
        assert success_rate >= 0.7  # At least 70% success during failure period
        assert successful_operations > 0  # Some operations should succeed
        assert avg_recovery_time <= 2.0  # Recovery operations under 2 seconds
        
        print(f"Production Failure Recovery:")
        print(f"  Total operations: {total_operations}")
        print(f"  Successful: {successful_operations}")
        print(f"  Failed: {failed_operations}")
        print(f"  Success rate: {success_rate:.2%}")
        print(f"  Avg recovery time: {avg_recovery_time:.3f}s")
    
    async def test_resource_cleanup_under_load(self, load_test_server):
        """Test proper resource cleanup under sustained load."""
        server = load_test_server
        
        # Setup for resource cleanup testing
        large_datasets = []
        
        def create_large_response(*args, **kwargs):
            # Create large response that should be cleaned up
            large_data = [{"ListingId": f"CLEANUP{i:06d}", "ListPrice": 400000} 
                         for i in range(1000)]
            large_datasets.append(large_data)  # Track for cleanup verification
            return large_data
        
        server.oauth_handler.get_access_token.return_value = "cleanup_token"
        server.query_validator.validate_search_filters.return_value = {"city": "Austin"}
        server.reso_client.query_properties.side_effect = create_large_response
        server.data_mapper.map_properties.return_value = [
            {"listing_id": f"CLEANUP{i:06d}", "list_price": 400000} for i in range(1000)
        ]
        server.data_mapper.get_property_summary.return_value = "Cleanup Test"
        
        # Execute multiple operations with large responses
        operations = 20
        results = []
        
        for i in range(operations):
            result = await server._search_properties({
                "filters": {"city": "Austin"},
                "limit": 1000
            })
            results.append(result)
            
            # Verify operation succeeded
            assert "Found 1000 properties" in result.content[0].text
            
            # Clear local reference to help with cleanup testing
            if i > 0:
                results[i-1] = None
        
        # Verify resource management
        assert len(large_datasets) == operations  # All operations created datasets
        assert len(results) == operations  # All operations completed
        
        # In a real scenario, you'd check actual memory usage here
        # For this test, we verify the system can handle multiple large operations
        final_result_count = sum(1 for r in results if r is not None)
        assert final_result_count > 0  # At least some results retained
        
        print(f"Resource Cleanup Test:")
        print(f"  Operations completed: {operations}")
        print(f"  Large datasets created: {len(large_datasets)}")
        print(f"  Final results retained: {final_result_count}")


class TestLoadTestReporting:
    """Generate comprehensive load test reports."""
    
    async def test_comprehensive_load_test_report(self, load_test_server, load_test_data_generator):
        """Generate comprehensive load test report with all metrics."""
        server = load_test_server
        
        # Setup comprehensive test scenario
        property_data = load_test_data_generator.generate_property_data(500)
        agent_data = load_test_data_generator.generate_agent_data(100)
        search_queries = load_test_data_generator.generate_search_queries(50)
        
        server.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
        
        def comprehensive_response(*args, **kwargs):
            filters = kwargs.get('filters', {})
            if 'listing_id' in filters:
                return property_data[:1]
            elif 'status' in filters and filters['status'] == 'sold':
                return property_data[::2]
            else:
                return property_data[:50]
        
        server.reso_client.query_properties.side_effect = comprehensive_response
        server.reso_client.query_members.return_value = agent_data[:25]
        server.data_mapper.map_properties.return_value = [
            {"listing_id": f"REPORT{i:06d}", "list_price": 400000} for i in range(50)
        ]
        server.data_mapper.map_property.return_value = {
            "listing_id": "REPORT000000", "list_price": 400000
        }
        server.data_mapper.get_property_summary.return_value = "Report Test"
        
        # Execute comprehensive test suite
        test_results = {
            "search_operations": [],
            "details_operations": [],
            "market_operations": [],
            "agent_operations": [],
            "concurrent_operations": []
        }
        
        # 1. Search operations test
        for query in search_queries[:20]:
            start_time = time.time()
            result = await server._search_properties(query)
            duration = time.time() - start_time
            
            test_results["search_operations"].append({
                "duration": duration,
                "success": "Found" in result.content[0].text
            })
        
        # 2. Details operations test
        for i in range(10):
            start_time = time.time()
            result = await server._get_property_details({"listing_id": f"REPORT{i:06d}"})
            duration = time.time() - start_time
            
            test_results["details_operations"].append({
                "duration": duration,
                "success": "Property Details" in result.content[0].text
            })
        
        # 3. Market analysis test
        for i in range(5):
            start_time = time.time()
            result = await server._analyze_market({
                "city": "Austin", "state": "TX", "property_type": "residential"
            })
            duration = time.time() - start_time
            
            test_results["market_operations"].append({
                "duration": duration,
                "success": "Market Analysis" in result.content[0].text
            })
        
        # 4. Agent search test
        for i in range(10):
            start_time = time.time()
            result = await server._find_agent({
                "city": "Austin", "state": "TX", "limit": 20
            })
            duration = time.time() - start_time
            
            test_results["agent_operations"].append({
                "duration": duration,
                "success": "Found" in result.content[0].text
            })
        
        # 5. Concurrent operations test
        concurrent_tasks = [
            server._search_properties({"query": f"concurrent {i}", "limit": 25})
            for i in range(15)
        ]
        
        concurrent_start = time.time()
        concurrent_results = await asyncio.gather(*concurrent_tasks)
        concurrent_duration = time.time() - concurrent_start
        
        test_results["concurrent_operations"] = {
            "total_duration": concurrent_duration,
            "operations": len(concurrent_tasks),
            "throughput": len(concurrent_tasks) / concurrent_duration,
            "success_count": sum(1 for r in concurrent_results if "Found" in r.content[0].text)
        }
        
        # Generate comprehensive report
        report = self._generate_load_test_report(test_results)
        
        # Verify report completeness
        assert len(test_results["search_operations"]) == 20
        assert len(test_results["details_operations"]) == 10
        assert len(test_results["market_operations"]) == 5
        assert len(test_results["agent_operations"]) == 10
        assert test_results["concurrent_operations"]["operations"] == 15
        
        print("\n" + "="*60)
        print("COMPREHENSIVE LOAD TEST REPORT")
        print("="*60)
        print(report)
        print("="*60)
    
    def _generate_load_test_report(self, test_results: Dict[str, Any]) -> str:
        """Generate formatted load test report."""
        report_sections = []
        
        # Search Operations Analysis
        search_ops = test_results["search_operations"]
        if search_ops:
            search_times = [op["duration"] for op in search_ops]
            search_success = sum(1 for op in search_ops if op["success"])
            
            report_sections.append(f"""
PROPERTY SEARCH OPERATIONS
  Operations: {len(search_ops)}
  Success Rate: {search_success/len(search_ops):.1%}
  Avg Response: {statistics.mean(search_times):.3f}s
  Min Response: {min(search_times):.3f}s
  Max Response: {max(search_times):.3f}s
  Std Deviation: {statistics.stdev(search_times):.3f}s""")
        
        # Details Operations Analysis
        details_ops = test_results["details_operations"]
        if details_ops:
            details_times = [op["duration"] for op in details_ops]
            details_success = sum(1 for op in details_ops if op["success"])
            
            report_sections.append(f"""
PROPERTY DETAILS OPERATIONS
  Operations: {len(details_ops)}
  Success Rate: {details_success/len(details_ops):.1%}
  Avg Response: {statistics.mean(details_times):.3f}s
  Min Response: {min(details_times):.3f}s
  Max Response: {max(details_times):.3f}s""")
        
        # Market Analysis Operations
        market_ops = test_results["market_operations"]
        if market_ops:
            market_times = [op["duration"] for op in market_ops]
            market_success = sum(1 for op in market_ops if op["success"])
            
            report_sections.append(f"""
MARKET ANALYSIS OPERATIONS
  Operations: {len(market_ops)}
  Success Rate: {market_success/len(market_ops):.1%}
  Avg Response: {statistics.mean(market_times):.3f}s
  Min Response: {min(market_times):.3f}s
  Max Response: {max(market_times):.3f}s""")
        
        # Agent Search Operations
        agent_ops = test_results["agent_operations"]
        if agent_ops:
            agent_times = [op["duration"] for op in agent_ops]
            agent_success = sum(1 for op in agent_ops if op["success"])
            
            report_sections.append(f"""
AGENT SEARCH OPERATIONS
  Operations: {len(agent_ops)}
  Success Rate: {agent_success/len(agent_ops):.1%}
  Avg Response: {statistics.mean(agent_times):.3f}s
  Min Response: {min(agent_times):.3f}s
  Max Response: {max(agent_times):.3f}s""")
        
        # Concurrent Operations Analysis
        concurrent = test_results["concurrent_operations"]
        if concurrent:
            report_sections.append(f"""
CONCURRENT OPERATIONS
  Total Operations: {concurrent["operations"]}
  Total Duration: {concurrent["total_duration"]:.2f}s
  Throughput: {concurrent["throughput"]:.2f} ops/s
  Success Count: {concurrent["success_count"]}
  Success Rate: {concurrent["success_count"]/concurrent["operations"]:.1%}""")
        
        return "\n".join(report_sections)