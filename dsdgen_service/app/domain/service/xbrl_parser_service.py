from ..repository.xbrl_parser_repository import XBRLParserRepository
import pandas as pd

class XBRLParserService:
    def __init__(self):
        self.repository = XBRLParserRepository()

    def get_balance_sheet_dataframe(self, rcept_no: str) -> pd.DataFrame:
        """
        접수번호를 기반으로 재무상태표 데이터를 DataFrame으로 반환합니다.
        
        Args:
            rcept_no: 접수번호 (예: 20250331002860_11011)
            
        Returns:
            pandas.DataFrame: 재무상태표 데이터프레임 (항목명(한글), 값, 연도, 단위 포함)
        """
        print(f"[INFO] 접수번호 {rcept_no}에 대한 재무상태표 데이터프레임 추출 시작...")
        
        try:
            # 재무상태표 데이터프레임 추출
            df = self.repository.extract_balance_sheet_dataframe(rcept_no)
            print(f"[INFO] 데이터프레임 추출 성공! 총 {len(df)}개 항목")
            
            # DataFrame 반환
            return df
            
        except Exception as e:
            print(f"[ERROR] 데이터프레임 추출 중 오류 발생: {e}")
            # 오류 발생 시 빈 DataFrame 반환
            return pd.DataFrame()
            
