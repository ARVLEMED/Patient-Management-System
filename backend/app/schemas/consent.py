from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ConsentType(str, Enum):
    """Consent type enumeration"""
    VIEW = "view"
    EDIT = "edit"
    SHARE = "share"


class ConsentStatus(str, Enum):
    """Consent status enumeration"""
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


# ============= REQUEST SCHEMAS =============

class ConsentCreateRequest(BaseModel):
    """Schema for creating new consent"""
    facility_id: str = Field(..., description="Healthcare facility ID")
    consent_type: ConsentType = Field(..., description="Type of consent (view, edit, share)")
    purpose: str = Field(..., min_length=10, max_length=500, description="Purpose of consent")
    expires_at: Optional[datetime] = Field(None, description="Optional expiration date")
    
    class Config:
        json_schema_extra = {
            "example": {
                "facility_id": "FAC-123456",
                "consent_type": "view",
                "purpose": "To allow HealthHub Clinic to view my medical records for consultation",
                "expires_at": "2024-12-31T23:59:59"
            }
        }


class ConsentCheckRequest(BaseModel):
    """Schema for checking consent"""
    patient_id: str = Field(..., description="Patient ID")
    facility_id: str = Field(..., description="Healthcare facility ID")
    consent_type: ConsentType = Field(..., description="Required consent type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "PAT-123456",
                "facility_id": "FAC-123456",
                "consent_type": "view"
            }
        }


# ============= RESPONSE SCHEMAS =============

class ConsentResponse(BaseModel):
    """Schema for consent response"""
    consent_id: str
    patient_id: str
    facility_id: str
    facility_name: Optional[str] = None
    consent_type: ConsentType
    granted_at: datetime
    expires_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None
    purpose: str
    status: ConsentStatus
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "consent_id": "CON-123456",
                "patient_id": "PAT-123456",
                "facility_id": "FAC-123456",
                "facility_name": "HealthHub Clinic",
                "consent_type": "view",
                "granted_at": "2024-01-15T10:30:00",
                "expires_at": "2024-12-31T23:59:59",
                "revoked_at": None,
                "purpose": "To allow HealthHub Clinic to view my medical records",
                "status": "active"
            }
        }


class ConsentListResponse(BaseModel):
    """Schema for listing consents"""
    consents: list[ConsentResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "consents": [],
                "total": 0
            }
        }


class ConsentCheckResponse(BaseModel):
    """Schema for consent check response"""
    has_consent: bool
    consent_id: Optional[str] = None
    consent_type: Optional[ConsentType] = None
    status: Optional[ConsentStatus] = None
    expires_at: Optional[datetime] = None
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "has_consent": True,
                "consent_id": "CON-123456",
                "consent_type": "view",
                "status": "active",
                "expires_at": "2024-12-31T23:59:59",
                "message": "Active consent found"
            }
        }


class ConsentRevokeResponse(BaseModel):
    """Schema for consent revocation response"""
    consent_id: str
    revoked_at: datetime
    message: str = "Consent revoked successfully"
    
    class Config:
        json_schema_extra = {
            "example": {
                "consent_id": "CON-123456",
                "revoked_at": "2024-01-20T15:45:00",
                "message": "Consent revoked successfully"
            }
        }