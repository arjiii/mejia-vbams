from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from models import User
from schemas import UserCreate, UserResponse, LoginRequest, Token, UserLocationUpdate, MessageResponse
from auth import get_password_hash, verify_password, create_access_token

import os

# Get config from env
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Import the proper get_current_user from auth module
from auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create a new user instance
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        phone=user_data.phone,
        role=user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse.from_orm(new_user)

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login a user and return a JWT token."""
    try:
        print(f"[LOGIN] Attempting login for: {login_data.email}")
        
        db_user = db.query(User).filter(User.email == login_data.email).first()
        print(f"[LOGIN] User found: {db_user is not None}")
        
        if not db_user:
            print(f"[LOGIN] User not found: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials"
            )
        
        hashed_pw = db_user.hashed_password
        if not isinstance(hashed_pw, str):
            hashed_pw = str(hashed_pw)
        
        print(f"[LOGIN] Verifying password...")
        if not verify_password(login_data.password, hashed_pw):
            print(f"[LOGIN] Password verification failed")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials"
            )

        print(f"[LOGIN] Creating access token...")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )
        
        print(f"[LOGIN] Login successful for: {login_data.email}")
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[LOGIN ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse.from_orm(current_user)

@router.put("/update-location", response_model=MessageResponse)
async def update_user_location(
    location_data: UserLocationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's current location."""
    setattr(current_user, 'latitude', location_data.latitude)
    setattr(current_user, 'longitude', location_data.longitude)
    db.commit()
    db.refresh(current_user)
    return MessageResponse(message="Location updated successfully")

@router.post("/logout", response_model=MessageResponse)
async def logout():
    """Logout user (client-side token removal)."""
    return MessageResponse(message="Logged out successfully")
