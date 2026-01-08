from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
import logging

from app.models.models import Consent, ConsentStatus, ConsentType
from app.schemas.consent import ConsentCheckResponse

logger = logging.getLogger(__name__)


class ConsentService:
    """Service for consent management operations"""
    
    @staticmethod
    def check_consent(
        db: Session,
        patient_id: str,
        facility_id: str,
        consent_type: ConsentType
    ) -> ConsentCheckResponse:
        """
        Check if valid consent exists for patient and facility
        
        Args:
            db: Database session
            patient_id: Patient ID
            facility_id: Facility ID
            consent_type: Required consent type
            
        Returns:
            ConsentCheckResponse with consent status
        """
        # Query for active consent
        consent = db.query(Consent).filter(
            Consent.patient_id == patient_id,
            Consent.facility_id == facility_id,
            Consent.status == ConsentStatus.ACTIVE
        ).first()
        
        if not consent:
            return ConsentCheckResponse(
                has_consent=False,
                message="No active consent found"
            )
        
        # Check if consent has expired
        if consent.expires_at and consent.expires_at < datetime.utcnow():
            # Update status to expired
            consent.status = ConsentStatus.EXPIRED
            db.commit()
            
            return ConsentCheckResponse(
                has_consent=False,
                consent_id=consent.consent_id,
                status=ConsentStatus.EXPIRED,
                message="Consent has expired"
            )
        
        # Check if consent type is sufficient
        # Hierarchy: share > edit > view
        consent_hierarchy = {
            ConsentType.VIEW: 1,
            ConsentType.EDIT: 2,
            ConsentType.SHARE: 3
        }
        
        required_level = consent_hierarchy.get(consent_type, 1)
        granted_level = consent_hierarchy.get(consent.consent_type, 1)
        
        if granted_level < required_level:
            return ConsentCheckResponse(
                has_consent=False,
                consent_id=consent.consent_id,
                consent_type=consent.consent_type,
                status=consent.status,
                message=f"Insufficient consent. Required: {consent_type}, Granted: {consent.consent_type}"
            )
        
        # Valid consent found
        return ConsentCheckResponse(
            has_consent=True,
            consent_id=consent.consent_id,
            consent_type=consent.consent_type,
            status=consent.status,
            expires_at=consent.expires_at,
            message="Active consent found"
        )
    
    @staticmethod
    def grant_consent(
        db: Session,
        patient_id: str,
        facility_id: str,
        consent_type: ConsentType,
        purpose: str,
        granted_by: str,
        expires_at: Optional[datetime] = None
    ) -> Consent:
        """
        Grant new consent
        
        Args:
            db: Database session
            patient_id: Patient ID
            facility_id: Facility ID
            consent_type: Type of consent
            purpose: Purpose of consent
            granted_by: User ID who granted consent
            expires_at: Optional expiration date
            
        Returns:
            Created consent object
        """
        # Check if active consent already exists
        existing_consent = db.query(Consent).filter(
            Consent.patient_id == patient_id,
            Consent.facility_id == facility_id,
            Consent.status == ConsentStatus.ACTIVE
        ).first()
        
        if existing_consent:
            # Revoke existing consent
            existing_consent.status = ConsentStatus.REVOKED
            existing_consent.revoked_at = datetime.utcnow()
        
        # Create new consent
        new_consent = Consent(
            patient_id=patient_id,
            facility_id=facility_id,
            consent_type=consent_type,
            granted_at=datetime.utcnow(),
            expires_at=expires_at,
            granted_by=granted_by,
            purpose=purpose,
            status=ConsentStatus.ACTIVE
        )
        
        db.add(new_consent)
        db.commit()
        db.refresh(new_consent)
        
        logger.info(f"Consent granted: {new_consent.consent_id} for patient {patient_id}")
        
        return new_consent
    
    @staticmethod
    def revoke_consent(
        db: Session,
        consent_id: str,
        patient_id: str
    ) -> Consent:
        """
        Revoke consent
        
        Args:
            db: Database session
            consent_id: Consent ID to revoke
            patient_id: Patient ID (for authorization check)
            
        Returns:
            Revoked consent object
            
        Raises:
            ValueError: If consent not found or not owned by patient
        """
        consent = db.query(Consent).filter(
            Consent.consent_id == consent_id
        ).first()
        
        if not consent:
            raise ValueError("Consent not found")
        
        if consent.patient_id != patient_id:
            raise ValueError("Not authorized to revoke this consent")
        
        if consent.status == ConsentStatus.REVOKED:
            raise ValueError("Consent already revoked")
        
        # Revoke consent
        consent.status = ConsentStatus.REVOKED
        consent.revoked_at = datetime.utcnow()
        
        db.commit()
        db.refresh(consent)
        
        logger.info(f"Consent revoked: {consent_id} by patient {patient_id}")
        
        return consent
    
    @staticmethod
    def get_patient_consents(
        db: Session,
        patient_id: str,
        status: Optional[ConsentStatus] = None
    ) -> List[Consent]:
        """
        Get all consents for a patient
        
        Args:
            db: Database session
            patient_id: Patient ID
            status: Optional filter by status
            
        Returns:
            List of consent objects
        """
        query = db.query(Consent).filter(Consent.patient_id == patient_id)
        
        if status:
            query = query.filter(Consent.status == status)
        
        # Check for expired consents and update status
        consents = query.all()
        for consent in consents:
            if (consent.status == ConsentStatus.ACTIVE and 
                consent.expires_at and 
                consent.expires_at < datetime.utcnow()):
                consent.status = ConsentStatus.EXPIRED
        
        db.commit()
        
        return consents
    
    @staticmethod
    def get_facility_consents(
        db: Session,
        facility_id: str,
        status: Optional[ConsentStatus] = None
    ) -> List[Consent]:
        """
        Get all consents for a facility
        
        Args:
            db: Database session
            facility_id: Facility ID
            status: Optional filter by status
            
        Returns:
            List of consent objects
        """
        query = db.query(Consent).filter(Consent.facility_id == facility_id)
        
        if status:
            query = query.filter(Consent.status == status)
        
        return query.all()