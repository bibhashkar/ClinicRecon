from fastapi import FastAPI
from app.api.v1.reconcile import router as reconcile_router
# add validate_router

app = FastAPI(title="Onye Clinical Data Reconciliation Engine")

app.include_router(reconcile_router, prefix="/api")
# include validate

@app.get("/")
async def health():
    return {"status": "healthy", "message": "Onye Reconciliation Engine ready"}