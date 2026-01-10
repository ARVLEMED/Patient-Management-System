from fastapi import FastAPI, HTTPException, Header, status
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware

from app.data.mock_patients import MOCK_PATIENTS

app = FastAPI(
    title="Central Patient Registry (Mock)",
    description="Mock API simulating Kenya's Central Patient Registry",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://frontend:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Get API key from environment
REGISTRY_API_KEY = os.getenv("REGISTRY_API_KEY", "default_registry_key")


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key for registry access"""
    if x_api_key != REGISTRY_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    return x_api_key


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "central-patient-registry-mock",
        "version": "1.0.0",
        "total_patients": len(MOCK_PATIENTS)
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Central Patient Registry API (Mock)",
        "endpoints": {
            "health": "/health",
            "search_patient": "/api/registry/patients?national_id={id}"
        }
    }


@app.get("/api/registry/patients")
async def search_patient(
    national_id: str,
    api_key: str = Header(None, alias="X-API-Key")
):
    """
    Search for patient by National ID
    
    Args:
        national_id: Patient's national ID number
        api_key: API key for authentication
        
    Returns:
        Patient data from central registry
        
    Raises:
        HTTPException: If patient not found or invalid API key
    """
    # Verify API key
    if api_key != REGISTRY_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Search for patient
    patient = next(
        (p for p in MOCK_PATIENTS if p["national_id"] == national_id),
        None
    )
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with National ID {national_id} not found in registry"
        )
    
    return patient


@app.get("/api/registry/patients/{patient_id}")
async def get_patient_by_id(
    patient_id: str,
    api_key: str = Header(None, alias="X-API-Key")
):
    """
    Get patient by patient ID
    
    Args:
        patient_id: Patient's unique ID
        api_key: API key for authentication
        
    Returns:
        Patient data from central registry
        
    Raises:
        HTTPException: If patient not found or invalid API key
    """
    # Verify API key
    if api_key != REGISTRY_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    
    # Search for patient
    patient = next(
        (p for p in MOCK_PATIENTS if p["patient_id"] == patient_id),
        None
    )
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found in registry"
        )
    
    return patient