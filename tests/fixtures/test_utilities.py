"""Test utilities and helper functions for comprehensive testing."""

import time
import asyncio
import functools
from typing import Dict, Any, List, Optional, Callable, Union, Tuple
from unittest.mock import AsyncMock, Mock, patch
import statistics
import json
import tempfile
import os
from contextlib import contextmanager
from datetime import datetime, timedelta

from .property_fixtures import PropertyDataFixtures
from .agent_fixtures import AgentDataFixtures
from .market_fixtures import MarketDataFixtures


class TestUtilities:
    """Comprehensive test utilities for all testing scenarios."""
    
    def __init__(self):
        self.property_fixtures = PropertyDataFixtures()
        self.agent_fixtures = AgentDataFixtures()
        self.market_fixtures = MarketDataFixtures()
    
    # Performance Testing Utilities
    
    @staticmethod
    def time_async_function(func: Callable) -> Callable:
        """Decorator to time async function execution."""
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Add timing info to result if it's a dict
            if hasattr(result, '__dict__'):
                result._execution_time = execution_time
            
            return result, execution_time
        return wrapper
    
    @staticmethod
    def benchmark_function(iterations: int = 1, warmup: int = 0):
        """Decorator to benchmark function performance over multiple iterations."""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                # Warmup runs
                for _ in range(warmup):
                    await func(*args, **kwargs)
                
                # Benchmark runs
                times = []
                results = []
                
                for _ in range(iterations):
                    start_time = time.time()
                    result = await func(*args, **kwargs)
                    end_time = time.time()
                    
                    times.append(end_time - start_time)
                    results.append(result)
                
                # Calculate statistics
                benchmark_stats = {
                    "iterations": iterations,
                    "mean_time": statistics.mean(times),
                    "median_time": statistics.median(times),
                    "min_time": min(times),
                    "max_time": max(times),
                    "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
                    "total_time": sum(times)
                }
                
                return results[-1], benchmark_stats
            return wrapper
        return decorator
    
    @staticmethod
    async def measure_concurrent_performance(tasks: List[Callable], 
                                           max_concurrent: int = 10) -> Dict[str, Any]:
        """Measure performance of concurrent task execution."""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def run_with_semaphore(task):
            async with semaphore:
                start_time = time.time()
                try:
                    result = await task()
                    success = True
                    error = None
                except Exception as e:
                    result = None
                    success = False
                    error = str(e)
                
                return {
                    "result": result,
                    "success": success,
                    "error": error,
                    "execution_time": time.time() - start_time
                }
        
        start_time = time.time()
        results = await asyncio.gather(*[run_with_semaphore(task) for task in tasks])
        total_time = time.time() - start_time
        
        # Calculate performance metrics
        successful_results = [r for r in results if r["success"]]
        failed_results = [r for r in results if not r["success"]]
        
        execution_times = [r["execution_time"] for r in successful_results]
        
        return {
            "total_tasks": len(tasks),
            "successful_tasks": len(successful_results),
            "failed_tasks": len(failed_results),
            "success_rate": len(successful_results) / len(tasks),
            "total_execution_time": total_time,
            "avg_task_time": statistics.mean(execution_times) if execution_times else 0,
            "min_task_time": min(execution_times) if execution_times else 0,
            "max_task_time": max(execution_times) if execution_times else 0,
            "throughput": len(successful_results) / total_time if total_time > 0 else 0,
            "results": results
        }
    
    # Mock and Fixture Utilities
    
    def create_comprehensive_server_mock(self, **config) -> Mock:
        """Create a comprehensive mock server with all components."""
        server_mock = Mock()
        
        # OAuth handler mock
        oauth_mock = AsyncMock()
        oauth_mock.get_access_token.return_value = config.get("auth_token", "test_token")
        server_mock.oauth_handler = oauth_mock
        
        # RESO client mock
        client_mock = AsyncMock()
        server_mock.reso_client = client_mock
        
        # Data mapper mock
        mapper_mock = Mock()
        server_mock.data_mapper = mapper_mock
        
        # Query validator mock
        validator_mock = Mock()
        server_mock.query_validator = validator_mock
        
        # Configure default behaviors
        self._configure_default_mock_behaviors(server_mock, **config)
        
        return server_mock
    
    def _configure_default_mock_behaviors(self, server_mock: Mock, **config):
        """Configure default mock behaviors for server components."""
        # Default property data
        default_properties = self.property_fixtures.create_property_dataset(
            config.get("property_count", 50)
        )
        
        # Default agent data
        default_agents = self.agent_fixtures.create_agent_dataset(
            config.get("agent_count", 20)
        )
        
        # Configure RESO client responses
        server_mock.reso_client.query_properties.return_value = default_properties
        server_mock.reso_client.query_members.return_value = default_agents
        
        # Configure data mapper responses
        mapped_properties = [
            self.property_fixtures.create_mapped_property(prop) 
            for prop in default_properties
        ]
        server_mock.data_mapper.map_properties.return_value = mapped_properties
        server_mock.data_mapper.map_property.return_value = mapped_properties[0] if mapped_properties else {}
        server_mock.data_mapper.get_property_summary.return_value = "Test Property Summary"
        
        # Configure query validator responses
        server_mock.query_validator.parse_natural_language_query.return_value = {
            "city": "Austin", "state": "TX"
        }
        server_mock.query_validator.validate_search_filters.return_value = {
            "city": "Austin", "state": "TX"
        }
    
    def create_realistic_api_responses(self, scenario: str = "balanced") -> Dict[str, Any]:
        """Create realistic API response datasets for different scenarios."""
        scenarios = {
            "balanced": {
                "active_count": 150,
                "sold_count": 80,
                "agent_count": 30,
                "market_tempo": "balanced"
            },
            "hot_market": {
                "active_count": 50,
                "sold_count": 120,
                "agent_count": 25,
                "market_tempo": "hot"
            },
            "slow_market": {
                "active_count": 300,
                "sold_count": 40,
                "agent_count": 35,
                "market_tempo": "slow"
            },
            "luxury_market": {
                "active_count": 25,
                "sold_count": 15,
                "agent_count": 15,
                "market_tempo": "exclusive"
            }
        }
        
        config = scenarios.get(scenario, scenarios["balanced"])
        
        # Generate appropriate property mix
        if scenario == "luxury_market":
            properties = [
                self.property_fixtures.create_luxury_property(f"LUX{i:04d}")
                for i in range(config["active_count"])
            ]
        else:
            properties = self.property_fixtures.create_property_dataset(
                config["active_count"]
            )
        
        # Generate sold properties
        sold_properties = [
            self.property_fixtures.create_sold_property(f"SOLD{i:04d}")
            for i in range(config["sold_count"])
        ]
        
        # Generate agents with appropriate specializations
        agent_types = ["basic", "top_producer"] if scenario == "luxury_market" else None
        agents = self.agent_fixtures.create_agent_dataset(
            config["agent_count"], agent_types
        )
        
        return {
            "active_properties": properties,
            "sold_properties": sold_properties,
            "agents": agents,
            "market_config": config
        }
    
    # Error Simulation Utilities
    
    @staticmethod
    def create_error_simulator(error_rate: float = 0.1, error_types: List[str] = None):
        """Create an error simulator for testing error handling."""
        if error_types is None:
            error_types = ["timeout", "connection", "auth", "server"]
        
        error_map = {
            "timeout": asyncio.TimeoutError("Simulated timeout"),
            "connection": ConnectionError("Simulated connection error"),
            "auth": PermissionError("Simulated auth error"),
            "server": Exception("Simulated server error")
        }
        
        call_count = 0
        
        def simulate_error(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            
            if call_count % int(1 / error_rate) == 0:
                error_type = error_types[call_count % len(error_types)]
                raise error_map[error_type]
            
            return "success"
        
        return simulate_error
    
    @staticmethod
    def create_cascading_failure_simulator(failure_sequence: List[str]):
        """Create a simulator for cascading failures."""
        call_count = 0
        
        def simulate_cascading_failure(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            
            if call_count <= len(failure_sequence):
                failure_type = failure_sequence[call_count - 1]
                if failure_type == "success":
                    return "success"
                else:
                    raise Exception(f"Cascading failure: {failure_type}")
            
            return "success"  # Recovery after sequence
        
        return simulate_cascading_failure
    
    # Data Validation Utilities
    
    @staticmethod
    def validate_property_data_structure(property_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate property data structure and completeness."""
        required_fields = [
            "ListingId", "StandardStatus", "ListPrice", "BedroomsTotal",
            "BathroomsTotalInteger", "City", "StateOrProvince"
        ]
        
        errors = []
        
        # Check required fields
        for field in required_fields:
            if field not in property_data:
                errors.append(f"Missing required field: {field}")
            elif property_data[field] is None:
                errors.append(f"Required field is None: {field}")
        
        # Validate data types
        if "ListPrice" in property_data and not isinstance(property_data["ListPrice"], (int, float)):
            errors.append("ListPrice must be numeric")
        
        if "BedroomsTotal" in property_data and not isinstance(property_data["BedroomsTotal"], int):
            errors.append("BedroomsTotal must be integer")
        
        # Validate ranges
        if "ListPrice" in property_data and property_data["ListPrice"] < 0:
            errors.append("ListPrice cannot be negative")
        
        if "BedroomsTotal" in property_data and property_data["BedroomsTotal"] < 0:
            errors.append("BedroomsTotal cannot be negative")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_agent_data_structure(agent_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate agent data structure and completeness."""
        required_fields = [
            "MemberKey", "MemberFirstName", "MemberLastName", 
            "MemberEmail", "MemberOfficeName", "MemberCity", "MemberStateOrProvince"
        ]
        
        errors = []
        
        # Check required fields
        for field in required_fields:
            if field not in agent_data:
                errors.append(f"Missing required field: {field}")
            elif agent_data[field] is None:
                errors.append(f"Required field is None: {field}")
        
        # Validate email format (basic)
        if "MemberEmail" in agent_data and "@" not in str(agent_data["MemberEmail"]):
            errors.append("Invalid email format")
        
        return len(errors) == 0, errors
    
    # Test Data Management
    
    @contextmanager
    def temporary_test_data(self, data: Dict[str, Any]):
        """Context manager for temporary test data files."""
        temp_files = {}
        
        try:
            for name, content in data.items():
                temp_file = tempfile.NamedTemporaryFile(
                    mode='w', suffix='.json', delete=False
                )
                json.dump(content, temp_file, indent=2, default=str)
                temp_file.close()
                temp_files[name] = temp_file.name
            
            yield temp_files
            
        finally:
            # Cleanup
            for temp_file in temp_files.values():
                try:
                    os.unlink(temp_file)
                except FileNotFoundError:
                    pass
    
    def create_test_dataset_collection(self, size: str = "medium") -> Dict[str, Any]:
        """Create a comprehensive test dataset collection."""
        size_configs = {
            "small": {"properties": 50, "agents": 20, "locations": 2},
            "medium": {"properties": 200, "agents": 50, "locations": 4},
            "large": {"properties": 1000, "agents": 200, "locations": 8},
            "xl": {"properties": 5000, "agents": 500, "locations": 12}
        }
        
        config = size_configs.get(size, size_configs["medium"])
        
        # Generate diverse property data
        property_types = ["basic", "luxury", "condo", "investment", "new_construction", "sold"]
        properties = self.property_fixtures.create_property_dataset(
            config["properties"], property_types
        )
        
        # Generate diverse agent data
        agent_types = ["basic", "top_producer", "new_agent", "broker", "commercial"]
        agents = self.agent_fixtures.create_agent_dataset(
            config["agents"], agent_types
        )
        
        # Generate market data for multiple locations
        cities = ["Austin", "Dallas", "Houston", "San Antonio"][:config["locations"]]
        market_data = {}
        
        for city in cities:
            market_data[city] = self.market_fixtures.create_market_snapshot(city)
        
        return {
            "properties": properties,
            "agents": agents,
            "market_data": market_data,
            "config": config,
            "generation_timestamp": datetime.now().isoformat()
        }
    
    # Assertion Utilities
    
    @staticmethod
    def assert_response_format(response: Any, expected_structure: Dict[str, Any]):
        """Assert that response matches expected structure."""
        assert hasattr(response, 'content'), "Response must have content attribute"
        assert len(response.content) > 0, "Response content cannot be empty"
        assert hasattr(response.content[0], 'text'), "Response content must have text attribute"
        
        content_text = response.content[0].text
        assert isinstance(content_text, str), "Response content text must be string"
        assert len(content_text) > 0, "Response content text cannot be empty"
        
        # Check for expected content patterns
        for pattern, should_exist in expected_structure.items():
            if should_exist:
                assert pattern in content_text, f"Expected pattern '{pattern}' not found in response"
            else:
                assert pattern not in content_text, f"Unexpected pattern '{pattern}' found in response"
    
    @staticmethod
    def assert_performance_metrics(metrics: Dict[str, Any], thresholds: Dict[str, float]):
        """Assert that performance metrics meet specified thresholds."""
        for metric, threshold in thresholds.items():
            assert metric in metrics, f"Missing performance metric: {metric}"
            
            if metric.endswith("_rate") or metric.endswith("_ratio"):
                # Rate/ratio metrics (0-1 scale)
                assert 0 <= metrics[metric] <= 1, f"Rate/ratio metric {metric} out of range: {metrics[metric]}"
            
            if metric.startswith("max_"):
                # Maximum thresholds
                assert metrics[metric] <= threshold, f"Metric {metric} exceeds threshold: {metrics[metric]} > {threshold}"
            elif metric.startswith("min_"):
                # Minimum thresholds
                assert metrics[metric] >= threshold, f"Metric {metric} below threshold: {metrics[metric]} < {threshold}"
            else:
                # Default: maximum threshold
                assert metrics[metric] <= threshold, f"Metric {metric} exceeds threshold: {metrics[metric]} > {threshold}"
    
    # Reporting Utilities
    
    def generate_test_report(self, test_results: Dict[str, Any], 
                           test_type: str = "comprehensive") -> str:
        """Generate a comprehensive test report."""
        report_sections = []
        
        # Header
        report_sections.append(f"# {test_type.title()} Test Report")
        report_sections.append(f"Generated: {datetime.now().isoformat()}")
        report_sections.append("")
        
        # Summary
        if "summary" in test_results:
            summary = test_results["summary"]
            report_sections.append("## Summary")
            report_sections.append(f"- Total Tests: {summary.get('total_tests', 0)}")
            report_sections.append(f"- Passed: {summary.get('passed', 0)}")
            report_sections.append(f"- Failed: {summary.get('failed', 0)}")
            report_sections.append(f"- Success Rate: {summary.get('success_rate', 0):.1%}")
            report_sections.append("")
        
        # Performance Metrics
        if "performance" in test_results:
            perf = test_results["performance"]
            report_sections.append("## Performance Metrics")
            report_sections.append(f"- Average Response Time: {perf.get('avg_response_time', 0):.3f}s")
            report_sections.append(f"- Throughput: {perf.get('throughput', 0):.2f} ops/sec")
            report_sections.append(f"- Error Rate: {perf.get('error_rate', 0):.2%}")
            report_sections.append("")
        
        # Detailed Results
        if "details" in test_results:
            report_sections.append("## Detailed Results")
            for test_name, result in test_results["details"].items():
                status = "✅ PASS" if result.get("passed", False) else "❌ FAIL"
                report_sections.append(f"### {test_name} {status}")
                
                if "metrics" in result:
                    for metric, value in result["metrics"].items():
                        report_sections.append(f"- {metric}: {value}")
                
                if "errors" in result and result["errors"]:
                    report_sections.append("**Errors:**")
                    for error in result["errors"]:
                        report_sections.append(f"- {error}")
                
                report_sections.append("")
        
        return "\n".join(report_sections)
    
    def save_test_artifacts(self, artifacts: Dict[str, Any], 
                           base_path: str = "/tmp/test_artifacts") -> Dict[str, str]:
        """Save test artifacts to files."""
        os.makedirs(base_path, exist_ok=True)
        saved_files = {}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for name, content in artifacts.items():
            filename = f"{name}_{timestamp}.json"
            filepath = os.path.join(base_path, filename)
            
            with open(filepath, 'w') as f:
                json.dump(content, f, indent=2, default=str)
            
            saved_files[name] = filepath
        
        return saved_files