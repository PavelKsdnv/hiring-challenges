from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health", response_model=dict[str, str])
async def get_health():
    return {"status": "ok"}