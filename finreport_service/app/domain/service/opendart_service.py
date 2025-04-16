from ..repository.opendart_repository import OpenDartRepository

class OpenDartService:
    def __init__(self):
        self.repository = OpenDartRepository()

    def fetch_and_store_xbrl(self, rcept_no: str, reprt_code: str, auto_extract: bool = True, delete_zip: bool = True) -> str:
        """
        XBRL ZIP 파일 다운로드 후 저장 경로 반환
        auto_extract: 다운로드 후 자동으로 압축 해제할지 여부 (기본값: True)
        delete_zip: 압축 해제 후 원본 ZIP 파일을 삭제할지 여부 (기본값: True)
        
        반환값: 
        - auto_extract가 True이면 압축 해제된 디렉토리 경로 반환
        - auto_extract가 False이면 다운로드된 ZIP 파일 경로 반환
        """
        return self.repository.download_xbrl_zip(
            rcept_no=rcept_no, 
            reprt_code=reprt_code,
            auto_extract=auto_extract,
            delete_zip=delete_zip
        )
