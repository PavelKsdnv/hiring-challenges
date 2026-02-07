from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health", response_model=dict[str, str]) # pesho add more specific dict maybe something from Pydantic?
async def get_health():
    return {"status": "ok"} # pesho maybe a better health checking logic