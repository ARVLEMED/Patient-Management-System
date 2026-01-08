from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration"""
    PATIENT = "patient"
    HEALTHCARE_WORKER = "healthcare_worker"
    ADMIN = "admin"


# ============= REQUEST SCHEMAS =============

class UserRegisterRequest(BaseModel):
    """Schema for user registration"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password (min 8 characters, must contain uppercase, lowercase, and number)"
    )
    role: UserRole = Field(..., description="User role")
    
    # Additional fields based on role
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    national_id: Optional[str] = Field(None, min_length=8, max_length=20, description="Required for patients")
    date_of_birth: Optional[str] = Field(None, description="YYYY-MM-DD format, required for patients")
    
    # Healthcare worker specific fields
    facility_id: Optional[str] = Field(None, description="Required for healthcare workers")
    license_number: Optional[str] = Field(None, description="Required for healthcare workers")
    job_title: Optional[str] = Field(None, description="Required for healthcare workers")
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "patient@example.com",
                "password": "SecurePass123",
                "role": "patient",
                "first_name": "John",
                "last_name": "Doe",
                "national_id": "12345678",
                "date_of_birth": "1990-05-15"
            }
        }


class UserLoginRequest(BaseModel):
    """Schema for user login"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "patient@test.com",
                "password": "Test123!"
            }
        }


class RefreshTokenRequest(BaseModel):
    """Schema for token refresh"""
    refresh_token: str = Field(..., description="Refresh token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


# ============= RESPONSE SCHEMAS =============

class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(default=900, description="Token expiry in seconds (15 minutes)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 900
            }
        }


class UserResponse(BaseModel):
    """Schema for user information response"""
    user_id: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "patient@test.com",
                "role": "patient",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00",
                "last_login": "2024-01-20T14:25:00"
            }
        }


class PatientProfileResponse(BaseModel):
    """Schema for patient profile response"""
    patient_id: str
    user_id: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class HealthcareWorkerProfileResponse(BaseModel):
    """Schema for healthcare worker profile response"""
    worker_id: str
    user_id: str
    facility_id: str
    facility_name: Optional[str] = None
    license_number: str
    job_title: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    """Complete user profile response"""
    user: UserResponse
    patient: Optional[PatientProfileResponse] = None
    healthcare_worker: Optional[HealthcareWorkerProfileResponse] = None
    
    class Config:
        from_attributes = True