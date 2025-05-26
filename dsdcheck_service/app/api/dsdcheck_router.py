from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"message": "Hello World from dsdcheck_service"} 