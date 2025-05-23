from fastapi import APIRouter
from ..domain.controller.stocktrend_controller import StocktrendController

router = APIRouter(
    prefix="/stocktrend",
    tags=["stocktrend"]
)

@router.get("/hello")
async def get_hello():
    controller = StocktrendController()
    return await controller.get_hello()
