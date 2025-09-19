# Troubleshooting Guide - UNLOCK MLS MCP Server Error Resolution

**Document Version**: 1.0  
**Created**: July 27, 2025  
**Reference**: error-resolution-plan.md, implementation-checklist.md

## 🚨 **Emergency Quick Reference**

### **Critical Issues & Immediate Solutions**

| Issue | Symptom | Immediate Fix | Reference |
|-------|---------|---------------|-----------|
| Server won't start | `AttributeError: 'OAuth2Handler' object has no attribute 'get_access_token'` | Add `get_access_token()` method to OAuth2Handler | Section 1.1 |
| Tests failing with auth errors | `Mock object has no attribute 'get_access_token'` | OAuth method now exists, re-run tests | Section 2.1 |
| Data type errors in tests | `TypeError: object of type 'Mock' has no len()` | Fix mock return types to actual data structures | Section 2.2 |
| Test timeouts | Tests hang for 2+ minutes | Authentication fix should resolve, check mock configs | Section 2.3 |

### **Emergency Rollback Commands**

```bash
# Complete rollback to known good state
git reset --hard HEAD~[number-of-commits]

# Rollback just OAuth fix
git checkout HEAD -- src/auth/oauth2.py

# Rollback just test fixes  
git checkout HEAD -- tests/
```

## 🔧 **Phase 1: OAuth2Handler Issues**

### **Problem**: Server Startup Failure

**Symptoms**:
```
Traceback (most recent call last):
  File "/Users/davidgumpper/Documents/projects/unlock-reso-mcp/src/server.py", line 1757, in run
    await self.oauth_handler.get_access_token()
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'OAuth2Handler' object has no attribute 'get_access_token'
```

**Root Cause**: OAuth2Handler class only implements `get_valid_token()` but server code expects `get_access_token()`

**Solution**: Add alias method to OAuth2Handler

**Troubleshooting Steps**:

1. **Verify current methods**:
```bash
python -c "from src.auth.oauth2 import OAuth2Handler; print([m for m in dir(OAuth2Handler) if 'token' in m])"
```

Expected output before fix:
```
['get_valid_token', '_access_token']
```

2. **Add method to OAuth2Handler**:
```python
async def get_access_token(self) -> str:
    """Get access token (alias for get_valid_token for API consistency)."""
    return await self.get_valid_token()
```

3. **Verify method added**:
```bash
python -c "from src.auth.oauth2 import OAuth2Handler; print('get_access_token' in dir(OAuth2Handler))"
```

Expected output after fix:
```
True
```

4. **Test server startup**:
```bash
python -m main
```

**Expected Success**: Server should start without AttributeError (may fail on authentication due to missing credentials, but that's a different issue)

### **Problem**: Method Addition Causes Syntax Errors

**Symptoms**:
```
  File "/Users/davidgumpper/Documents/projects/unlock-reso-mcp/src/auth/oauth2.py", line X
    async def get_access_token(self) -> str:
        ^
SyntaxError: invalid syntax
```

**Troubleshooting**:
1. **Check indentation**: Ensure method is properly indented inside the class
2. **Check placement**: Add method after existing methods, before class end
3. **Check syntax**: Verify proper async/await syntax

**Correct Implementation**:
```python
class OAuth2Handler:
    # ... existing methods ...
    
    async def get_valid_token(self) -> str:
        # existing implementation
        pass
    
    async def get_access_token(self) -> str:  # ← Add here
        """Get access token (alias for get_valid_token for API consistency)."""
        return await self.get_valid_token()
```

### **Problem**: Method Added But Tests Still Fail

**Symptoms**: Server starts but tests still show AttributeError

**Troubleshooting**:
1. **Check import cache**: Restart Python interpreter
2. **Verify method signature**: Ensure exact signature matches expectations
3. **Check method visibility**: Ensure method is public (not starting with _)

```bash
# Force reload
python -c "
import importlib
import src.auth.oauth2
importlib.reload(src.auth.oauth2)
from src.auth.oauth2 import OAuth2Handler
print('Methods:', [m for m in dir(OAuth2Handler) if 'access' in m])
"
```

## 🧪 **Phase 2: Test Infrastructure Issues**

### **Problem**: Authentication Mock Failures

**Symptoms**:
```python
# In test output:
AttributeError: Mock object has no attribute 'get_access_token'
```

**Root Cause**: Tests are properly mocking `get_access_token` but method didn't exist before Phase 1 fix

**Solution**: After Phase 1 fix, these should automatically work

**Troubleshooting**:
1. **Re-run specific test**:
```bash
pytest tests/test_error_scenarios.py::TestAuthenticationErrors::test_oauth_token_failure -v
```

2. **If still failing, check mock configuration**:
```python
# In test file, verify mock setup:
server.oauth_handler.get_access_token.return_value = "test_token"
# Should work after Phase 1 fix
```

3. **Verify Phase 1 fix is complete**: Ensure method exists in OAuth2Handler

### **Problem**: Data Type Mock Failures

**Symptoms**:
```python
TypeError: object of type 'Mock' has no len()
# Or similar errors when code expects lists/dicts but gets Mock objects
```

**Root Cause**: Mock configurations return Mock objects instead of proper data types

**Solution**: Update mock configurations to return appropriate data structures

**Common Fixes**:

1. **Property data mocks**:
```python
# ❌ WRONG (returns Mock):
server.data_mapper.map_properties.return_value = Mock()

# ✅ CORRECT (returns list):
server.data_mapper.map_properties.return_value = [
    {"listing_id": "TEST001", "price": 500000, "bedrooms": 3},
    {"listing_id": "TEST002", "price": 600000, "bedrooms": 4}
]
```

2. **Agent data mocks**:
```python
# ❌ WRONG:
server.reso_client.query_members.return_value = Mock()

# ✅ CORRECT:
server.reso_client.query_members.return_value = [
    {"MemberKey": "AGT001", "MemberFirstName": "John", "MemberLastName": "Smith"},
    {"MemberKey": "AGT002", "MemberFirstName": "Jane", "MemberLastName": "Doe"}
]
```

3. **Market analysis mocks**:
```python
# ❌ WRONG:
server.data_mapper.create_market_analysis.return_value = Mock()

# ✅ CORRECT:
server.data_mapper.create_market_analysis.return_value = {
    "average_price": 450000,
    "median_price": 425000,
    "total_properties": 150,
    "price_trend": "stable"
}
```

**Troubleshooting Steps**:

1. **Identify specific error**:
```bash
pytest tests/test_error_scenarios.py::TestAuthenticationErrors::test_oauth_token_failure -v --tb=long
```

2. **Look for TypeError patterns**: Find where code expects specific data types

3. **Update corresponding mock**: Replace Mock() with appropriate data structure

4. **Validate fix**:
```bash
pytest tests/test_error_scenarios.py::TestAuthenticationErrors::test_oauth_token_failure -v
```

### **Problem**: Test Timeouts

**Symptoms**: Tests hang for 2+ minutes then timeout

**Root Cause**: Usually authentication issues causing infinite loops or waits

**Troubleshooting**:

1. **Check if Phase 1 fix is complete**: Server should start without AttributeError

2. **Run single test with timeout**:
```bash
timeout 30 pytest tests/test_integration.py::TestEndToEndWorkflows::test_complete_property_search_workflow -v
```

3. **Check for infinite loops**: Look for authentication retry loops

4. **Verify mock configurations**: Ensure mocks return quickly

**Common Solutions**:
- Phase 1 OAuth fix usually resolves timeouts
- If still hanging, check for missing return values in mocks
- Ensure async mocks are properly configured

### **Problem**: Mixed Test Results (Some Pass, Some Fail)

**Symptoms**: Inconsistent test results across runs

**Troubleshooting**:

1. **Run tests multiple times**:
```bash
for i in {1..3}; do echo "Run $i:"; pytest tests/test_error_scenarios.py -v --tb=no; done
```

2. **Check for race conditions**: Especially in concurrent tests

3. **Look for shared state**: Tests may be affecting each other

4. **Isolate problematic tests**:
```bash
pytest tests/test_error_scenarios.py::TestAuthenticationErrors -v
pytest tests/test_error_scenarios.py::TestNetworkErrors -v
```

## 🔍 **Phase 3: Full Test Suite Issues**

### **Problem**: Performance/Load Tests Still Failing

**Symptoms**: Performance or load tests timeout or fail after OAuth fix

**Root Cause**: These tests may have additional complexity beyond authentication

**Troubleshooting**:

1. **Check if tests actually run**:
```bash
pytest tests/test_performance.py -v --tb=short -x
```

2. **Look for performance-specific issues**:
- Resource exhaustion
- Timing dependencies  
- Complex mock setups

3. **Simplify test parameters**: Reduce load/duration for debugging

4. **Check system resources**: Ensure adequate memory/CPU

### **Problem**: Unknown Test Modules Have Unique Issues

**Symptoms**: test_validators.py or test_reso_client.py have different failure patterns

**Troubleshooting**:

1. **Run modules individually**:
```bash
pytest tests/test_validators.py -v --tb=short
pytest tests/test_reso_client.py -v --tb=short  
```

2. **Check for module-specific dependencies**: May need different mock patterns

3. **Look for import errors**: May have missing dependencies

4. **Check test structure**: Ensure tests follow expected patterns

### **Problem**: Low Overall Success Rate

**Symptoms**: Even after fixes, success rate is <80%

**Root Cause Analysis**:

1. **Categorize failures**:
```bash
pytest tests/ -v --tb=no | grep "FAILED" | cut -d':' -f1 | sort | uniq -c
```

2. **Look for patterns**:
- Authentication-related: Should be fixed by Phase 1
- Data type issues: Need mock fixes
- New issues: May need investigation

3. **Prioritize fixes**: Focus on highest-impact issues first

## 📋 **Phase 4: Quality Assurance Issues**

### **Problem**: Documentation Still Has Wrong Method Names

**Symptoms**: Documentation references `get_valid_token()` instead of `get_access_token()`

**Solution**: Update documentation to use consistent API

**Find and Replace**:
```bash
# Find all references
grep -r "get_valid_token\|get_access_token" docs/ README.md CLAUDE.md

# Update as needed to use get_access_token() for consistency
```

### **Problem**: Coverage Drops Below 89%

**Symptoms**: Code coverage report shows <89%

**Troubleshooting**:

1. **Run coverage with working tests only**:
```bash
pytest tests/test_tools.py tests/test_oauth2.py tests/test_data_mapper.py --cov=src --cov-report=term
```

2. **Compare before/after**: Ensure no regression in covered lines

3. **Check if new lines added**: New method should be covered by tests

### **Problem**: MCP Functionality Not Working

**Symptoms**: Tools or resources fail when tested

**Troubleshooting**:

1. **Test tools individually**: Isolate which tools have issues

2. **Check authentication flow**: Ensure tools can authenticate

3. **Verify mock configurations**: Tools may need proper mocks for testing

## 🚀 **Phase 5: Production Issues**

### **Problem**: Real API Authentication Fails

**Symptoms**: Works with mocks but fails with real Bridge Interactive API

**Troubleshooting**:

1. **Check credentials**: Verify `.env` file has correct values

2. **Test authentication directly**:
```bash
python -c "
import asyncio
from src.auth.oauth2 import OAuth2Handler

async def test_auth():
    handler = OAuth2Handler()
    try:
        token = await handler.authenticate()
        print('Success:', bool(token))
    except Exception as e:
        print('Error:', e)

asyncio.run(test_auth())
"
```

3. **Check network connectivity**: Ensure API endpoint is reachable

### **Problem**: Performance Issues in Production

**Symptoms**: Slower than expected response times

**Troubleshooting**:

1. **Profile specific operations**: Identify bottlenecks

2. **Check API rate limits**: May be hitting Bridge Interactive limits

3. **Monitor resource usage**: Look for memory/CPU issues

## 🔄 **Common Rollback Scenarios**

### **Rollback Scenario 1: OAuth Fix Breaks Something**

**When**: After adding `get_access_token()` method, unexpected issues arise

**Quick Rollback**:
```bash
git checkout HEAD -- src/auth/oauth2.py
```

**Alternative Fix**: Instead of rollback, update all callers to use `get_valid_token()`

### **Rollback Scenario 2: Test Fixes Create New Issues**

**When**: Mock updates cause new test failures

**Selective Rollback**:
```bash
git checkout HEAD -- tests/test_error_scenarios.py
git checkout HEAD -- tests/test_integration.py
```

**Debugging**: Run tests individually to isolate problematic changes

### **Rollback Scenario 3: Complete System Regression**

**When**: Multiple issues arise, need to return to known good state

**Full Rollback**:
```bash
# Find last known good commit
git log --oneline -10

# Reset to that commit
git reset --hard [commit-hash]
```

## 📊 **Success Indicators & Validation**

### **Phase 1 Success Validation**

```bash
# All should succeed:
python -c "from src.auth.oauth2 import OAuth2Handler; print('get_access_token' in dir(OAuth2Handler))"  # Should print True
python -m main &; sleep 3; kill %1  # Should start without AttributeError
pytest tests/test_tools.py tests/test_oauth2.py tests/test_data_mapper.py -v  # Should pass 69/69
```

### **Phase 2 Success Validation**

```bash
# Significant improvement expected:
pytest tests/test_error_scenarios.py -v --tb=no | grep -c "PASSED"  # Should be >15/24
pytest tests/test_integration.py -v --tb=no | grep -c "PASSED"      # Should be >8/10
```

### **Complete Success Validation**

```bash
# Final validation:
pytest tests/ -v --tb=no | grep "==.*=="  # Should show 165+/195+ passed
python -m main &; sleep 5; kill %1         # Should start normally
pytest --cov=src --cov-report=term | grep "TOTAL"  # Should show 89%+
```

## 📞 **Getting Help**

### **Error Patterns Not Covered**

If encountering errors not covered in this guide:

1. **Document the error**: Full traceback and context
2. **Check error-quick-reference.md**: May have additional patterns
3. **Search for similar patterns**: In technical-error-analysis.md
4. **Create minimal reproduction**: Isolate the issue

### **Performance Issues**

For performance-related problems:

1. **Profile the specific operation**: Use Python profiling tools
2. **Check resource usage**: Monitor memory/CPU during tests
3. **Compare with baseline**: Use before/after measurements

### **Integration Issues**

For problems with real API integration:

1. **Validate credentials**: Test authentication separately
2. **Check API documentation**: Verify expected behavior
3. **Test with curl**: Validate API access outside Python

---

**This troubleshooting guide covers the most common issues expected during error resolution. Update this document with any new patterns discovered during implementation.**