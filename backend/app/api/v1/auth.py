from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import logging
import httpx

from app.core.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    generate_tokens,
    decode_refresh_token,
    encrypt_data
)
from app.core.config import settings
from app.models.models import User, Patient, HealthcareWorker, UserRole
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserResponse,
    UserProfileResponse,
    PatientProfileResponse,
    HealthcareWorkerProfileResponse
)
from app.api.dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - **email**: User email (must be unique)
    - **password**: Strong password (min 8 chars, uppercase, lowercase, number)
    - **role**: User role (patient, healthcare_worker, admin)
    - Additional fields required based on role
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = hash_password(user_data.password)
    
    # Create user
    new_user = User(
        email=user_data.email,
        password_hash=password_hash,
        role=user_data.role,
        is_active=True,
        created_at=datetime.utcnow()
    )
    
    db.add(new_user)
    db.flush()  # Get user_id without committing
    
    try:
        # Create role-specific profile
        if user_data.role == UserRole.PATIENT:
            # Validate required fields
            if not all([user_data.first_name, user_data.last_name, user_data.national_id, user_data.date_of_birth]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="First name, last name, national ID, and date of birth are required for patients"
                )
            
            # Fetch patient from central registry
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(
                        f"{settings.REGISTRY_API_URL}/api/registry/patients",
                        params={"national_id": user_data.national_id},
                        headers={"X-API-Key": settings.REGISTRY_API_KEY},
                        timeout=10.0
                    )
                    
                    if response.status_code == 404:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Patient not found in central registry. Please register with the central registry first."
                        )
                    
                    response.raise_for_status()
                    registry_data = response.json()
                    
                except httpx.HTTPError as e:
                    logger.error(f"Registry API error: {e}")
                    # Continue with local registration even if registry is down
                    registry_data = None
            
            # Create patient profile
            patient = Patient(
                patient_id=registry_data.get("patient_id") if registry_data else f"PAT-LOCAL-{new_user.user_id[:8]}",
                user_id=new_user.user_id,
                national_id_encrypted=encrypt_data(user_data.national_id),
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                date_of_birth=datetime.fromisoformat(user_data.date_of_birth),
                created_at=datetime.utcnow()
            )
            db.add(patient)
        
        elif user_data.role == UserRole.HEALTHCARE_WORKER:
            # Validate required fields
            if not all([user_data.facility_id, user_data.license_number, user_data.job_title]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Facility ID, license number, and job title are required for healthcare workers"
                )
            
            # Create healthcare worker profile
            worker = HealthcareWorker(
                user_id=new_user.user_id,
                facility_id=user_data.facility_id,
                license_number=user_data.license_number,
                job_title=user_data.job_title,
                created_at=datetime.utcnow()
            )
            db.add(worker)
        
        # Commit changes
        db.commit()
        db.refresh(new_user)
        
        # Generate tokens
        tokens = generate_tokens(
            user_id=new_user.user_id,
            email=new_user.email,
            role=new_user.role.value
        )
        
        logger.info(f"New user registered: {new_user.email} ({new_user.role})")
        
        return TokenResponse(**tokens, expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    
    except Exception as e:
        db.rollback()
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user profile: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    login_data: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login user and get access tokens
    
    - **email**: User email
    - **password**: User password
    """
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Generate tokens
    tokens = generate_tokens(
        user_id=user.user_id,
        email=user.email,
        role=user.role.value
    )
    
    logger.info(f"User logged in: {user.email}")
    
    return TokenResponse(**tokens, expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    - **refresh_token**: Valid refresh token
    """
    try:
        # Decode refresh token
        payload = decode_refresh_token(refresh_data.refresh_token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Generate new tokens
        tokens = generate_tokens(
            user_id=user.user_id,
            email=user.email,
            role=user.role.value
        )
        
        logger.info(f"Token refreshed for user: {user.email}")
        
        return TokenResponse(**tokens, expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token"
        )


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's profile information
    """
    user_response = UserResponse.model_validate(current_user)
    
    profile_data = {"user": user_response}
    
    # Add role-specific profile
    if current_user.role == UserRole.PATIENT:
        patient = db.query(Patient).filter(Patient.user_id == current_user.user_id).first()
        if patient:
            profile_data["patient"] = PatientProfileResponse(
                patient_id=patient.patient_id,
                user_id=patient.user_id,
                first_name=patient.first_name,
                last_name=patient.last_name,
                date_of_birth=patient.date_of_birth,
                email=current_user.email,
                created_at=patient.created_at
            )
    
    elif current_user.role == UserRole.HEALTHCARE_WORKER:
        worker = db.query(HealthcareWorker).filter(
            HealthcareWorker.user_id == current_user.user_id
        ).first()
        if worker:
            profile_data["healthcare_worker"] = HealthcareWorkerProfileResponse(
                worker_id=worker.worker_id,
                user_id=worker.user_id,
                facility_id=worker.facility_id,
                facility_name=worker.facility.name if worker.facility else None,
                license_number=worker.license_number,
                job_title=worker.job_title,
                email=current_user.email,
                created_at=worker.created_at
            )
    
    return UserProfileResponse(**profile_data)