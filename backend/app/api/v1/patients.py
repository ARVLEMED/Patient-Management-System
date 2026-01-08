from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
import httpx
import logging

from app.core.database import get_db
from app.core.config import settings
from app.core.security import decrypt_data
from app.models.models import Patient, HealthcareWorker, AccessResult, User
from app.schemas.patient import (
    PatientSearchRequest,
    RegistryPatientResponse,
    PatientDetailResponse,
    PatientResponse
)
from app.services.consent_service import ConsentService
from app.services.access_log_service import AccessLogService
from app.api.dependencies import (
    get_current_user,
    get_current_patient,
    get_current_healthcare_worker,
    get_client_ip
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/search", response_model=RegistryPatientResponse)
async def search_patient_by_national_id(
    national_id: str = Query(..., min_length=8, max_length=20),
    current_worker: HealthcareWorker = Depends(get_current_healthcare_worker),
    db: Session = Depends(get_db)
):
    """
    Search for patient in central registry by National ID
    
    **Healthcare worker role required**
    
    This endpoint only searches the registry, does not check consent.
    Use GET /patients/{patient_id} to access full patient data with consent validation.
    
    - **national_id**: Patient's National ID
    """
    try:
        # Call central registry
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.REGISTRY_API_URL}/api/registry/patients",
                params={"national_id": national_id},
                headers={"X-API-Key": settings.REGISTRY_API_KEY},
                timeout=10.0
            )
            
            if response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Patient not found in central registry"
                )
            
            response.raise_for_status()
            registry_data = response.json()
            
            logger.info(f"Patient search by worker {current_worker.worker_id}: National ID {national_id}")
            
            return RegistryPatientResponse(**registry_data)
    
    except httpx.HTTPError as e:
        logger.error(f"Registry API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Central registry service unavailable"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching patient: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error searching for patient"
        )


@router.get("/{patient_id}", response_model=PatientDetailResponse)
async def get_patient_data(
    patient_id: str,
    request: Request,
    current_worker: HealthcareWorker = Depends(get_current_healthcare_worker),
    db: Session = Depends(get_db)
):
    """
    Get detailed patient data (requires valid consent)
    
    **Healthcare worker role required**
    
    This endpoint validates consent before returning patient data and logs all access attempts.
    
    - **patient_id**: Patient ID from central registry
    """
    client_ip = get_client_ip(request)
    
    # Check if patient exists locally
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    
    if not patient:
        # Log denied access
        AccessLogService.log_access(
            db=db,
            patient_id=patient_id,
            accessed_by=current_worker.worker_id,
            facility_id=current_worker.facility_id,
            action="view",
            result=AccessResult.DENIED,
            reason="Patient not found in local system",
            ip_address=client_ip
        )
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found. Patient must register in the system first."
        )
    
    # Check consent
    consent_check = ConsentService.check_consent(
        db=db,
        patient_id=patient_id,
        facility_id=current_worker.facility_id,
        consent_type="view"
    )
    
    if not consent_check.has_consent:
        # Log denied access
        AccessLogService.log_access(
            db=db,
            patient_id=patient_id,
            accessed_by=current_worker.worker_id,
            facility_id=current_worker.facility_id,
            action="view",
            result=AccessResult.DENIED,
            reason=consent_check.message,
            ip_address=client_ip
        )
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: {consent_check.message}"
        )
    
    # Fetch data from central registry
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.REGISTRY_API_URL}/api/registry/patients/{patient_id}",
                headers={"X-API-Key": settings.REGISTRY_API_KEY},
                timeout=10.0
            )
            
            if response.status_code == 404:
                # Log denied access
                AccessLogService.log_access(
                    db=db,
                    patient_id=patient_id,
                    accessed_by=current_worker.worker_id,
                    facility_id=current_worker.facility_id,
                    action="view",
                    result=AccessResult.DENIED,
                    reason="Patient not found in central registry",
                    ip_address=client_ip
                )
                
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Patient not found in central registry"
                )
            
            response.raise_for_status()
            registry_data = response.json()
    
    except httpx.HTTPError as e:
        logger.error(f"Registry API error: {e}")
        # Log denied access
        AccessLogService.log_access(
            db=db,
            patient_id=patient_id,
            accessed_by=current_worker.worker_id,
            facility_id=current_worker.facility_id,
            action="view",
            result=AccessResult.DENIED,
            reason="Central registry service unavailable",
            ip_address=client_ip
        )
        
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Central registry service unavailable"
        )
    
    # Log successful access
    AccessLogService.log_access(
        db=db,
        patient_id=patient_id,
        accessed_by=current_worker.worker_id,
        facility_id=current_worker.facility_id,
        action="view",
        result=AccessResult.ALLOWED,
        ip_address=client_ip
    )
    
    # Return patient data with access metadata
    return PatientDetailResponse(
        patient_id=registry_data["patient_id"],
        first_name=registry_data["first_name"],
        last_name=registry_data["last_name"],
        date_of_birth=registry_data["date_of_birth"],
        gender=registry_data["gender"],
        phone=registry_data["phone"],
        email=registry_data["email"],
        address=registry_data["address"],
        emergency_contact=registry_data["emergency_contact"],
        access_granted_at=consent_check.consent_id,
        consent_type=consent_check.consent_type.value
    )


@router.get("/me/profile", response_model=PatientResponse)
async def get_my_patient_profile(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    Get current patient's own profile
    
    **Patient role required**
    """
    return PatientResponse(
        patient_id=current_patient.patient_id,
        user_id=current_patient.user_id,
        first_name=current_patient.first_name,
        last_name=current_patient.last_name,
        date_of_birth=current_patient.date_of_birth,
        created_at=current_patient.created_at
    )


@router.get("/me/full-data", response_model=RegistryPatientResponse)
async def get_my_full_data(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    Get current patient's full data from central registry
    
    **Patient role required**
    
    Patients can always access their own data without consent requirements.
    """
    try:
        # Decrypt national ID
        national_id = decrypt_data(current_patient.national_id_encrypted)
        
        # Fetch from central registry
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.REGISTRY_API_URL}/api/registry/patients",
                params={"national_id": national_id},
                headers={"X-API-Key": settings.REGISTRY_API_KEY},
                timeout=10.0
            )
            
            if response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Patient data not found in central registry"
                )
            
            response.raise_for_status()
            registry_data = response.json()
            
            return RegistryPatientResponse(**registry_data)
    
    except httpx.HTTPError as e:
        logger.error(f"Registry API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Central registry service unavailable"
        )
    except Exception as e:
        logger.error(f"Error fetching patient data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching patient data"
        )