from ..repository.opendart_repository import OpenDartRepository

class OpenDartService:
    def __init__(self):
        self.repository = OpenDartRepository()

    def fetch_and_store_xbrl(self, rcept_no: str, reprt_code: str) -> str:
        """
        XBRL ZIP 파일 다운로드 후 저장 경로 반환
        """
        return self.repository.download_xbrl_zip(rcept_no=rcept_no, reprt_code=reprt_code)
