from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.patient import ReconcileRequest, ReconcileResponse, DataQualityRecord, DataQualityResponse
from app.services.reconciliation import reconcile_medication
from app.services.data_quality import validate_data_quality

router = APIRouter()

def verify_api_key(api_key: str):
    from app.core.config import settings
    if api_key != settings.API_KEY:
        raise HTTPException(401, "Invalid API key")
    return api_key

@router.post("/reconcile/medication", response_model=ReconcileResponse)
async def reconcile_endpoint(request: ReconcileRequest
                            #  , api_key: str = Depends(verify_api_key)
                             ):
    try:
        print(request.dict())
        return await reconcile_medication(request)
    except Exception as e:
        raise HTTPException(500, f"Reconciliation failed: {str(e)}")

@router.post("/validate/data-quality", response_model=DataQualityResponse)
async def validate_data_quality_endpoint(record: DataQualityRecord
                                        #  , api_key: str = Depends(verify_api_key)
                                         ):
    try:
        return await validate_data_quality(record)
    except Exception as e:
        raise HTTPException(500, f"Data quality validation failed: {str(e)}")