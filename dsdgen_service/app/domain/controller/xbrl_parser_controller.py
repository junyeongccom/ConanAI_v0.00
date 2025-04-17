from ..service.xbrl_parser_service import XBRLParserService
from typing import Dict, Any

class XBRLParserController:
    def __init__(self):
        self.service = XBRLParserService()

    def get_balance_sheet_dataframe(self, rcept_no: str) -> Dict[str, Any]:
        """
        재무상태표 데이터를 DataFrame에서 JSON 형식으로 변환하여 반환합니다.
        
        Args:
            rcept_no: 접수번호
            
        Returns:
            Dict[str, Any]: 재무상태표 데이터
        """
        df = self.service.get_balance_sheet_dataframe(rcept_no)
        
        if df.empty:
            return {"success": False, "message": "데이터를 찾을 수 없습니다.", "data": []}
        
        # DataFrame을 JSON 형식으로 변환
        balance_sheet_data = df.to_dict(orient='records')
        
        return {
            "success": True,
            "message": f"재무상태표 데이터 {len(balance_sheet_data)}개 항목이 추출되었습니다.",
            "data": balance_sheet_data
        }
