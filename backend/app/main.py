from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.handler import router as reconcile_router
# add validate_router

app = FastAPI(title="Onye Clinical Data Reconciliation Engine")

# Allow browser-based frontends (e.g. Vite dev server) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reconcile_router, prefix="/api")
# include validate

@app.get("/")
async def health():
    return {"status": "healthy", "message": "Onye Reconciliation Engine ready"}