# Distance Tool Debugging Guide

## Issues Fixed

### ✅ 1. Parameter Mismatch (Fixed)
**Problem**: Server was passing `property_address=property_address` but location service expected `address`
**Fix**: Changed parameter name in `src/server.py` line 1258
```python
# Before:
property_address=property_address,
# After:
address=property_address,
```

### ✅ 2. Result Processing Error (Fixed)
**Problem**: Server was treating response as a list, but location service returns a dictionary
**Fix**: Extract `nearest_locations` from response dictionary in `src/server.py` lines 1264-1265
```python
# Added:
locations = results.get('nearest_locations', []) if results else []
```

### ✅ 3. Distance Field Mismatch (Fixed)
**Problem**: Server looking for `distance_miles` but service provides `straight_line_distance_miles`
**Fix**: Updated field name in `src/server.py` line 1281
```python
# Before:
distance = place.get('distance_miles', 0)
# After:
distance = place.get('straight_line_distance_miles', 0)
```

### ✅ 4. Enhanced Error Logging (Added)
**Improvement**: Added detailed error logging and debugging information
**Location**: `src/server.py` lines 1310-1346

### ✅ 5. Google Places API Field Mask Fix (Added)
**Problem**: API requests were using incorrect "fields" parameter causing "Invalid JSON payload" errors
**Fix**: Updated to use proper `X-Goog-FieldMask` header instead of "fields" in request body
**Location**: `src/utils/google_places_client.py` lines 300-302 and 391-393
```python
# Before (incorrect):
"fields": "places.location,places.displayName"

# After (correct):
headers = {
    'X-Goog-FieldMask': 'places.location,places.displayName'
}
```

## Configuration Requirements

### Google Maps API Key Setup

1. **Get API Key**:
   - Visit: https://console.developers.google.com/apis/credentials
   - Create a new API key or use existing one
   - Enable these APIs:
     - Places API (New)
     - Geocoding API

2. **Configure in Project**:

   **Option A: Environment Variable**
   ```bash
   export GOOGLE_MAPS_API_KEY=your_actual_api_key_here
   ```

   **Option B: .env File**
   ```bash
   # Add to .env file
   GOOGLE_MAPS_API_KEY=your_actual_api_key_here
   ```

3. **Verify Configuration**:
   Run the diagnostic script:
   ```bash
   python diagnose_location_service.py
   ```

## Current Error Analysis

Based on the error "I apologize, but the unlock MLS MCP server's find_distance_to_nearest function is experiencing technical issues", here are the most likely causes:

### 🔍 Most Likely Issues:

1. **Google Maps API Key Missing or Invalid**
   - The API key might not be properly loaded
   - The API key might be invalid or expired
   - Required APIs (Places API, Geocoding API) might not be enabled

2. **API Permissions**
   - The API key might not have permissions for Places API
   - Billing might not be enabled for the Google Cloud project
   - API quotas might be exceeded

3. **Network/Connectivity Issues**
   - Firewall blocking requests to Google APIs
   - Network connectivity issues

## Debugging Steps

### Step 1: Check Current Error Details
With the enhanced error logging, you should now see more detailed error information. Look for logs containing:
- "Google Maps API key status"
- "Location service status"
- "Exception type" and "Exception message"

### Step 2: Verify API Key Configuration
```bash
# Check if environment variable is set
echo $GOOGLE_MAPS_API_KEY

# Check .env file
grep GOOGLE_MAPS_API_KEY .env
```

### Step 3: Test API Key Manually
```bash
# Test API key with curl (replace YOUR_API_KEY)
curl "https://maps.googleapis.com/maps/api/place/textsearch/json?query=hospital+near+Austin+TX&key=YOUR_API_KEY"
```

### Step 4: Check Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Go to APIs & Services > Credentials
4. Verify your API key exists and is enabled
5. Go to APIs & Services > Library
6. Ensure these APIs are enabled:
   - Places API (New)
   - Geocoding API

### Step 5: Check Billing
- Ensure billing is enabled for your Google Cloud project
- Check quota usage in the Google Cloud Console

## Expected Behavior After Fixes

Once properly configured, the distance tool should:

1. **Accept these parameters**:
   - `property_address`: Full address (e.g., "2502 Spruceleaf CIR, Austin, TX 78757")
   - `place_type`: Type of place (e.g., "hospital", "school", "restaurant")
   - `radius_miles`: Search radius (default: 5.0, max: 25.0)
   - `max_results`: Maximum results (default: 5, max: 20)

2. **Return formatted results** with:
   - List of nearby locations
   - Distances in miles
   - Addresses and ratings (if available)
   - Search summary

3. **Handle errors gracefully** with specific error messages for:
   - Missing API key
   - Authentication failures
   - Rate limit exceeded
   - Location not found

## Testing the Fix

Use this test case:
```json
{
  "property_address": "2502 Spruceleaf CIR, Austin, TX 78757",
  "place_type": "hospital",
  "max_results": 5,
  "radius_miles": 10
}
```

Expected result: List of hospitals within 10 miles with distances.

## Contact for Further Help

If issues persist after following this guide:
1. Check the enhanced error logs for specific error details
2. Verify Google Maps API key configuration
3. Test the API key manually with curl
4. Check Google Cloud Console for billing and quota issues

The enhanced error logging will now provide much more specific information about what's failing.