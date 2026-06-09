from fastapi import APIRouter, Depends
from api.auth import get_current_admin

router = APIRouter()

@router.post("/index/all")
async def index_all(admin: dict = Depends(get_current_admin)):
    # Trigger full index
    return {"message": "Full re-index started"}

@router.post("/index/source/{source_id}")
async def index_source(source_id: str, admin: dict = Depends(get_current_admin)):
    # Trigger source index
    return {"message": f"Re-index started for {source_id}"}
