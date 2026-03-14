from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Literal
from datetime import date

class PatientContext(BaseModel):
    age: int = Field(..., ge=0, le=120)
    conditions: List[str]
    recent_labs: Optional[Dict[str, float]] = None

class Source(BaseModel):
    system: str
    medication: str
    last_updated: Optional[str] = None
    last_filled: Optional[str] = None
    source_reliability: Literal["high", "medium", "low"]

class ReconcileRequest(BaseModel):
    patient_context: PatientContext
    sources: List[Source] = Field(..., min_items=1)

class ReconcileResponse(BaseModel):
    reconciled_medication: str
    confidence_score: float = Field(..., ge=0, le=1)
    reasoning: str
    recommended_actions: List[str]
    clinical_safety_check: str

class DataQualityRecord(BaseModel):
    demographics: Dict
    medications: List[str]
    allergies: List[str]
    conditions: List[str]
    vital_signs: Dict
    last_updated: str

class DataQualityResponse(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    breakdown: Dict[str, int]
    issues_detected: List[Dict[str, str]]