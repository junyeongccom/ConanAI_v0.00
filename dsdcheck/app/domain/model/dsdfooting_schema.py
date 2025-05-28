from pydantic import BaseModel
from typing import List, Optional, Dict

class FootingResultItem(BaseModel):
    """개별 검증 항목 결과"""
    item: str
    expected: Optional[float] = None
    actual: Optional[float] = None
    is_match: bool
    children: Optional[List['FootingResultItem']] = None

class YearlyFootingSheetResult(BaseModel):
    """시트별 연도별 검증 결과"""
    sheet: str
    title: str
    results_by_year: Dict[str, List[FootingResultItem]]

class FootingResponse(BaseModel):
    """전체 검증 결과 응답"""
    results: List[YearlyFootingSheetResult]
    total_sheets: int
    mismatch_count: int
