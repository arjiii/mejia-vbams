from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import User, Vehicle, Breakdown, BreakdownStatus
from schemas import (
    BreakdownCreate, 
    BreakdownResponse, 
    BreakdownUpdate,
    MessageResponse
)
from auth import get_current_user, require_driver

router = APIRouter()

@router.post("/", response_model=BreakdownResponse, status_code=status.HTTP_201_CREATED)
async def report_breakdown(
    breakdown_data: BreakdownCreate,
    current_user: User = Depends(require_driver),
    db: Session = Depends(get_db)
):
    """Report a new vehicle breakdown."""
    # Verify vehicle belongs to user
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == breakdown_data.vehicle_id,
        Vehicle.owner_id == current_user.id,
        Vehicle.is_active == True
    ).first()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found or does not belong to you"
        )
    
    try:
        # Create new breakdown report
        # Convert Pydantic data to dict and handle Enums if necessary
        data = breakdown_data.dict()
        # Ensure Enums are stored as values (strings) to avoid type mismatch between schema/model Enums
        if hasattr(data.get('category'), 'value'):
            data['category'] = data['category'].value
        if hasattr(data.get('severity'), 'value'):
            data['severity'] = data['severity'].value
            
        # Add driver_id to data (not in BreakdownCreate schema)
        data['driver_id'] = current_user.id
        
        # Create breakdown with all data
        db_breakdown = Breakdown(**data)
        
        db.add(db_breakdown)
        db.commit()
        db.refresh(db_breakdown)
        
        return BreakdownResponse.from_orm(db_breakdown)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating breakdown: {str(e)}"
        )

@router.get("/", response_model=List[BreakdownResponse])
async def get_user_breakdowns(
    current_user: User = Depends(require_driver),
    db: Session = Depends(get_db)
):
    """Get all breakdowns reported by the current user."""
    breakdowns = db.query(Breakdown).filter(
        Breakdown.driver_id == current_user.id
    ).order_by(Breakdown.created_at.desc()).all()
    
    return [BreakdownResponse.from_orm(breakdown) for breakdown in breakdowns]

@router.get("/{breakdown_id}", response_model=BreakdownResponse)
async def get_breakdown(
    breakdown_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific breakdown by ID."""
    breakdown = db.query(Breakdown).filter(
        Breakdown.id == breakdown_id
    ).first()
    
    if not breakdown:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breakdown not found"
        )
    
    # Check if user has access to this breakdown
    if (current_user.role == "driver" and breakdown.driver_id != current_user.id) and \
       (current_user.role == "service_provider" and breakdown.service_provider_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this breakdown"
        )
    
    return BreakdownResponse.from_orm(breakdown)

@router.put("/{breakdown_id}", response_model=BreakdownResponse)
async def update_breakdown(
    breakdown_id: int,
    breakdown_data: BreakdownUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update breakdown information."""
    breakdown = db.query(Breakdown).filter(
        Breakdown.id == breakdown_id
    ).first()
    
    if not breakdown:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breakdown not found"
        )
    
    # Check if user has permission to update this breakdown
    if (current_user.role == "driver" and breakdown.driver_id != current_user.id) and \
       (current_user.role == "service_provider" and breakdown.service_provider_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this breakdown"
        )
    
    # Update breakdown
    update_data = breakdown_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(breakdown, field, value)
    
    db.commit()
    db.refresh(breakdown)
    
    return BreakdownResponse.from_orm(breakdown)

@router.put("/{breakdown_id}/status", response_model=BreakdownResponse)
async def update_breakdown_status(
    breakdown_id: int,
    status_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update breakdown status."""
    breakdown = db.query(Breakdown).filter(
        Breakdown.id == breakdown_id
    ).first()
    
    if not breakdown:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breakdown not found"
        )
    
    # Check if user has permission to update status
    if (current_user.role == "driver" and breakdown.driver_id != current_user.id) and \
       (current_user.role == "service_provider" and breakdown.service_provider_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this breakdown"
        )
    
    new_status = status_data.get("status")
    if new_status not in [status.value for status in BreakdownStatus]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status"
        )
    
    breakdown.status = new_status
    
    # Update timestamps based on status
    if new_status == BreakdownStatus.IN_PROGRESS.value:
        breakdown.actual_arrival_time = datetime.utcnow()
    elif new_status == BreakdownStatus.COMPLETED.value:
        breakdown.actual_completion_time = datetime.utcnow()
        breakdown.is_resolved = True
    
    db.commit()
    db.refresh(breakdown)
    
    return BreakdownResponse.from_orm(breakdown)

@router.get("/nearby/{latitude}/{longitude}", response_model=List[BreakdownResponse])
async def get_nearby_breakdowns(
    latitude: float,
    longitude: float,
    radius: float = 10.0,  # kilometers
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get breakdowns near a specific location."""
    # This would require PostGIS or similar for proper geospatial queries
    # For now, we'll use a simple bounding box approximation
    breakdowns = db.query(Breakdown).filter(
        Breakdown.status.in_([BreakdownStatus.REPORTED.value, BreakdownStatus.ASSIGNED.value])
    ).all()
    
    # Filter by distance (simplified - in production, use proper geospatial queries)
    nearby_breakdowns = []
    for breakdown in breakdowns:
        # Simple distance calculation (not accurate for large distances)
        distance = ((breakdown.latitude - latitude) ** 2 + (breakdown.longitude - longitude) ** 2) ** 0.5
        if distance <= radius / 111.0:  # Rough conversion: 1 degree ≈ 111 km
            nearby_breakdowns.append(breakdown)
    
    return [BreakdownResponse.from_orm(breakdown) for breakdown in nearby_breakdowns]

@router.delete("/{breakdown_id}", response_model=MessageResponse)
async def delete_breakdown(
    breakdown_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a breakdown report."""
    breakdown = db.query(Breakdown).filter(
        Breakdown.id == breakdown_id
    ).first()
    
    if not breakdown:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breakdown not found"
        )
    
    # Check if user has permission to delete
    if current_user.role == "driver" and breakdown.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this breakdown"
        )
    
    db.delete(breakdown)
    db.commit()
    
    return MessageResponse(message="Breakdown deleted successfully")
