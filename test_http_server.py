#!/usr/bin/env python3
"""
Test script for UNLOCK MLS MCP Server with HTTP Remote transport
"""

import asyncio
import requests
import json
from typing import Dict, Any

# Configuration
SERVER_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health endpoint."""
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    try:
        response = requests.get(f"{SERVER_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_tools_endpoint():
    """Test the tools endpoint."""
    try:
        response = requests.get(f"{SERVER_URL}/tools", timeout=5)
        if response.status_code == 200:
            print("✅ Tools endpoint working")
            data = response.json()
            tools = data.get("tools", [])
            print(f"   Available tools: {len(tools)}")
            for tool in tools:
                print(f"   - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
            return True
        else:
            print(f"❌ Tools endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Tools endpoint error: {e}")
        return False

def test_mcp_protocol():
    """Test MCP protocol endpoints."""
    print("\n🔍 Testing MCP Protocol Endpoints...")
    
    # Test initialization
    try:
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(f"{SERVER_URL}/mcp", json=init_request, timeout=5)
        if response.status_code == 200:
            print("✅ MCP initialization working")
            return True
        else:
            print(f"❌ MCP initialization failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ MCP initialization error: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing UNLOCK MLS MCP Server - HTTP Remote Transport")
    print("=" * 60)
    
    # Test basic endpoints
    print("\n📡 Testing Basic Endpoints...")
    health_ok = test_health_endpoint()
    root_ok = test_root_endpoint()
    tools_ok = test_tools_endpoint()
    
    # Test MCP protocol
    mcp_ok = test_mcp_protocol()
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 30)
    print(f"Health Endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Root Endpoint: {'✅ PASS' if root_ok else '❌ FAIL'}")
    print(f"Tools Endpoint: {'✅ PASS' if tools_ok else '❌ FAIL'}")
    print(f"MCP Protocol: {'✅ PASS' if mcp_ok else '❌ FAIL'}")
    
    if all([health_ok, root_ok, tools_ok, mcp_ok]):
        print("\n🎉 All tests passed! Server is ready for use.")
    else:
        print("\n⚠️  Some tests failed. Check server logs for details.")
    
    print("\n📝 Next Steps:")
    print("1. Configure Bridge Interactive credentials in .env")
    print("2. Test with actual MCP client")
    print("3. Deploy to production environment")

if __name__ == "__main__":
    main()
