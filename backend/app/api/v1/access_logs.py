from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.core.database import get_db
from app.models.models import User, Patient, HealthcareWorker, AccessResult
from app.schemas.access_log import AccessLogResponse, AccessLogListResponse
from app.services.access_log_service import AccessLogService
from app.api.dependencies import (
    get_current_user,
    get_current_patient,
    get_current_healthcare_worker
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/patient/{patient_id}", response_model=AccessLogListResponse)
async def get_patient_access_logs(
    patient_id: str,
    limit: int = Query(100, ge=1, le=500, description="Maximum number of logs to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get access logs for a patient
    
    **Patient can view their own logs, admins can view all logs**
    
    - **patient_id**: Patient ID
    - **limit**: Maximum number of logs to return (default: 100, max: 500)
    """
    # Authorization check
    if current_user.role.value == "patient":
        # Patient can only view their own logs
        patient = db.query(Patient).filter(Patient.user_id == current_user.user_id).first()
        if not patient or patient.patient_id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view these access logs"
            )
    elif current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view access logs"
        )
    
    # Get access logs
    logs = AccessLogService.get_patient_access_logs(
        db=db,
        patient_id=patient_id,
        limit=limit
    )
    
    # Format response with enriched data
    log_responses = []
    for log in logs:
        # Get patient name
        patient_name = None
        if log.patient:
            patient_name = f"{log.patient.first_name} {log.patient.last_name}"
        
        # Get worker name
        worker_name = None
        if log.worker and log.worker.user:
            worker_name = log.worker.user.email
        
        # Get facility name
        facility_name = None
        if log.facility:
            facility_name = log.facility.name
        
        log_responses.append(
            AccessLogResponse(
                log_id=log.log_id,
                patient_id=log.patient_id,
                patient_name=patient_name,
                accessed_by=log.accessed_by,
                worker_name=worker_name,
                facility_id=log.facility_id,
                facility_name=facility_name,
                action=log.action,
                result=log.result,
                reason=log.reason,
                timestamp=log.timestamp,
                ip_address=log.ip_address
            )
        )
    
    return AccessLogListResponse(
        logs=log_responses,
        total=len(log_responses)
    )


@router.get("/worker/me", response_model=AccessLogListResponse)
async def get_my_worker_access_logs(
    limit: int = Query(100, ge=1, le=500, description="Maximum number of logs to return"),
    current_worker: HealthcareWorker = Depends(get_current_healthcare_worker),
    db: Session = Depends(get_db)
):
    """
    Get access logs for current healthcare worker
    
    **Healthcare worker role required**
    
    - **limit**: Maximum number of logs to return (default: 100, max: 500)
    """
    # Get access logs
    logs = AccessLogService.get_worker_access_logs(
        db=db,
        worker_id=current_worker.worker_id,
        limit=limit
    )
    
    # Format response
    log_responses = []
    for log in logs:
        # Get patient name
        patient_name = None
        if log.patient:
            patient_name = f"{log.patient.first_name} {log.patient.last_name}"
        
        # Get facility name
        facility_name = None
        if log.facility:
            facility_name = log.facility.name
        
        log_responses.append(
            AccessLogResponse(
                log_id=log.log_id,
                patient_id=log.patient_id,
                patient_name=patient_name,
                accessed_by=log.accessed_by,
                worker_name=None,  # Don't show own name
                facility_id=log.facility_id,
                facility_name=facility_name,
                action=log.action,
                result=log.result,
                reason=log.reason,
                timestamp=log.timestamp,
                ip_address=log.ip_address
            )
        )
    
    return AccessLogListResponse(
        logs=log_responses,
        total=len(log_responses)
    )


@router.get("/facility/{facility_id}", response_model=AccessLogListResponse)
async def get_facility_access_logs(
    facility_id: str,
    limit: int = Query(100, ge=1, le=500, description="Maximum number of logs to return"),
    current_worker: HealthcareWorker = Depends(get_current_healthcare_worker),
    db: Session = Depends(get_db)
):
    """
    Get access logs for a facility
    
    **Healthcare worker role required (must be from the same facility)**
    
    - **facility_id**: Facility ID
    - **limit**: Maximum number of logs to return (default: 100, max: 500)
    """
    # Authorization check - worker must be from the same facility
    if current_worker.facility_id != facility_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view access logs for this facility"
        )
    
    # Get access logs
    logs = AccessLogService.get_facility_access_logs(
        db=db,
        facility_id=facility_id,
        limit=limit
    )
    
    # Format response
    log_responses = []
    for log in logs:
        # Get patient name
        patient_name = None
        if log.patient:
            patient_name = f"{log.patient.first_name} {log.patient.last_name}"
        
        # Get worker name
        worker_name = None
        if log.worker and log.worker.user:
            worker_name = log.worker.user.email
        
        log_responses.append(
            AccessLogResponse(
                log_id=log.log_id,
                patient_id=log.patient_id,
                patient_name=patient_name,
                accessed_by=log.accessed_by,
                worker_name=worker_name,
                facility_id=log.facility_id,
                facility_name=log.facility.name if log.facility else None,
                action=log.action,
                result=log.result,
                reason=log.reason,
                timestamp=log.timestamp,
                ip_address=log.ip_address
            )
        )
    
    return AccessLogListResponse(
        logs=log_responses,
        total=len(log_responses)
    )