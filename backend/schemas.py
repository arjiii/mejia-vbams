from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums
class UserRole(str, Enum):
    DRIVER = "driver"
    SERVICE_PROVIDER = "service_provider"
    ADMIN = "admin"

class VehicleType(str, Enum):
    CAR = "car"
    TRUCK = "truck"
    MOTORCYCLE = "motorcycle"
    BUS = "bus"
    VAN = "van"

class FuelType(str, Enum):
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    LPG = "lpg"

class BreakdownCategory(str, Enum):
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    TIRE = "tire"
    FUEL = "fuel"
    ACCIDENT = "accident"
    OTHER = "other"

class BreakdownSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BreakdownStatus(str, Enum):
    REPORTED = "reported"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ServiceType(str, Enum):
    TOWING = "towing"
    REPAIR = "repair"
    FUEL_DELIVERY = "fuel_delivery"
    JUMP_START = "jump_start"
    TIRE_CHANGE = "tire_change"
    LOCKOUT = "lockout"
    DIAGNOSTIC = "diagnostic"

# User Schemas
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role: UserRole = UserRole.DRIVER

class UserCreate(UserBase):
    password: str
    business_name: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_verified: bool
    profile_image: Optional[str]
    latitude: float
    longitude: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLocationUpdate(BaseModel):
    latitude: float
    longitude: float

# Vehicle Schemas
class VehicleBase(BaseModel):
    make: str
    model: str
    year: int
    license_plate: str
    vin: str
    color: str
    vehicle_type: VehicleType
    fuel_type: FuelType
    mileage: Optional[int] = 0
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    insurance_expiry_date: Optional[datetime] = None
    iot_device_id: Optional[str] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    license_plate: Optional[str] = None
    vin: Optional[str] = None
    color: Optional[str] = None
    vehicle_type: Optional[VehicleType] = None
    fuel_type: Optional[FuelType] = None
    mileage: Optional[int] = None
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    insurance_expiry_date: Optional[datetime] = None
    iot_device_id: Optional[str] = None

class VehicleResponse(VehicleBase):
    id: int
    owner_id: int
    last_service_date: datetime
    next_service_due: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class VehicleMileageUpdate(BaseModel):
    mileage: int
    
    @validator('mileage')
    def validate_mileage(cls, v):
        if v < 0:
            raise ValueError('Mileage must be a positive number')
        return v

# Breakdown Schemas
class BreakdownBase(BaseModel):
    vehicle_id: int
    latitude: float
    longitude: float
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    description: str
    category: BreakdownCategory
    severity: BreakdownSeverity = BreakdownSeverity.MEDIUM

class BreakdownCreate(BreakdownBase):
    pass

class BreakdownUpdate(BaseModel):
    description: Optional[str] = None
    category: Optional[BreakdownCategory] = None
    severity: Optional[BreakdownSeverity] = None
    status: Optional[BreakdownStatus] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    rating: Optional[int] = None
    feedback: Optional[str] = None

class BreakdownResponse(BreakdownBase):
    id: int
    driver_id: int
    status: BreakdownStatus
    estimated_cost: float
    actual_cost: float
    service_provider_id: Optional[int]
    estimated_arrival_time: Optional[datetime]
    actual_arrival_time: Optional[datetime]
    estimated_completion_time: Optional[datetime]
    actual_completion_time: Optional[datetime]
    rating: Optional[int]
    feedback: Optional[str]
    is_resolved: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Service Provider Schemas
class ServiceProviderBase(BaseModel):
    business_name: str
    business_license: str
    services: List[ServiceType]
    service_radius: int = 50
    latitude: float
    longitude: float
    base_rate: float
    per_km_rate: float = 0.0
    hourly_rate: float = 0.0
    documents: Optional[List[str]] = []

    @validator('services', 'documents', pre=True)
    def parse_json_fields(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except:
                return []
        return v

class ServiceProviderCreate(ServiceProviderBase):
    pass

class ServiceProviderUpdate(BaseModel):
    business_name: Optional[str] = None
    services: Optional[List[ServiceType]] = None
    documents: Optional[List[str]] = None
    service_radius: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    base_rate: Optional[float] = None
    per_km_rate: Optional[float] = None
    hourly_rate: Optional[float] = None
    is_online: Optional[bool] = None

class ServiceProviderResponse(ServiceProviderBase):
    id: int
    user_id: int
    average_rating: float
    rating_count: int
    is_verified: bool
    is_active: bool
    is_online: bool
    current_latitude: Optional[float]
    current_longitude: Optional[float]
    last_location_update: datetime
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ServiceProviderPublicResponse(ServiceProviderResponse):
    first_name: str
    last_name: str
    phone: str
    distance: float = 0.0

class ServiceProviderAdminDetail(ServiceProviderResponse):
    user: UserResponse

class ServiceProviderLocationUpdate(BaseModel):
    latitude: float
    longitude: float

# Assistance Request Schemas
class AssistanceRequestBase(BaseModel):
    breakdown_id: int
    service_type: ServiceType
    priority: str = "medium"
    latitude: float
    longitude: float
    address: Optional[str] = None
    special_instructions: Optional[str] = None
    contact_phone: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None

class AssistanceRequestCreate(AssistanceRequestBase):
    pass

class AssistanceRequestUpdate(BaseModel):
    status: Optional[str] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    estimated_arrival_time: Optional[datetime] = None
    actual_arrival_time: Optional[datetime] = None
    estimated_completion_time: Optional[datetime] = None
    actual_completion_time: Optional[datetime] = None
    payment_status: Optional[str] = None
    payment_method: Optional[str] = None
    rating: Optional[int] = None
    feedback: Optional[str] = None



class AssistanceRequestResponse(AssistanceRequestBase):
    id: int
    requester_id: int
    status: str
    assigned_provider_id: Optional[int]
    estimated_cost: float
    actual_cost: float
    estimated_arrival_time: Optional[datetime]
    actual_arrival_time: Optional[datetime]
    estimated_completion_time: Optional[datetime]
    actual_completion_time: Optional[datetime]
    payment_status: str
    payment_method: Optional[str]
    rating: Optional[int]
    feedback: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Response Schemas
class MessageResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str

# Earnings Schemas
class Transaction(BaseModel):
    id: int
    job: str
    customer: str
    amount: float
    date: str
    status: str

class EarningsResponse(BaseModel):
    today: float
    this_week: float
    this_month: float
    total: float
    transactions: List[Transaction]
