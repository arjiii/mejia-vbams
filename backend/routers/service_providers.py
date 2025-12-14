from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json

from database import get_db
from models import User, ServiceProvider
from schemas import (
    ServiceProviderCreate, 
    ServiceProviderResponse, 
    ServiceProviderUpdate,
    ServiceProviderLocationUpdate,
    MessageResponse,
    ServiceProviderPublicResponse,
    EarningsResponse,
    ServiceProviderAdminDetail
)
from auth import get_current_user, require_service_provider, require_admin, require_service_provider_any_status

router = APIRouter()

# ... (Previous endpoints omitted)

@router.get("/profile", response_model=ServiceProviderResponse)
async def get_current_service_provider(
    current_user: User = Depends(require_service_provider_any_status),
    db: Session = Depends(get_db)
):
    """Get current service provider profile."""
    profile = db.query(ServiceProvider).filter(ServiceProvider.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/profile", response_model=ServiceProviderResponse)
async def update_current_service_provider(
    profile_data: ServiceProviderUpdate,
    current_user: User = Depends(require_service_provider_any_status),
    db: Session = Depends(get_db)
):
    """Update current service provider profile."""
    profile = db.query(ServiceProvider).filter(ServiceProvider.user_id == current_user.id).first()
    
    # Logic to map schema to model - assumes schema fields match model fields
    update_data = profile_data.dict(exclude_unset=True)
    
    if not profile:
        # Create new profile logic
        profile = ServiceProvider(user_id=current_user.id, **update_data)
        
        # Defaults
        if not profile.business_name: profile.business_name = current_user.first_name + "'s Business"
        if not profile.business_license: profile.business_license = f"TEMP-{current_user.id}"
        if not profile.latitude: profile.latitude = 0.0
        if not profile.longitude: profile.longitude = 0.0
        if not profile.base_rate: profile.base_rate = 500.0
        
        # Handle services serialization
        services_list = update_data.get('services', [])
        # Provide default empty list if None, otherwise serialize
        if services_list is None:
            profile.services = json.dumps([])
        else:
            # Convert Enums to string values for JSON serialization
            profile.services = json.dumps([s.value if hasattr(s, 'value') else s for s in services_list])
        
        # Handle documents serialization
        docs_list = update_data.get('documents', [])
        if docs_list is None:
            profile.documents = json.dumps([])
        else:
            profile.documents = json.dumps(docs_list)
        
        db.add(profile)
    else:
        for k, v in update_data.items():
            # Handle list fields that need serialization to JSON string for Text columns
            if k == 'services' and isinstance(v, list):
                # Convert Enums to string values
                serialized = json.dumps([s.value if hasattr(s, 'value') else s for s in v])
                setattr(profile, k, serialized)
            elif k == 'documents' and isinstance(v, list):
                setattr(profile, k, json.dumps(v))
            else:
                setattr(profile, k, v)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/nearby/{latitude}/{longitude}", response_model=List[ServiceProviderPublicResponse])
async def get_nearby_service_providers(
    latitude: float,
    longitude: float,
    radius: float = 50.0,  # kilometers
    service_type: str = None,
    db: Session = Depends(get_db)
):
    """Get verified service providers near a specific location, sorted by distance."""
    # ONLY get verified, active, and online providers
    providers = db.query(ServiceProvider).join(User).filter(
        ServiceProvider.is_active == True,
        ServiceProvider.is_online == True,
        ServiceProvider.is_verified == True  # ONLY VERIFIED PROVIDERS
    ).all()
    
    # Filter by distance and service type
    nearby_providers = []
    for provider in providers:
        # Simple distance calculation
        distance = ((provider.latitude - latitude) ** 2 + (provider.longitude - longitude) ** 2) ** 0.5
        # 1 degree lat approx 111km
        dist_km = distance * 111.0
        
        if dist_km <= radius:
            if not service_type or service_type in provider.services:
                # Create public response with user details
                entry = ServiceProviderPublicResponse.from_orm(provider)
                entry.first_name = provider.user.first_name
                entry.last_name = provider.user.last_name
                entry.phone = provider.user.phone
                entry.distance = round(dist_km, 1)
                nearby_providers.append(entry)
    
    # Sort by distance (nearest first)
    nearby_providers.sort(key=lambda p: p.distance)
    
    return nearby_providers

@router.get("/earnings", response_model=EarningsResponse)
async def get_provider_earnings(
    current_user: User = Depends(require_service_provider),
    db: Session = Depends(get_db)
):
    """Get service provider earnings (Dummy Data)."""
    # In a real app, this would aggregate from the database based on completed jobs
    
    return {
        "today": 850.0,
        "this_week": 3250.0,
        "this_month": 12400.0,
        "total": 45600.0,
        "transactions": [
            {
                "id": 1,
                "job": "Tire Replacement",
                "customer": "John Doe",
                "amount": 500.0,
                "date": "2024-12-04",
                "status": "paid"
            },
            {
                "id": 2,
                "job": "Battery Service",
                "customer": "Jane Smith",
                "amount": 400.0,
                "date": "2024-12-03",
                "status": "paid"
            },
            {
                "id": 3,
                "job": "Towing",
                "customer": "Bob Wilson",
                "amount": 1200.0,
                "date": "2024-12-03",
                "status": "pending"
            },
            {
                "id": 4,
                "job": "Oil Change",
                "customer": "Alice Brown",
                "amount": 300.0,
                "date": "2024-12-02",
                "status": "paid"
            }
        ]
    }

@router.get("/", response_model=List[ServiceProviderAdminDetail])
async def get_all_service_providers(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all service providers (Admin only)."""
    providers = db.query(ServiceProvider).all()
    return providers

@router.put("/{user_id}/approve", response_model=MessageResponse)
async def approve_service_provider(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Approve a service provider and ensure profile exists."""
    user = db.query(User).filter(User.id == user_id, User.role == "service_provider").first()
    if not user:
        raise HTTPException(status_code=404, detail="Service provider user not found")
    
    # 1. Verify User
    user.is_verified = True
    
    # 2. Check/Create Profile
    profile = db.query(ServiceProvider).filter(ServiceProvider.user_id == user.id).first()
    if not profile:
        profile = ServiceProvider(
            user_id=user.id,
            business_name=user.first_name, # Fallback
            business_license=f"LIC-{user.id}-{int(datetime.utcnow().timestamp())}",
            latitude=user.latitude or 0.0,
            longitude=user.longitude or 0.0,
            base_rate=500.0,
            is_verified=True,
            is_active=True
        )
        db.add(profile)
    else:
        profile.is_verified = True
        profile.is_active = True
        
    db.commit()
    return MessageResponse(message="Service Provider approved successfully")

@router.put("/{user_id}/suspend", response_model=MessageResponse)
async def suspend_service_provider(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Suspend a service provider."""
    user = db.query(User).filter(User.id == user_id, User.role == "service_provider").first()
    if not user:
        raise HTTPException(status_code=404, detail="Service provider user not found")
    
    profile = db.query(ServiceProvider).filter(ServiceProvider.user_id == user.id).first()
    
    # Suspend user account
    user.is_active = False
    user.is_verified = False
    
    # Suspend provider profile
    if profile:
        profile.is_active = False
        profile.is_verified = False
        profile.is_online = False
        
    db.commit()
    return MessageResponse(message="Service Provider suspended successfully")

@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_service_provider(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a service provider and their profile."""
    user = db.query(User).filter(User.id == user_id, User.role == "service_provider").first()
    if not user:
        raise HTTPException(status_code=404, detail="Service provider user not found")
    
    # Delete provider profile first (foreign key)
    profile = db.query(ServiceProvider).filter(ServiceProvider.user_id == user.id).first()
    if profile:
        db.delete(profile)
    
    # Delete user
    db.delete(user)
    db.commit()
    
    return MessageResponse(message="Service Provider deleted successfully")
