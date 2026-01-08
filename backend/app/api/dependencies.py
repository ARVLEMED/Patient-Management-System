from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.models import User, Patient, HealthcareWorker, UserRole
import logging

logger = logging.getLogger(__name__)

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Authorization credentials
        db: Database session
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    try:
        # Decode token
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    # Get user from database
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_patient(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Patient:
    """
    Dependency to get current patient (requires patient role)
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Current patient object
        
    Raises:
        HTTPException: If user is not a patient
    """
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Patient role required."
        )
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.user_id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    return patient


async def get_current_healthcare_worker(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> HealthcareWorker:
    """
    Dependency to get current healthcare worker (requires healthcare_worker role)
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Current healthcare worker object
        
    Raises:
        HTTPException: If user is not a healthcare worker
    """
    if current_user.role != UserRole.HEALTHCARE_WORKER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Healthcare worker role required."
        )
    
    worker = db.query(HealthcareWorker).filter(
        HealthcareWorker.user_id == current_user.user_id
    ).first()
    
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Healthcare worker profile not found"
        )
    
    return worker


async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to verify admin role
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user object if admin
        
    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Admin role required."
        )
    
    return current_user


def get_client_ip(request: Request) -> Optional[str]:
    """
    Extract client IP address from request
    
    Args:
        request: FastAPI request object
        
    Returns:
        Client IP address or None
    """
    # Check for forwarded IP (in case of proxy)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    # Get direct client IP
    if request.client:
        return request.client.host
    
    return None