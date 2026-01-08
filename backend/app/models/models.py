from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.core.database import Base


def generate_uuid():
    """Generate UUID for primary keys"""
    return str(uuid.uuid4())


# Enums
class UserRole(str, enum.Enum):
    PATIENT = "patient"
    HEALTHCARE_WORKER = "healthcare_worker"
    ADMIN = "admin"


class FacilityType(str, enum.Enum):
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    PHARMACY = "pharmacy"


class ConsentType(str, enum.Enum):
    VIEW = "view"
    EDIT = "edit"
    SHARE = "share"


class ConsentStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


class AccessResult(str, enum.Enum):
    ALLOWED = "allowed"
    DENIED = "denied"


# User Model
class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="user", uselist=False)
    healthcare_worker = relationship("HealthcareWorker", back_populates="user", uselist=False)


# Patient Model
class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String(36), primary_key=True)  # From central registry
    user_id = Column(String(36), ForeignKey("users.user_id"), unique=True, nullable=False)
    national_id_encrypted = Column(Text, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="patient")
    consents = relationship("Consent", back_populates="patient")
    access_logs = relationship("AccessLog", back_populates="patient")


# Healthcare Facility Model
class HealthcareFacility(Base):
    __tablename__ = "healthcare_facilities"

    facility_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    facility_type = Column(Enum(FacilityType), nullable=False)
    license_number = Column(String(100), unique=True, nullable=False)
    location = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workers = relationship("HealthcareWorker", back_populates="facility")
    consents = relationship("Consent", back_populates="facility")
    access_logs = relationship("AccessLog", back_populates="facility")


# Healthcare Worker Model
class HealthcareWorker(Base):
    __tablename__ = "healthcare_workers"

    worker_id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.user_id"), unique=True, nullable=False)
    facility_id = Column(String(36), ForeignKey("healthcare_facilities.facility_id"), nullable=False)
    license_number = Column(String(100), unique=True, nullable=False)
    job_title = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="healthcare_worker")
    facility = relationship("HealthcareFacility", back_populates="workers")
    access_logs = relationship("AccessLog", back_populates="worker")


# Consent Model
class Consent(Base):
    __tablename__ = "consents"

    consent_id = Column(String(36), primary_key=True, default=generate_uuid)
    patient_id = Column(String(36), ForeignKey("patients.patient_id"), nullable=False, index=True)
    facility_id = Column(String(36), ForeignKey("healthcare_facilities.facility_id"), nullable=False, index=True)
    consent_type = Column(Enum(ConsentType), nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    revoked_at = Column(DateTime, nullable=True)
    granted_by = Column(String(36), nullable=False)  # user_id who granted
    purpose = Column(Text, nullable=False)
    status = Column(Enum(ConsentStatus), default=ConsentStatus.ACTIVE, nullable=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="consents")
    facility = relationship("HealthcareFacility", back_populates="consents")


# Access Log Model
class AccessLog(Base):
    __tablename__ = "access_logs"

    log_id = Column(String(36), primary_key=True, default=generate_uuid)
    patient_id = Column(String(36), ForeignKey("patients.patient_id"), nullable=False, index=True)
    accessed_by = Column(String(36), ForeignKey("healthcare_workers.worker_id"), nullable=False)
    facility_id = Column(String(36), ForeignKey("healthcare_facilities.facility_id"), nullable=False)
    action = Column(String(50), nullable=False)  # view, edit, share
    result = Column(Enum(AccessResult), nullable=False)
    reason = Column(Text, nullable=True)  # if denied
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="access_logs")
    worker = relationship("HealthcareWorker", back_populates="access_logs")
    facility = relationship("HealthcareFacility", back_populates="access_logs")