"""
Seed data script for Patient Management System
Populates database with initial test data
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.core.database import SessionLocal
from app.core.security import hash_password, encrypt_data
from app.models.models import (
    User, Patient, HealthcareFacility, HealthcareWorker,
    Consent, AccessLog, UserRole, FacilityType,
    ConsentType, ConsentStatus, AccessResult
)

logger = logging.getLogger(__name__)


def seed_database():
    """Seed database with initial data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            
            logger.info("Seed script SKIPPED: users already exist")

            return
        
        logger.info("Starting database seeding...")
        logger.info("Seed script STARTED")

        
        # 1. Create Healthcare Facilities (3)
        facilities = create_facilities(db)
        logger.info(f"Created {len(facilities)} facilities")
        
        # 2. Create Users and Profiles
        users = create_users_and_profiles(db, facilities)
        logger.info(f"Created {len(users)} users with profiles")
        
        # 3. Create Consents (10)
        consents = create_consents(db, users, facilities)
        logger.info(f"Created {len(consents)} consents")
        
        # 4. Create Access Logs (20)
        access_logs = create_access_logs(db, users, facilities)
        logger.info(f"Created {len(access_logs)} access logs")
        
        db.commit()
        logger.info("Database seeding completed successfully!")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


def create_facilities(db: Session):
    """Create healthcare facilities"""
    facilities = [
        HealthcareFacility(
            facility_id="FAC-001",
            name="HealthHub Clinic",
            facility_type=FacilityType.CLINIC,
            license_number="HF-12345",
            location="Nairobi, Westlands",
            created_at=datetime.utcnow()
        ),
        HealthcareFacility(
            facility_id="FAC-002",
            name="Nairobi General Hospital",
            facility_type=FacilityType.HOSPITAL,
            license_number="HF-67890",
            location="Nairobi, Central Business District",
            created_at=datetime.utcnow()
        ),
        HealthcareFacility(
            facility_id="FAC-003",
            name="MediCare Pharmacy",
            facility_type=FacilityType.PHARMACY,
            license_number="HF-11223",
            location="Nairobi, Kilimani",
            created_at=datetime.utcnow()
        )
    ]
    
    for facility in facilities:
        db.add(facility)
    
    db.flush()
    return facilities


def create_users_and_profiles(db: Session, facilities):
    """Create users with their role-specific profiles"""
    users_data = []
    
    # Default password for all test accounts
    default_password = hash_password("Test123!")
    
    # === PATIENTS (5) ===
    patients_data = [
        {
            "email": "patient@test.com",
            "patient_id": "PAT-001234",
            "national_id": "12345678",
            "first_name": "John",
            "last_name": "Kamau",
            "date_of_birth": "1985-03-15"
        },
        {
            "email": "sarah.wanjiku@test.com",
            "patient_id": "PAT-001235",
            "national_id": "23456789",
            "first_name": "Sarah",
            "last_name": "Wanjiku",
            "date_of_birth": "1990-07-22"
        },
        {
            "email": "james.ochieng@test.com",
            "patient_id": "PAT-001236",
            "national_id": "34567890",
            "first_name": "James",
            "last_name": "Ochieng",
            "date_of_birth": "1978-11-10"
        },
        {
            "email": "faith.akinyi@test.com",
            "patient_id": "PAT-001237",
            "national_id": "45678901",
            "first_name": "Faith",
            "last_name": "Akinyi",
            "date_of_birth": "1995-05-18"
        },
        {
            "email": "david.kipchoge@test.com",
            "patient_id": "PAT-001238",
            "national_id": "56789012",
            "first_name": "David",
            "last_name": "Kipchoge",
            "date_of_birth": "1982-09-25"
        }
    ]
    
    for p_data in patients_data:
        user = User(
            email=p_data["email"],
            password_hash=default_password,
            role=UserRole.PATIENT,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(user)
        db.flush()
        
        patient = Patient(
            patient_id=p_data["patient_id"],
            user_id=user.user_id,
            national_id_encrypted=encrypt_data(p_data["national_id"]),
            first_name=p_data["first_name"],
            last_name=p_data["last_name"],
            date_of_birth=datetime.fromisoformat(p_data["date_of_birth"]),
            created_at=datetime.utcnow()
        )
        db.add(patient)
        
        users_data.append({"user": user, "profile": patient, "type": "patient"})
    
    # === HEALTHCARE WORKERS (8) ===
    workers_data = [
        {
            "email": "doctor@test.com",
            "facility_id": "FAC-001",
            "license_number": "MD-12345",
            "job_title": "General Practitioner"
        },
        {
            "email": "dr.smith@healthhub.com",
            "facility_id": "FAC-001",
            "license_number": "MD-23456",
            "job_title": "Pediatrician"
        },
        {
            "email": "nurse.jane@healthhub.com",
            "facility_id": "FAC-001",
            "license_number": "RN-34567",
            "job_title": "Registered Nurse"
        },
        {
            "email": "dr.omondi@ngh.co.ke",
            "facility_id": "FAC-002",
            "license_number": "MD-45678",
            "job_title": "Cardiologist"
        },
        {
            "email": "dr.wambui@ngh.co.ke",
            "facility_id": "FAC-002",
            "license_number": "MD-56789",
            "job_title": "Surgeon"
        },
        {
            "email": "nurse.peter@ngh.co.ke",
            "facility_id": "FAC-002",
            "license_number": "RN-67890",
            "job_title": "Emergency Nurse"
        },
        {
            "email": "pharmacist@medicare.com",
            "facility_id": "FAC-003",
            "license_number": "PH-78901",
            "job_title": "Chief Pharmacist"
        },
        {
            "email": "assistant@medicare.com",
            "facility_id": "FAC-003",
            "license_number": "PA-89012",
            "job_title": "Pharmacy Assistant"
        }
    ]
    
    for w_data in workers_data:
        user = User(
            email=w_data["email"],
            password_hash=default_password,
            role=UserRole.HEALTHCARE_WORKER,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(user)
        db.flush()
        
        worker = HealthcareWorker(
            user_id=user.user_id,
            facility_id=w_data["facility_id"],
            license_number=w_data["license_number"],
            job_title=w_data["job_title"],
            created_at=datetime.utcnow()
        )
        db.add(worker)
        db.flush()
        
        users_data.append({"user": user, "profile": worker, "type": "worker"})
    
    # === ADMINS (2) ===
    admins_data = [
        {"email": "admin@test.com"},
        {"email": "superadmin@pms.com"}
    ]
    
    for a_data in admins_data:
        user = User(
            email=a_data["email"],
            password_hash=default_password,
            role=UserRole.ADMIN,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(user)
        users_data.append({"user": user, "profile": None, "type": "admin"})
    
    db.flush()
    return users_data


def create_consents(db: Session, users, facilities):
    """Create consent records"""
    # Get patients and facilities
    patients = [u for u in users if u["type"] == "patient"]
    
    consents = []
    
    # Active consents
    consent_configs = [
        # Patient 1: HealthHub Clinic - Active view consent
        {
            "patient": patients[0]["profile"],
            "facility": facilities[0],
            "consent_type": ConsentType.VIEW,
            "status": ConsentStatus.ACTIVE,
            "purpose": "Regular health checkup and consultation",
            "expires_at": datetime.utcnow() + timedelta(days=180)
        },
        # Patient 1: Nairobi General Hospital - Active edit consent
        {
            "patient": patients[0]["profile"],
            "facility": facilities[1],
            "consent_type": ConsentType.EDIT,
            "status": ConsentStatus.ACTIVE,
            "purpose": "Emergency treatment and medical records update",
            "expires_at": datetime.utcnow() + timedelta(days=90)
        },
        # Patient 2: HealthHub Clinic - Active share consent
        {
            "patient": patients[1]["profile"],
            "facility": facilities[0],
            "consent_type": ConsentType.SHARE,
            "status": ConsentStatus.ACTIVE,
            "purpose": "Comprehensive care coordination with specialists",
            "expires_at": None
        },
        # Patient 2: MediCare Pharmacy - Active view consent
        {
            "patient": patients[1]["profile"],
            "facility": facilities[2],
            "consent_type": ConsentType.VIEW,
            "status": ConsentStatus.ACTIVE,
            "purpose": "Prescription fulfillment and medication counseling",
            "expires_at": datetime.utcnow() + timedelta(days=365)
        },
        # Patient 3: Nairobi General Hospital - Active view consent
        {
            "patient": patients[2]["profile"],
            "facility": facilities[1],
            "consent_type": ConsentType.VIEW,
            "status": ConsentStatus.ACTIVE,
            "purpose": "Cardiac consultation and follow-up",
            "expires_at": datetime.utcnow() + timedelta(days=120)
        },
        # Patient 4: HealthHub Clinic - Expired consent
        {
            "patient": patients[3]["profile"],
            "facility": facilities[0],
            "consent_type": ConsentType.VIEW,
            "status": ConsentStatus.EXPIRED,
            "purpose": "Annual health screening",
            "expires_at": datetime.utcnow() - timedelta(days=30)
        },
        # Patient 4: Nairobi General Hospital - Active edit consent
        {
            "patient": patients[3]["profile"],
            "facility": facilities[1],
            "consent_type": ConsentType.EDIT,
            "status": ConsentStatus.ACTIVE,
            "purpose": "Maternity care and delivery",
            "expires_at": datetime.utcnow() + timedelta(days=180)
        },
        # Patient 5: HealthHub Clinic - Revoked consent
        {
            "patient": patients[4]["profile"],
            "facility": facilities[0],
            "consent_type": ConsentType.VIEW,
            "status": ConsentStatus.REVOKED,
            "purpose": "General consultation",
            "expires_at": None,
            "revoked_at": datetime.utcnow() - timedelta(days=15)
        },
        # Patient 5: MediCare Pharmacy - Active view consent
        {
            "patient": patients[4]["profile"],
            "facility": facilities[2],
            "consent_type": ConsentType.VIEW,
            "status": ConsentStatus.ACTIVE,
            "purpose": "Medication management",
            "expires_at": datetime.utcnow() + timedelta(days=90)
        },
        # Patient 3: MediCare Pharmacy - Active view consent
        {
            "patient": patients[2]["profile"],
            "facility": facilities[2],
            "consent_type": ConsentType.VIEW,
            "status": ConsentStatus.ACTIVE,
            "purpose": "Prescription medications",
            "expires_at": datetime.utcnow() + timedelta(days=60)
        }
    ]
    
    for config in consent_configs:
        consent = Consent(
            patient_id=config["patient"].patient_id,
            facility_id=config["facility"].facility_id,
            consent_type=config["consent_type"],
            granted_at=datetime.utcnow() - timedelta(days=30),
            expires_at=config["expires_at"],
            revoked_at=config.get("revoked_at"),
            granted_by=config["patient"].user_id,
            purpose=config["purpose"],
            status=config["status"]
        )
        db.add(consent)
        consents.append(consent)
    
    db.flush()
    return consents


def create_access_logs(db: Session, users, facilities):
    """Create access log records"""
    patients = [u for u in users if u["type"] == "patient"]
    workers = [u for u in users if u["type"] == "worker"]
    
    logs = []
    
    # Access log configurations
    log_configs = [
        # Allowed accesses
        {"patient": patients[0], "worker": workers[0], "action": "view", "result": AccessResult.ALLOWED, "reason": None},
        {"patient": patients[0], "worker": workers[1], "action": "view", "result": AccessResult.ALLOWED, "reason": None},
        {"patient": patients[0], "worker": workers[3], "action": "edit", "result": AccessResult.ALLOWED, "reason": None},
        {"patient": patients[1], "worker": workers[0], "action": "share", "result": AccessResult.ALLOWED, "reason": None},
        {"patient": patients[1], "worker": workers[6], "action": "view", "result": AccessResult.ALLOWED, "reason": None},
        {"patient": patients[2], "worker": workers[3], "action": "view", "result": AccessResult.ALLOWED, "reason": None},
        {"patient": patients[2], "worker": workers[6], "action": "view", "result": AccessResult.ALLOWED, "reason": None},
        {"patient": patients[3], "worker": workers[3], "action": "edit", "result": AccessResult.ALLOWED, "reason": None},
        {"patient": patients[4], "worker": workers[6], "action": "view", "result": AccessResult.ALLOWED, "reason": None},
        
        # Denied accesses
        {"patient": patients[2], "worker": workers[0], "action": "view", "result": AccessResult.DENIED, "reason": "No active consent found"},
        {"patient": patients[3], "worker": workers[0], "action": "view", "result": AccessResult.DENIED, "reason": "Consent has expired"},
        {"patient": patients[4], "worker": workers[0], "action": "view", "result": AccessResult.DENIED, "reason": "Consent has been revoked"},
        {"patient": patients[0], "worker": workers[6], "action": "view", "result": AccessResult.DENIED, "reason": "No active consent found"},
        {"patient": patients[1], "worker": workers[3], "action": "view", "result": AccessResult.DENIED, "reason": "No active consent found"},
        {"patient": patients[1], "worker": workers[4], "action": "edit", "result": AccessResult.DENIED, "reason": "Insufficient consent"},
        {"patient": patients[2], "worker": workers[1], "action": "view", "result": AccessResult.DENIED, "reason": "No active consent found"},
        {"patient": patients[3], "worker": workers[6], "action": "view", "result": AccessResult.DENIED, "reason": "No active consent found"},
        {"patient": patients[4], "worker": workers[1], "action": "view", "result": AccessResult.DENIED, "reason": "Consent has been revoked"},
        {"patient": patients[4], "worker": workers[3], "action": "view", "result": AccessResult.DENIED, "reason": "No active consent found"},
        {"patient": patients[0], "worker": workers[0], "action": "share", "result": AccessResult.DENIED, "reason": "Insufficient consent. Required: share, Granted: view"}
    ]
    
    for i, config in enumerate(log_configs):
        log = AccessLog(
            patient_id=config["patient"]["profile"].patient_id,
            accessed_by=config["worker"]["profile"].worker_id,
            facility_id=config["worker"]["profile"].facility_id,
            action=config["action"],
            result=config["result"],
            reason=config["reason"],
            timestamp=datetime.utcnow() - timedelta(hours=20 - i),
            ip_address=f"192.168.1.{100 + i}"
        )
        db.add(log)
        logs.append(log)
    
    db.flush()
    return logs


if __name__ == "__main__":
    seed_database()