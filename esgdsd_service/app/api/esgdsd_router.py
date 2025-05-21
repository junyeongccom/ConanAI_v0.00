from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.domain.controller.esgdsd_controller import ESGDSDController
from typing import Dict, Any

router = APIRouter()
controller = ESGDSDController()

@router.get("/hello")
async def hello_world():
    """
    Hello World 테스트 엔드포인트
    """
    return {"message": "Hello from ESG DSD Service!"}

@router.post("/extract")
async def extract_text(
    file: UploadFile = File(...),
    page_num: int = Form(...)
) -> Dict[str, Any]:
    """
    PDF 파일에서 텍스트를 추출합니다.

    Args:
        file (UploadFile): 업로드된 PDF 파일
        page_num (int): 추출할 페이지 번호 (1-based)

    Returns:
        Dict[str, Any]: 추출된 텍스트 정보

    Raises:
        HTTPException: 파일 처리 중 오류가 발생한 경우
    """
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        if page_num < 1:
            raise HTTPException(status_code=400, detail="Page number must be greater than 0")
        
        return await controller.extract_text(file, page_num)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 