from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, AssistanceRequest, Breakdown
from schemas import (
    AssistanceRequestCreate, 
    AssistanceRequestResponse, 
    AssistanceRequestUpdate,
    MessageResponse
)
from auth import get_current_user, require_driver, require_service_provider

router = APIRouter()

@router.post("/", response_model=AssistanceRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_assistance_request(
    request_data: AssistanceRequestCreate,
    current_user: User = Depends(require_driver),
    db: Session = Depends(get_db)
):
    """Create a new assistance request."""
    # Verify breakdown belongs to user
    breakdown = db.query(Breakdown).filter(
        Breakdown.id == request_data.breakdown_id,
        Breakdown.driver_id == current_user.id
    ).first()
    
    if not breakdown:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breakdown not found or does not belong to you"
        )
    
    # Create assistance request
    db_request = AssistanceRequest(
        requester_id=current_user.id,
        **request_data.dict()
    )
    
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    return AssistanceRequestResponse.from_orm(db_request)

@router.get("/", response_model=List[AssistanceRequestResponse])
async def get_assistance_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get assistance requests based on user role."""
    if current_user.role == "driver":
        requests = db.query(AssistanceRequest).filter(
            AssistanceRequest.requester_id == current_user.id
        ).order_by(AssistanceRequest.created_at.desc()).all()
    elif current_user.role == "service_provider":
        requests = db.query(AssistanceRequest).filter(
            AssistanceRequest.assigned_provider_id == current_user.id
        ).order_by(AssistanceRequest.created_at.desc()).all()
    else:
        requests = db.query(AssistanceRequest).order_by(
            AssistanceRequest.created_at.desc()
        ).all()
    
    return [AssistanceRequestResponse.from_orm(request) for request in requests]

@router.get("/available", response_model=List[AssistanceRequestResponse])
async def get_available_requests(
    current_user: User = Depends(require_service_provider),
    db: Session = Depends(get_db)
):
    """Get all pending assistance requests available for pickup."""
    requests = db.query(AssistanceRequest).filter(
        AssistanceRequest.status == "pending"
    ).order_by(AssistanceRequest.created_at.desc()).all()
    
    return [AssistanceRequestResponse.from_orm(request) for request in requests]

@router.get("/{request_id}", response_model=AssistanceRequestResponse)
async def get_assistance_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific assistance request."""
    request = db.query(AssistanceRequest).filter(
        AssistanceRequest.id == request_id
    ).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistance request not found"
        )
    
    # Check if user has access to this request
    if (current_user.role == "driver" and request.requester_id != current_user.id) and \
       (current_user.role == "service_provider" and request.assigned_provider_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this request"
        )
    
    return AssistanceRequestResponse.from_orm(request)

@router.put("/{request_id}", response_model=AssistanceRequestResponse)
async def update_assistance_request(
    request_id: int,
    request_data: AssistanceRequestUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update assistance request."""
    request = db.query(AssistanceRequest).filter(
        AssistanceRequest.id == request_id
    ).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistance request not found"
        )
    
    # Check if user has permission to update
    if (current_user.role == "driver" and request.requester_id != current_user.id) and \
       (current_user.role == "service_provider" and request.assigned_provider_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this request"
        )
    
    # Update request
    update_data = request_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(request, field, value)
    
    db.commit()
    db.refresh(request)
    
    return AssistanceRequestResponse.from_orm(request)

@router.put("/{request_id}/accept", response_model=AssistanceRequestResponse)
async def accept_assistance_request(
    request_id: int,
    current_user: User = Depends(require_service_provider),
    db: Session = Depends(get_db)
):
    """Accept an assistance request."""
    request = db.query(AssistanceRequest).filter(
        AssistanceRequest.id == request_id,
        AssistanceRequest.status == "pending"
    ).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistance request not found or already processed"
        )
    
    request.status = "accepted"
    request.assigned_provider_id = current_user.id
    
    # Update breakdown status
    breakdown = db.query(Breakdown).filter(
        Breakdown.id == request.breakdown_id
    ).first()
    if breakdown:
        breakdown.status = "assigned"
        breakdown.service_provider_id = current_user.id
    
    db.commit()
    db.refresh(request)
    
    return AssistanceRequestResponse.from_orm(request)

@router.put("/{request_id}/reject", response_model=AssistanceRequestResponse)
async def reject_assistance_request(
    request_id: int,
    current_user: User = Depends(require_service_provider),
    db: Session = Depends(get_db)
):
    """Reject an assistance request."""
    request = db.query(AssistanceRequest).filter(
        AssistanceRequest.id == request_id,
        AssistanceRequest.status == "pending"
    ).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistance request not found or already processed"
        )
    
    request.status = "rejected"
    
    db.commit()
    db.refresh(request)
    
    return AssistanceRequestResponse.from_orm(request)

@router.put("/{request_id}/complete", response_model=AssistanceRequestResponse)
async def complete_assistance_request(
    request_id: int,
    completion_data: dict,
    current_user: User = Depends(require_service_provider),
    db: Session = Depends(get_db)
):
    """Mark assistance request as completed."""
    request = db.query(AssistanceRequest).filter(
        AssistanceRequest.id == request_id,
        AssistanceRequest.assigned_provider_id == current_user.id
    ).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistance request not found or not assigned to you"
        )
    
    request.status = "completed"
    request.actual_completion_time = datetime.utcnow()
    
    if "actual_cost" in completion_data:
        request.actual_cost = completion_data["actual_cost"]
    
    if "feedback" in completion_data:
        request.feedback = completion_data["feedback"]
    
    # Update breakdown status
    breakdown = db.query(Breakdown).filter(
        Breakdown.id == request.breakdown_id
    ).first()
    if breakdown:
        breakdown.status = "completed"
        breakdown.actual_completion_time = datetime.utcnow()
        breakdown.is_resolved = True
    
    db.commit()
    db.refresh(request)
    
    return AssistanceRequestResponse.from_orm(request)
