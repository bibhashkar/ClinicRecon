from fastapi import APIRouter, Depends, HTTPException
from app.models.patient import ReconcileRequest, ReconcileResponse
from app.services.reconciliation import reconcile_medication

router = APIRouter()

def verify_api_key(api_key: str):
    from app.core.config import settings
    if api_key != settings.API_KEY:
        raise HTTPException(401, "Invalid API key")
    return api_key

@router.post("/reconcile/medication", response_model=ReconcileResponse)
async def reconcile_endpoint(request: ReconcileRequest, api_key: str = Depends(verify_api_key)):
    try:
        return await reconcile_medication(request)
    except Exception as e:
        raise HTTPException(500, f"Reconciliation failed: {str(e)}")