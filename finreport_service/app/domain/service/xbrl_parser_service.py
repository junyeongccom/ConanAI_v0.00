from ..repository.xbrl_parser_repository import XBRLParserRepository

class XBRLParserService:
    def __init__(self):
        self.repository = XBRLParserRepository()

    def filter_balance_sheet_tags(self, xbrl_filename: str, rcept_no: str) -> list[str]:
        # 먼저 태그를 추출
        tags = self.repository.get_balance_sheet_tags(xbrl_filename, rcept_no)
        
        # 추가로 데이터프레임 추출 (콘솔 출력용)
        print("\n[INFO] 재무상태표 데이터프레임 추출 시작...")
        try:
            df = self.repository.extract_balance_sheet_dataframe(xbrl_filename, rcept_no)
            print(f"[INFO] 데이터프레임 추출 성공! 총 {len(df)}개 항목")
        except Exception as e:
            print(f"[ERROR] 데이터프레임 추출 중 오류 발생: {e}")
        
        # 원래 반환값인 태그 목록 반환
        return tags