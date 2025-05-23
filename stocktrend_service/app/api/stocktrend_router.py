from fastapi import APIRouter, UploadFile, File
from ..domain.controller.stocktrend_controller import StocktrendController
from typing import Optional

router = APIRouter()

@router.get("/hello")
async def get_hello():
    controller = StocktrendController()
    return await controller.get_hello()

@router.post("/report", summary="Upload PDF report")
async def upload_report(
    file: UploadFile = File(..., description="PDF file to upload"),
    description: Optional[str] = None
):
    """
    Upload a PDF report file for processing
    
    Args:
        file: PDF file
        description: Optional description of the report
    
    Returns:
        dict: Processing result with file info
    """
    if not file.content_type == "application/pdf":
        return {"error": "Only PDF files are allowed"}
    
    controller = StocktrendController()
    result = await controller.process_report(file, description)
    return result
