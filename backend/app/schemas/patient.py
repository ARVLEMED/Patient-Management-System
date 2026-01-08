from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ============= REGISTRY PATIENT DATA (FROM CENTRAL REGISTRY) =============

class AddressData(BaseModel):
    """Address information from registry"""
    county: str
    sub_county: str
    ward: str


class EmergencyContactData(BaseModel):
    """Emergency contact information from registry"""
    name: str
    relationship: str
    phone: str


class RegistryPatientResponse(BaseModel):
    """Patient data from central registry"""
    patient_id: str
    national_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    phone: str
    email: str
    address: AddressData
    emergency_contact: EmergencyContactData
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "PAT-123456",
                "national_id": "12345678",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-05-15",
                "gender": "male",
                "phone": "+254712345678",
                "email": "john.doe@example.com",
                "address": {
                    "county": "Nairobi",
                    "sub_county": "Westlands",
                    "ward": "Parklands"
                },
                "emergency_contact": {
                    "name": "Jane Doe",
                    "relationship": "Spouse",
                    "phone": "+254787654321"
                }
            }
        }


# ============= LOCAL PATIENT DATA =============

class PatientResponse(BaseModel):
    """Local patient information"""
    patient_id: str
    user_id: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class PatientSearchRequest(BaseModel):
    """Schema for searching patient by national ID"""
    national_id: str = Field(..., min_length=8, max_length=20, description="Patient's National ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "national_id": "12345678"
            }
        }


class PatientDetailResponse(BaseModel):
    """Detailed patient information (requires consent)"""
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    phone: str
    email: str
    address: AddressData
    emergency_contact: EmergencyContactData
    access_granted_at: datetime
    consent_type: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "PAT-123456",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-05-15",
                "gender": "male",
                "phone": "+254712345678",
                "email": "john.doe@example.com",
                "address": {
                    "county": "Nairobi",
                    "sub_county": "Westlands",
                    "ward": "Parklands"
                },
                "emergency_contact": {
                    "name": "Jane Doe",
                    "relationship": "Spouse",
                    "phone": "+254787654321"
                },
                "access_granted_at": "2024-01-20T10:30:00",
                "consent_type": "view"
            }
        }