from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, ServiceProvider
from schemas import (
    ServiceProviderCreate, 
    ServiceProviderResponse, 
    ServiceProviderUpdate,
    ServiceProviderLocationUpdate,
    MessageResponse
)
from auth import get_current_user, require_service_provider

router = APIRouter()

@router.post("/register", response_model=ServiceProviderResponse, status_code=status.HTTP_201_CREATED)
async def register_service_provider(
    provider_data: ServiceProviderCreate,
    current_user: User = Depends(require_service_provider),
    db: Session = Depends(get_db)
):
    """Register as a service provider."""
    # Check if user already has a service provider profile
    existing_provider = db.query(ServiceProvider).filter(
        ServiceProvider.user_id == current_user.id
    ).first()
    
    if existing_provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service provider profile already exists"
        )
    
    # Check if business license already exists
    existing_license = db.query(ServiceProvider).filter(
        ServiceProvider.business_license == provider_data.business_license
    ).first()
    
    if existing_license:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Business license already registered"
        )
    
    # Create service provider profile
    db_provider = ServiceProvider(
        user_id=current_user.id,
        **provider_data.dict()
    )
    
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    
    return ServiceProviderResponse.from_orm(db_provider)

@router.get("/profile", response_model=ServiceProviderResponse)
async def get_service_provider_profile(
    current_user: User = Depends(require_service_provider),
    db: Session = Depends(get_db)
):
    """Get current user's service provider profile."""
    provider = db.query(ServiceProvider).filter(
        ServiceProvider.user_id == current_user.id
    ).first()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service provider profile not found"
        )
    
    return ServiceProviderResponse.from_orm(provider)

@router.put("/profile", response_model=ServiceProviderResponse)
async def update_service_provider_profile(
    provider_data: ServiceProviderUpdate,
    current_user: User = Depends(require_service_provider),
    db: Session = Depends(get_db)
):
    """Update service provider profile."""
    provider = db.query(ServiceProvider).filter(
        ServiceProvider.user_id == current_user.id
    ).first()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service provider profile not found"
        )
    
    # Update provider
    update_data = provider_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(provider, field, value)
    
    db.commit()
    db.refresh(provider)
    
    return ServiceProviderResponse.from_orm(provider)

@router.put("/location", response_model=MessageResponse)
async def update_service_provider_location(
    location_data: ServiceProviderLocationUpdate,
    current_user: User = Depends(require_service_provider),
    db: Session = Depends(get_db)
):
    """Update service provider's current location."""
    provider = db.query(ServiceProvider).filter(
        ServiceProvider.user_id == current_user.id
    ).first()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service provider profile not found"
        )
    
    provider.current_latitude = location_data.latitude
    provider.current_longitude = location_data.longitude
    provider.last_location_update = datetime.utcnow()
    
    db.commit()
    
    return MessageResponse(message="Location updated successfully")

@router.put("/online-status", response_model=MessageResponse)
async def update_online_status(
    status_data: dict,
    current_user: User = Depends(require_service_provider),
    db: Session = Depends(get_db)
):
    """Update service provider's online status."""
    provider = db.query(ServiceProvider).filter(
        ServiceProvider.user_id == current_user.id
    ).first()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service provider profile not found"
        )
    
    is_online = status_data.get("is_online", False)
    provider.is_online = is_online
    
    db.commit()
    
    return MessageResponse(message=f"Status updated to {'online' if is_online else 'offline'}")

@router.get("/nearby/{latitude}/{longitude}", response_model=List[ServiceProviderResponse])
async def get_nearby_service_providers(
    latitude: float,
    longitude: float,
    radius: float = 50.0,  # kilometers
    service_type: str = None,
    db: Session = Depends(get_db)
):
    """Get service providers near a specific location."""
    providers = db.query(ServiceProvider).filter(
        ServiceProvider.is_active == True,
        ServiceProvider.is_online == True
    ).all()
    
    # Filter by distance and service type
    nearby_providers = []
    for provider in providers:
        # Simple distance calculation
        distance = ((provider.latitude - latitude) ** 2 + (provider.longitude - longitude) ** 2) ** 0.5
        if distance <= radius / 111.0:  # Rough conversion: 1 degree ≈ 111 km
            if not service_type or service_type in provider.services:
                nearby_providers.append(provider)
    
    return [ServiceProviderResponse.from_orm(provider) for provider in nearby_providers]
