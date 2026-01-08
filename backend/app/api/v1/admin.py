from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import logging

from app.core.database import get_db
from app.models.models import (
    User, Patient, HealthcareWorker, HealthcareFacility,
    Consent, AccessLog, AccessResult, ConsentStatus
)
from app.schemas.user import UserResponse
from app.schemas.access_log import AccessLogResponse, AccessLogListResponse
from app.api.dependencies import get_current_admin
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()


class SystemStatistics(BaseModel):
    """System statistics response"""
    total_users: int
    total_patients: int
    total_healthcare_workers: int
    total_facilities: int
    total_consents: int
    active_consents: int
    total_access_logs: int
    allowed_access_count: int
    denied_access_count: int


class UserListResponse(BaseModel):
    """User list response"""
    users: list[UserResponse]
    total: int


@router.get("/users", response_model=UserListResponse)
async def list_all_users(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get list of all users
    
    **Admin role required**
    
    - **limit**: Maximum number of users to return (default: 100, max: 500)
    - **offset**: Number of users to skip (default: 0)
    """
    users = db.query(User).offset(offset).limit(limit).all()
    
    user_responses = [
        UserResponse(
            user_id=user.user_id,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login
        )
        for user in users
    ]
    
    total = db.query(func.count(User.user_id)).scalar()
    
    return UserListResponse(
        users=user_responses,
        total=total
    )


@router.get("/audit-logs", response_model=AccessLogListResponse)
async def get_audit_logs(
    limit: int = Query(100, ge=1, le=500),
    result: Optional[AccessResult] = Query(None, description="Filter by result (allowed/denied)"),
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get system audit logs (all access logs)
    
    **Admin role required**
    
    - **limit**: Maximum number of logs to return (default: 100, max: 500)
    - **result**: Optional filter by result (allowed, denied)
    """
    from app.services.access_log_service import AccessLogService
    
    logs = AccessLogService.get_all_access_logs(
        db=db,
        result=result,
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


@router.get("/statistics", response_model=SystemStatistics)
async def get_system_statistics(
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get system statistics
    
    **Admin role required**
    
    Returns comprehensive statistics about the system including:
    - User counts by role
    - Facility count
    - Consent statistics
    - Access log statistics
    """
    # Count users
    total_users = db.query(func.count(User.user_id)).scalar()
    total_patients = db.query(func.count(Patient.patient_id)).scalar()
    total_healthcare_workers = db.query(func.count(HealthcareWorker.worker_id)).scalar()
    
    # Count facilities
    total_facilities = db.query(func.count(HealthcareFacility.facility_id)).scalar()
    
    # Count consents
    total_consents = db.query(func.count(Consent.consent_id)).scalar()
    active_consents = db.query(func.count(Consent.consent_id)).filter(
        Consent.status == ConsentStatus.ACTIVE
    ).scalar()
    
    # Count access logs
    total_access_logs = db.query(func.count(AccessLog.log_id)).scalar()
    allowed_access_count = db.query(func.count(AccessLog.log_id)).filter(
        AccessLog.result == AccessResult.ALLOWED
    ).scalar()
    denied_access_count = db.query(func.count(AccessLog.log_id)).filter(
        AccessLog.result == AccessResult.DENIED
    ).scalar()
    
    return SystemStatistics(
        total_users=total_users,
        total_patients=total_patients,
        total_healthcare_workers=total_healthcare_workers,
        total_facilities=total_facilities,
        total_consents=total_consents,
        active_consents=active_consents,
        total_access_logs=total_access_logs,
        allowed_access_count=allowed_access_count,
        denied_access_count=denied_access_count
    )


@router.get("/consents", response_model=dict)
async def get_all_consents(
    limit: int = Query(100, ge=1, le=500),
    status_filter: Optional[ConsentStatus] = Query(None, alias="status"),
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all consents in the system
    
    **Admin role required**
    
    - **limit**: Maximum number of consents to return (default: 100, max: 500)
    - **status**: Optional filter by status (active, expired, revoked)
    """
    query = db.query(Consent)
    
    if status_filter:
        query = query.filter(Consent.status == status_filter)
    
    consents = query.order_by(Consent.granted_at.desc()).limit(limit).all()
    
    consent_responses = []
    for consent in consents:
        consent_responses.append({
            "consent_id": consent.consent_id,
            "patient_id": consent.patient_id,
            "facility_id": consent.facility_id,
            "facility_name": consent.facility.name if consent.facility else None,
            "consent_type": consent.consent_type.value,
            "granted_at": consent.granted_at.isoformat(),
            "expires_at": consent.expires_at.isoformat() if consent.expires_at else None,
            "revoked_at": consent.revoked_at.isoformat() if consent.revoked_at else None,
            "status": consent.status.value,
            "purpose": consent.purpose
        })
    
    total = db.query(func.count(Consent.consent_id)).scalar()
    
    return {
        "consents": consent_responses,
        "total": total
    }