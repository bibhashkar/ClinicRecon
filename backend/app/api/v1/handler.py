from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.patient import ReconcileRequest, ReconcileResponse, DataQualityRecord, DataQualityResponse
from app.services.reconciliation import reconcile_medication
from app.services.data_quality import validate_data_quality
from app.llm.client import LLMRateLimitError

router = APIRouter()

@router.post("/reconcile/medication", response_model=ReconcileResponse)
async def reconcile_endpoint(request: ReconcileRequest):
    try:
        return await reconcile_medication(request)
    except LLMRateLimitError as e:
        raise HTTPException(429, f"LLM rate limit exceeded: {str(e)}")
    except Exception as e:
        raise HTTPException(500, f"Reconciliation failed: {str(e)}")

@router.post("/validate/data-quality", response_model=DataQualityResponse)
async def validate_data_quality_endpoint(record: DataQualityRecord):
    try:
        return await validate_data_quality(record)
    except LLMRateLimitError as e:
        raise HTTPException(429, f"LLM rate limit exceeded: {str(e)}")
    except Exception as e:
        raise HTTPException(500, f"Data quality validation failed: {str(e)}")