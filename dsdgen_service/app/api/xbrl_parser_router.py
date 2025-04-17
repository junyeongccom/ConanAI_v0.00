from fastapi import APIRouter, Query
from ..domain.controller.xbrl_parser_controller import XBRLParserController
from typing import Dict, Any

router = APIRouter(prefix="/xbrl-parser", tags=["XBRL Parser"])
controller = XBRLParserController()

@router.get("/balance-sheet")
def get_balance_sheet(
    rcept_no: str = Query(..., description="DART 접수번호 (예: 20250331002860_11011)")
) -> Dict[str, Any]:
    """
    접수번호를 기반으로 재무상태표 데이터를 JSON 형식으로 반환합니다.
    
    Args:
        rcept_no: DART 접수번호
        
    Returns:
        Dict[str, Any]: 재무상태표 데이터가 포함된 응답
    """
    result = controller.get_balance_sheet_dataframe(rcept_no)
    return result