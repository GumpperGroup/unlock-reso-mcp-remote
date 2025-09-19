# Error Quick Reference - UNLOCK MLS MCP Server

**Last Updated**: July 27, 2025  
**Status**: CRITICAL ERRORS IDENTIFIED

## 🚨 Critical Error Summary

| Error | Severity | Impact | Files Affected | Quick Fix |
|-------|----------|--------|----------------|-----------|
| OAuth method missing | CRITICAL | Server won't start | 40+ files | Add `get_access_token()` method |
| Mock configurations | HIGH | Tests failing | 24+ test files | Update mock setup |
| Data type mismatches | MEDIUM | Secondary failures | Test fixtures | Fix mock return types |

## Primary Error: OAuth2Handler Method Missing

### Error Message:
```
AttributeError: 'OAuth2Handler' object has no attribute 'get_access_token'
```

### Root Cause:
- **Expected**: `await self.oauth_handler.get_access_token()`
- **Available**: `await self.oauth_handler.get_valid_token()`

### Affected Locations:
```bash
src/server.py:1156                    # Tool implementation
src/server.py:1757                    # Server startup
tests/test_*.py (40+ occurrences)     # All authentication mocks
docs/configuration.md:272             # Documentation
```

### Quick Fix:
```python
# Add to OAuth2Handler class (src/auth/oauth2.py):
async def get_access_token(self) -> str:
    """Get access token (alias for get_valid_token for API consistency)."""
    return await self.get_valid_token()
```

## Test Failure Patterns

### Pattern 1: Authentication Mock Failures
```python
# ❌ FAILING (40+ occurrences):
server.oauth_handler.get_access_token.return_value = "test_token"

# ✅ WORKING ALTERNATIVE:
server.oauth_handler.get_valid_token.return_value = "test_token"
```

### Pattern 2: Data Type Mock Failures  
```python
# ❌ FAILING:
result_text = f"Found {len(mapped_properties)} properties:\n\n"
# TypeError: object of type 'Mock' has no len()

# ✅ WORKING FIX:
# Ensure mock returns actual list instead of Mock object
server.data_mapper.map_properties.return_value = [
    {"listing_id": "123", "price": 500000},
    {"listing_id": "456", "price": 600000}
]
```

### Pattern 3: Server Startup Failures
```bash
# ❌ FAILING:
$ python -m main
AttributeError: 'OAuth2Handler' object has no attribute 'get_access_token'

# ✅ WORKING (after OAuth fix):
$ python -m main
2025-07-27 21:43:13 - src.server - INFO - Starting UNLOCK MLS MCP server
```

## Test Module Status Quick Reference

| Module | Status | Tests | Issue | Fix Priority |
|--------|--------|-------|-------|--------------|
| `test_tools.py` | ✅ PASSING | 21/21 | None | ✅ Complete |
| `test_oauth2.py` | ✅ PASSING | 19/19 | None | ✅ Complete |
| `test_data_mapper.py` | ✅ PASSING | 29/29 | None | ✅ Complete |
| `test_error_scenarios.py` | ❌ FAILING | 0/24 | OAuth mocks | 🔴 HIGH |
| `test_integration.py` | ⚠️ PARTIAL | 6/10 | OAuth mocks | 🔴 HIGH |
| `test_load.py` | ❌ FAILING | 2/5+ | OAuth mocks | 🟡 MEDIUM |
| `test_performance.py` | ❌ TIMEOUT | 0/15+ | OAuth mocks | 🟡 MEDIUM |
| `test_validators.py` | ❓ UNKNOWN | ?/15+ | Likely OAuth | 🟡 MEDIUM |
| `test_reso_client.py` | ❓ UNKNOWN | ?/25+ | Likely OAuth | 🟡 MEDIUM |

## Error Resolution Checklist

### ✅ Step 1: Fix Core Authentication (CRITICAL)
- [ ] Add `get_access_token()` method to OAuth2Handler
- [ ] Test server startup: `python -m main`
- [ ] Verify no AttributeError on OAuth calls

### ✅ Step 2: Validate Core Tests (HIGH)
- [ ] Run core tests: `pytest tests/test_tools.py tests/test_oauth2.py tests/test_data_mapper.py -v`
- [ ] Ensure 69/69 tests still passing
- [ ] Verify test execution time < 1 second

### ✅ Step 3: Fix Error Scenario Tests (HIGH)
- [ ] Update mock configurations in `test_error_scenarios.py`
- [ ] Run: `pytest tests/test_error_scenarios.py -v`
- [ ] Target: 24/24 tests passing

### ✅ Step 4: Fix Integration Tests (MEDIUM)
- [ ] Update mock configurations in `test_integration.py`
- [ ] Run: `pytest tests/test_integration.py -v`
- [ ] Target: 10/10 tests passing

### ✅ Step 5: Validate Full Suite (MEDIUM)
- [ ] Run: `pytest tests/ -v`
- [ ] Target: 195+ tests with 85%+ success rate
- [ ] Execution time: < 2 minutes

## Development Commands

### Test Authentication Fix:
```bash
# 1. Test server startup
python -m main

# 2. Test core functionality
pytest tests/test_tools.py tests/test_oauth2.py tests/test_data_mapper.py -v

# 3. Test error scenarios
pytest tests/test_error_scenarios.py -v

# 4. Test integration
pytest tests/test_integration.py -v

# 5. Full test suite
pytest tests/ -v --tb=short
```

### Debug Authentication Issues:
```bash
# Check OAuth2Handler methods
python -c "from src.auth.oauth2 import OAuth2Handler; print(dir(OAuth2Handler))"

# Test authentication flow
python -c "import asyncio; from src.auth.oauth2 import OAuth2Handler; h = OAuth2Handler(); print('Methods:', [m for m in dir(h) if not m.startswith('_')])"
```

## Common Error Messages

### 1. Server Startup Error
```
AttributeError: 'OAuth2Handler' object has no attribute 'get_access_token'
```
**Fix**: Add `get_access_token()` method to OAuth2Handler

### 2. Test Mock Error  
```
AttributeError: Mock object has no attribute 'get_access_token'
```
**Fix**: Update test mocks to use `get_valid_token()` OR implement `get_access_token()`

### 3. Data Type Error
```
TypeError: object of type 'Mock' has no len()
```
**Fix**: Configure mocks to return appropriate data types (lists, dicts, etc.)

### 4. Test Timeout Error
```
FAILED tests/test_integration.py - Timeout after 120 seconds
```
**Fix**: Resolve authentication issues causing infinite waits

## Emergency Rollback Plan

If OAuth2Handler changes break existing functionality:

### Option 1: Revert and Use Alternative
```python
# Revert OAuth2Handler changes
# Update all 40+ callers to use get_valid_token()
```

### Option 2: Implement Wrapper
```python
# Keep both methods:
async def get_access_token(self) -> str:
    return await self.get_valid_token()
    
async def get_valid_token(self) -> str:
    # existing implementation
```

## Success Indicators

### Immediate Success (Within 1 hour):
- ✅ Server starts without errors
- ✅ Core tools tests (21) still passing
- ✅ OAuth tests (19) still passing

### Short-term Success (Within 1 day):
- ✅ Error scenario tests (24) passing
- ✅ Integration tests (10) passing
- ✅ 90%+ of full test suite passing

### Long-term Success (Within 1 week):
- ✅ Performance tests functional
- ✅ Load tests providing metrics
- ✅ Real API integration validated

---

**Contact**: For questions about these errors, refer to the detailed analysis files:
- `comprehensive-test-errors.md` - Overall error analysis
- `technical-error-analysis.md` - Detailed technical breakdown
- `test-execution-summary.md` - Complete test results