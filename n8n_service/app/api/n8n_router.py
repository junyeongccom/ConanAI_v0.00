from fastapi import APIRouter

router = APIRouter(prefix="/n8n")

@router.get("/hello")
async def hello_world():
    return {"message": "hello world"}
