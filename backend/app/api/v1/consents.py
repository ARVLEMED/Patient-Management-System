from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.core.database import get_db
from app.models.models import User, Patient, HealthcareWorker, ConsentStatus
from app.schemas.consent import (
    ConsentCreateRequest,
    ConsentResponse,
    ConsentListResponse,
    ConsentCheckRequest,
    ConsentCheckResponse,
    ConsentRevokeResponse
)
from app.services.consent_service import ConsentService
from app.api.dependencies import get_current_user, get_current_patient, get_current_healthcare_worker

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=ConsentResponse, status_code=status.HTTP_201_CREATED)
async def grant_consent(
    consent_data: ConsentCreateRequest,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    Grant new consent to a healthcare facility
    
    **Patient role required**
    
    - **facility_id**: Healthcare facility ID
    - **consent_type**: Type of consent (view, edit, share)
    - **purpose**: Purpose of granting consent
    - **expires_at**: Optional expiration date
    """
    try:
        # Grant consent
        consent = ConsentService.grant_consent(
            db=db,
            patient_id=current_patient.patient_id,
            facility_id=consent_data.facility_id,
            consent_type=consent_data.consent_type,
            purpose=consent_data.purpose,
            granted_by=current_patient.user_id,
            expires_at=consent_data.expires_at
        )
        
        # Get facility name
        facility_name = consent.facility.name if consent.facility else None
        
        return ConsentResponse(
            consent_id=consent.consent_id,
            patient_id=consent.patient_id,
            facility_id=consent.facility_id,
            facility_name=facility_name,
            consent_type=consent.consent_type,
            granted_at=consent.granted_at,
            expires_at=consent.expires_at,
            revoked_at=consent.revoked_at,
            purpose=consent.purpose,
            status=consent.status
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error granting consent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error granting consent"
        )


@router.get("/patient/{patient_id}", response_model=ConsentListResponse)
async def get_patient_consents(
    patient_id: str,
    status_filter: Optional[ConsentStatus] = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all consents for a patient
    
    **Patient can view their own consents, healthcare workers can view if they have consent, admins can view all**
    
    - **patient_id**: Patient ID
    - **status**: Optional filter by status (active, expired, revoked)
    """
    # Authorization check
    if current_user.role.value == "patient":
        # Patient can only view their own consents
        patient = db.query(Patient).filter(Patient.user_id == current_user.user_id).first()
        if not patient or patient.patient_id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view these consents"
            )
    elif current_user.role.value == "healthcare_worker":
        # Healthcare worker can view if they have active consent
        worker = db.query(HealthcareWorker).filter(
            HealthcareWorker.user_id == current_user.user_id
        ).first()
        if not worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Healthcare worker profile not found"
            )
        
        # Check if worker's facility has consent
        consent_check = ConsentService.check_consent(
            db=db,
            patient_id=patient_id,
            facility_id=worker.facility_id,
            consent_type="view"
        )
        
        if not consent_check.has_consent and current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No active consent to view patient consents"
            )
    
    # Get consents
    consents = ConsentService.get_patient_consents(
        db=db,
        patient_id=patient_id,
        status=status_filter
    )
    
    # Format response
    consent_responses = []
    for consent in consents:
        facility_name = consent.facility.name if consent.facility else None
        consent_responses.append(
            ConsentResponse(
                consent_id=consent.consent_id,
                patient_id=consent.patient_id,
                facility_id=consent.facility_id,
                facility_name=facility_name,
                consent_type=consent.consent_type,
                granted_at=consent.granted_at,
                expires_at=consent.expires_at,
                revoked_at=consent.revoked_at,
                purpose=consent.purpose,
                status=consent.status
            )
        )
    
    return ConsentListResponse(
        consents=consent_responses,
        total=len(consent_responses)
    )


@router.patch("/{consent_id}/revoke", response_model=ConsentRevokeResponse)
async def revoke_consent(
    consent_id: str,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    Revoke a consent
    
    **Patient role required**
    
    - **consent_id**: Consent ID to revoke
    """
    try:
        consent = ConsentService.revoke_consent(
            db=db,
            consent_id=consent_id,
            patient_id=current_patient.patient_id
        )
        
        return ConsentRevokeResponse(
            consent_id=consent.consent_id,
            revoked_at=consent.revoked_at,
            message="Consent revoked successfully"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error revoking consent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error revoking consent"
        )


@router.post("/check", response_model=ConsentCheckResponse)
async def check_consent(
    check_data: ConsentCheckRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if consent exists between patient and facility
    
    **Healthcare worker or admin role required**
    
    - **patient_id**: Patient ID
    - **facility_id**: Facility ID
    - **consent_type**: Required consent type
    """
    # Authorization check - only healthcare workers and admins can check
    if current_user.role.value == "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients cannot use this endpoint"
        )
    
    # Check consent
    consent_check = ConsentService.check_consent(
        db=db,
        patient_id=check_data.patient_id,
        facility_id=check_data.facility_id,
        consent_type=check_data.consent_type
    )
    
    return consent_check


@router.get("/facility/{facility_id}", response_model=ConsentListResponse)
async def get_facility_consents(
    facility_id: str,
    status_filter: Optional[ConsentStatus] = Query(None, alias="status"),
    current_worker: HealthcareWorker = Depends(get_current_healthcare_worker),
    db: Session = Depends(get_db)
):
    """
    Get all consents for a facility
    
    **Healthcare worker role required (must be from the same facility)**
    
    - **facility_id**: Facility ID
    - **status**: Optional filter by status (active, expired, revoked)
    """
    # Authorization check - worker must be from the same facility
    if current_worker.facility_id != facility_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view consents for this facility"
        )
    
    # Get consents
    consents = ConsentService.get_facility_consents(
        db=db,
        facility_id=facility_id,
        status=status_filter
    )
    
    # Format response
    consent_responses = []
    for consent in consents:
        facility_name = consent.facility.name if consent.facility else None
        consent_responses.append(
            ConsentResponse(
                consent_id=consent.consent_id,
                patient_id=consent.patient_id,
                facility_id=consent.facility_id,
                facility_name=facility_name,
                consent_type=consent.consent_type,
                granted_at=consent.granted_at,
                expires_at=consent.expires_at,
                revoked_at=consent.revoked_at,
                purpose=consent.purpose,
                status=consent.status
            )
        )
    
    return ConsentListResponse(
        consents=consent_responses,
        total=len(consent_responses)
    )