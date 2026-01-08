from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.models.models import HealthcareFacility, User
from app.schemas.facility import FacilityResponse, FacilityListResponse
from app.api.dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=FacilityListResponse)
async def list_facilities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of all healthcare facilities
    
    **Authentication required**
    
    Returns all registered healthcare facilities in the system.
    """
    facilities = db.query(HealthcareFacility).all()
    
    facility_responses = [
        FacilityResponse(
            facility_id=facility.facility_id,
            name=facility.name,
            facility_type=facility.facility_type,
            license_number=facility.license_number,
            location=facility.location,
            created_at=facility.created_at
        )
        for facility in facilities
    ]
    
    return FacilityListResponse(
        facilities=facility_responses,
        total=len(facility_responses)
    )


@router.get("/{facility_id}", response_model=FacilityResponse)
async def get_facility(
    facility_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get facility details by ID
    
    **Authentication required**
    
    - **facility_id**: Facility ID
    """
    facility = db.query(HealthcareFacility).filter(
        HealthcareFacility.facility_id == facility_id
    ).first()
    
    if not facility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Facility not found"
        )
    
    return FacilityResponse(
        facility_id=facility.facility_id,
        name=facility.name,
        facility_type=facility.facility_type,
        license_number=facility.license_number,
        location=facility.location,
        created_at=facility.created_at
    )