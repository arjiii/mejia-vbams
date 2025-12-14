# Assistance Request Enhancement Implementation Plan

## Current Issues
1. ❌ Error: "models.Breakdown() got multiple values for keyword argument 'vehicle_id'"
2. ❌ User cannot select a specific service provider
3. ❌ Providers not sorted by distance
4. ❌ User location not shown prominently on map

## Required Changes

### 1. Fix Backend Breakdown Creation Error
**File:** `backend/routers/breakdowns.py`
- Check for duplicate `vehicle_id` parameter
- Ensure CreateBreakdownRequest schema matches Breakdown model

### 2. Enhanced Frontend - Provider Selection
**File:** `frontend/src/routes/assistance/+page.svelte`
- Add provider selection UI between breakdown form and submit
- Show providers sorted by distance (nearest first)
- Display provider card with:
  - Business name
  - Distance in km
  - Services offered
  - Rating (if available)
  - Radio button to select
- Make provider selection required before submission

### 3. Improve Map Display
**File:** `frontend/src/routes/assistance/+page.svelte`
- Show user's current location with distinct marker (blue pin)
- Show service providers with different markers (green pins)
- Auto-center map on user location when obtained
- Show distance lines/circles from user to providers

### 4. Backend - Add Provider to Assistance Request
**File:** `backend/routers/assistance.py`
- Add `service_provider_id` field to AssistanceRequest
- Update CreateAssistanceRequest schema
- Validate that selected provider exists and is verified

### 5. Sort Providers by Distance
**File:** `backend/routers/service_providers.py`
- Ensure get_nearby endpoint returns providers sorted by distance ASC
- Add distance calculation to response

## Implementation Steps

### Step 1: Fix Backend Error ✅
1. Review breakdown creation endpoint
2. Fix duplicate parameter issue
3. Test API endpoint

### Step 2: Add Provider Selection to Frontend
1. Create provider selection section after location
2. Add radio buttons for each provider
3. Show distance prominently
4. Make it required

### Step 3: Update Assistance Request Flow
1. Include selected_provider_id in submission
2. Update backend to accept provider_id
3. Assign request directly to selected provider

### Step 4: Enhance Map
1. Different marker colors for user vs providers
2. Auto-zoom to show all markers
3. Click provider marker to select

## Expected User Flow

1. User enters location (GPS or manual)
2. System fetches nearby providers, sorted by distance
3. Map shows user location + provider locations
4. User sees provider list with distances
5. User selects preferred provider
6. User submits request
7. Request is assigned to selected provider immediately

## Success Criteria

✅ No backend errors during breakdown creation
✅ Providers shown sorted by distance (nearest first)
✅ User can see distance in km for each provider
✅ User can select which provider to request
✅ Map shows user location clearly
✅ Map shows all nearby provider locations
✅ Selected provider receives the assistance request directly
