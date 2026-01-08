from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class FacilityType(str, Enum):
    """Facility type enumeration"""
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    PHARMACY = "pharmacy"


# ============= RESPONSE SCHEMAS =============

class FacilityResponse(BaseModel):
    """Schema for healthcare facility response"""
    facility_id: str
    name: str
    facility_type: FacilityType
    license_number: str
    location: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "facility_id": "FAC-123456",
                "name": "HealthHub Clinic",
                "facility_type": "clinic",
                "license_number": "HF-12345",
                "location": "Nairobi, Westlands",
                "created_at": "2024-01-01T00:00:00"
            }
        }


class FacilityListResponse(BaseModel):
    """Schema for listing facilities"""
    facilities: list[FacilityResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "facilities": [],
                "total": 0
            }
        }