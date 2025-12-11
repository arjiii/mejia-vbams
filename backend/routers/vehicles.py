from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, Vehicle
from schemas import (
    VehicleCreate, 
    VehicleResponse, 
    VehicleUpdate, 
    VehicleMileageUpdate,
    MessageResponse
)
from auth import get_current_user, require_driver

router = APIRouter()

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    current_user: User = Depends(require_driver),
    db: Session = Depends(get_db)
):
    """Register a new vehicle."""
    # Check if license plate already exists
    existing_vehicle = db.query(Vehicle).filter(
        Vehicle.license_plate == vehicle_data.license_plate
    ).first()
    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle with this license plate already exists"
        )
    
    # Check if VIN already exists
    existing_vin = db.query(Vehicle).filter(Vehicle.vin == vehicle_data.vin).first()
    if existing_vin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle with this VIN already exists"
        )
    
    # Create new vehicle
    db_vehicle = Vehicle(
        owner_id=current_user.id,
        **vehicle_data.dict()
    )
    
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    
    return VehicleResponse.from_orm(db_vehicle)

@router.get("/", response_model=List[VehicleResponse])
async def get_user_vehicles(
    current_user: User = Depends(require_driver),
    db: Session = Depends(get_db)
):
    """Get all vehicles owned by the current user."""
    vehicles = db.query(Vehicle).filter(
        Vehicle.owner_id == current_user.id,
        Vehicle.is_active == True
    ).all()
    
    return [VehicleResponse.from_orm(vehicle) for vehicle in vehicles]

@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    current_user: User = Depends(require_driver),
    db: Session = Depends(get_db)
):
    """Get a specific vehicle by ID."""
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.owner_id == current_user.id,
        Vehicle.is_active == True
    ).first()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    return VehicleResponse.from_orm(vehicle)

@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    current_user: User = Depends(require_driver),
    db: Session = Depends(get_db)
):
    """Update vehicle information."""
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.owner_id == current_user.id,
        Vehicle.is_active == True
    ).first()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Check for duplicate license plate if being updated
    if vehicle_data.license_plate and vehicle_data.license_plate != vehicle.license_plate:
        existing_vehicle = db.query(Vehicle).filter(
            Vehicle.license_plate == vehicle_data.license_plate,
            Vehicle.id != vehicle_id
        ).first()
        if existing_vehicle:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle with this license plate already exists"
            )
    
    # Check for duplicate VIN if being updated
    if vehicle_data.vin and vehicle_data.vin != vehicle.vin:
        existing_vin = db.query(Vehicle).filter(
            Vehicle.vin == vehicle_data.vin,
            Vehicle.id != vehicle_id
        ).first()
        if existing_vin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle with this VIN already exists"
            )
    
    # Update vehicle
    update_data = vehicle_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vehicle, field, value)
    
    db.commit()
    db.refresh(vehicle)
    
    return VehicleResponse.from_orm(vehicle)

@router.delete("/{vehicle_id}", response_model=MessageResponse)
async def delete_vehicle(
    vehicle_id: int,
    current_user: User = Depends(require_driver),
    db: Session = Depends(get_db)
):
    """Delete a vehicle (soft delete)."""
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.owner_id == current_user.id,
        Vehicle.is_active == True
    ).first()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    vehicle.is_active = False
    db.commit()
    
    return MessageResponse(message="Vehicle deleted successfully")

@router.put("/{vehicle_id}/mileage", response_model=VehicleResponse)
async def update_vehicle_mileage(
    vehicle_id: int,
    mileage_data: VehicleMileageUpdate,
    current_user: User = Depends(require_driver),
    db: Session = Depends(get_db)
):
    """Update vehicle mileage."""
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.owner_id == current_user.id,
        Vehicle.is_active == True
    ).first()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    vehicle.mileage = mileage_data.mileage
    db.commit()
    db.refresh(vehicle)
    
    return VehicleResponse.from_orm(vehicle)
