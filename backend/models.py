from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(str, enum.Enum):
    DRIVER = "driver"
    SERVICE_PROVIDER = "service_provider"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    # Use Integer for SQLite compatibility (unsigned attribute ignored by SQLite)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.DRIVER)
    is_verified = Column(Boolean, default=False)
    profile_image = Column(String(255), default="")
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    vehicles = relationship("Vehicle", back_populates="owner")
    breakdowns = relationship("Breakdown", back_populates="driver", foreign_keys="Breakdown.driver_id")
    service_provider_profile = relationship("ServiceProvider", back_populates="user", uselist=False)

class VehicleType(str, enum.Enum):
    CAR = "car"
    TRUCK = "truck"
    MOTORCYCLE = "motorcycle"
    BUS = "bus"
    VAN = "van"

class FuelType(str, enum.Enum):
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    LPG = "lpg"

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String(20), unique=True, index=True, nullable=False)
    vin = Column(String(17), unique=True, index=True, nullable=False)
    color = Column(String(30), nullable=False)
    vehicle_type = Column(SQLEnum(VehicleType), nullable=False)
    fuel_type = Column(SQLEnum(FuelType), nullable=False)
    mileage = Column(Integer, default=0)
    last_service_date = Column(DateTime(timezone=True), default=func.now())
    next_service_due = Column(DateTime(timezone=True))
    insurance_provider = Column(String(100))
    insurance_policy_number = Column(String(50))
    insurance_expiry_date = Column(DateTime(timezone=True))
    iot_device_id = Column(String(50), unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="vehicles")
    breakdowns = relationship("Breakdown", back_populates="vehicle")

class BreakdownCategory(str, enum.Enum):
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    TIRE = "tire"
    FUEL = "fuel"
    ACCIDENT = "accident"
    OTHER = "other"

class BreakdownSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BreakdownStatus(str, enum.Enum):
    REPORTED = "reported"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Breakdown(Base):
    __tablename__ = "breakdowns"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(BreakdownCategory), nullable=False)
    severity = Column(SQLEnum(BreakdownSeverity), default=BreakdownSeverity.MEDIUM)
    status = Column(SQLEnum(BreakdownStatus), default=BreakdownStatus.REPORTED)
    estimated_cost = Column(Float, default=0.0)
    actual_cost = Column(Float, default=0.0)
    service_provider_id = Column(Integer, ForeignKey("users.id"))
    estimated_arrival_time = Column(DateTime(timezone=True))
    actual_arrival_time = Column(DateTime(timezone=True))
    estimated_completion_time = Column(DateTime(timezone=True))
    actual_completion_time = Column(DateTime(timezone=True))
    rating = Column(Integer)
    feedback = Column(Text)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="breakdowns")
    driver = relationship("User", back_populates="breakdowns", foreign_keys=[driver_id])
    service_provider = relationship("User", foreign_keys=[service_provider_id])

class ServiceType(str, enum.Enum):
    TOWING = "towing"
    REPAIR = "repair"
    FUEL_DELIVERY = "fuel_delivery"
    JUMP_START = "jump_start"
    TIRE_CHANGE = "tire_change"
    LOCKOUT = "lockout"
    DIAGNOSTIC = "diagnostic"

class ServiceProvider(Base):
    __tablename__ = "service_providers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    business_name = Column(String(100), nullable=False)
    business_license = Column(String(50), unique=True, nullable=False)
    services = Column(Text)  # JSON string of service types
    documents = Column(Text) # JSON string of uploaded documents
    service_radius = Column(Integer, default=50)  # kilometers
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    base_rate = Column(Float, nullable=False)
    per_km_rate = Column(Float, default=0.0)
    hourly_rate = Column(Float, default=0.0)
    average_rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_online = Column(Boolean, default=False)
    current_latitude = Column(Float)
    current_longitude = Column(Float)
    last_location_update = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="service_provider_profile")

class AssistanceRequestStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class AssistanceRequest(Base):
    __tablename__ = "assistance_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    breakdown_id = Column(Integer, ForeignKey("breakdowns.id"), nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_type = Column(SQLEnum(ServiceType), nullable=False)
    priority = Column(String(20), default="medium")
    status = Column(SQLEnum(AssistanceRequestStatus), default=AssistanceRequestStatus.PENDING)
    assigned_provider_id = Column(Integer, ForeignKey("users.id"))
    estimated_cost = Column(Float, default=0.0)
    actual_cost = Column(Float, default=0.0)
    estimated_arrival_time = Column(DateTime(timezone=True))
    actual_arrival_time = Column(DateTime(timezone=True))
    estimated_completion_time = Column(DateTime(timezone=True))
    actual_completion_time = Column(DateTime(timezone=True))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(255))
    special_instructions = Column(Text)
    contact_phone = Column(String(20))
    emergency_contact_name = Column(String(100))
    emergency_contact_phone = Column(String(20))
    emergency_contact_relationship = Column(String(50))
    payment_status = Column(String(20), default="pending")
    payment_method = Column(String(20))
    rating = Column(Integer)
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    breakdown = relationship("Breakdown")
    requester = relationship("User", foreign_keys=[requester_id])
    assigned_provider = relationship("User", foreign_keys=[assigned_provider_id])
