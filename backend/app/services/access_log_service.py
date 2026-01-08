from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
import logging

from app.models.models import AccessLog, AccessResult, Patient, HealthcareWorker, HealthcareFacility

logger = logging.getLogger(__name__)


class AccessLogService:
    """Service for access logging operations"""
    
    @staticmethod
    def log_access(
        db: Session,
        patient_id: str,
        accessed_by: str,
        facility_id: str,
        action: str,
        result: AccessResult,
        reason: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AccessLog:
        """
        Log patient data access attempt
        
        Args:
            db: Database session
            patient_id: Patient ID
            accessed_by: Healthcare worker ID
            facility_id: Facility ID
            action: Action performed (view, edit, share)
            result: Access result (allowed, denied)
            reason: Optional reason for denial
            ip_address: Optional IP address
            
        Returns:
            Created access log object
        """
        access_log = AccessLog(
            patient_id=patient_id,
            accessed_by=accessed_by,
            facility_id=facility_id,
            action=action,
            result=result,
            reason=reason,
            timestamp=datetime.utcnow(),
            ip_address=ip_address
        )
        
        db.add(access_log)
        db.commit()
        db.refresh(access_log)
        
        log_message = f"Access {result.value}: {action} by worker {accessed_by} on patient {patient_id}"
        if result == AccessResult.DENIED:
            logger.warning(f"{log_message} - Reason: {reason}")
        else:
            logger.info(log_message)
        
        return access_log
    
    @staticmethod
    def get_patient_access_logs(
        db: Session,
        patient_id: str,
        limit: int = 100
    ) -> List[AccessLog]:
        """
        Get access logs for a patient
        
        Args:
            db: Database session
            patient_id: Patient ID
            limit: Maximum number of logs to return
            
        Returns:
            List of access log objects with enriched data
        """
        logs = db.query(AccessLog).filter(
            AccessLog.patient_id == patient_id
        ).order_by(
            AccessLog.timestamp.desc()
        ).limit(limit).all()
        
        return logs
    
    @staticmethod
    def get_worker_access_logs(
        db: Session,
        worker_id: str,
        limit: int = 100
    ) -> List[AccessLog]:
        """
        Get access logs for a healthcare worker
        
        Args:
            db: Database session
            worker_id: Healthcare worker ID
            limit: Maximum number of logs to return
            
        Returns:
            List of access log objects
        """
        logs = db.query(AccessLog).filter(
            AccessLog.accessed_by == worker_id
        ).order_by(
            AccessLog.timestamp.desc()
        ).limit(limit).all()
        
        return logs
    
    @staticmethod
    def get_facility_access_logs(
        db: Session,
        facility_id: str,
        limit: int = 100
    ) -> List[AccessLog]:
        """
        Get access logs for a facility
        
        Args:
            db: Database session
            facility_id: Facility ID
            limit: Maximum number of logs to return
            
        Returns:
            List of access log objects
        """
        logs = db.query(AccessLog).filter(
            AccessLog.facility_id == facility_id
        ).order_by(
            AccessLog.timestamp.desc()
        ).limit(limit).all()
        
        return logs
    
    @staticmethod
    def get_all_access_logs(
        db: Session,
        result: Optional[AccessResult] = None,
        limit: int = 100
    ) -> List[AccessLog]:
        """
        Get all access logs (admin only)
        
        Args:
            db: Database session
            result: Optional filter by result (allowed/denied)
            limit: Maximum number of logs to return
            
        Returns:
            List of access log objects
        """
        query = db.query(AccessLog)
        
        if result:
            query = query.filter(AccessLog.result == result)
        
        logs = query.order_by(
            AccessLog.timestamp.desc()
        ).limit(limit).all()
        
        return logs