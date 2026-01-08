from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class AccessResult(str, Enum):
    """Access result enumeration"""
    ALLOWED = "allowed"
    DENIED = "denied"


# ============= RESPONSE SCHEMAS =============

class AccessLogResponse(BaseModel):
    """Schema for access log response"""
    log_id: str
    patient_id: str
    patient_name: Optional[str] = None
    accessed_by: str
    worker_name: Optional[str] = None
    facility_id: str
    facility_name: Optional[str] = None
    action: str
    result: AccessResult
    reason: Optional[str] = None
    timestamp: datetime
    ip_address: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "log_id": "LOG-123456",
                "patient_id": "PAT-123456",
                "patient_name": "John Doe",
                "accessed_by": "WRK-123456",
                "worker_name": "Dr. James Smith",
                "facility_id": "FAC-123456",
                "facility_name": "HealthHub Clinic",
                "action": "view",
                "result": "allowed",
                "reason": None,
                "timestamp": "2024-01-20T10:30:00",
                "ip_address": "192.168.1.1"
            }
        }


class AccessLogListResponse(BaseModel):
    """Schema for listing access logs"""
    logs: list[AccessLogResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "logs": [],
                "total": 0
            }
        }


class AccessLogCreateRequest(BaseModel):
    """Internal schema for creating access logs"""
    patient_id: str
    accessed_by: str
    facility_id: str
    action: str
    result: AccessResult
    reason: Optional[str] = None
    ip_address: Optional[str] = None