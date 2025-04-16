import os
import requests
import zipfile
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
API_KEY = os.getenv("DART_API_KEY")
SAVE_DIR = Path("/app/app/dart_documents")
EXTRACT_DIR = SAVE_DIR / "extracted"

class OpenDartRepository:
    def __init__(self):
        self.api_key = API_KEY
        self.save_dir = SAVE_DIR
        self.extract_dir = EXTRACT_DIR
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.extract_dir.mkdir(parents=True, exist_ok=True)
        # API 키 확인 로깅
        print(f"[INFO] API Key 설정됨: {'*' * 5}{API_KEY[-5:] if API_KEY else 'NOT SET'}")
        print(f"[INFO] 저장 경로: {self.save_dir}")
        print(f"[INFO] 압축 해제 경로: {self.extract_dir}")

    def download_xbrl_zip(self, rcept_no: str, reprt_code: str = "11011", filename: str = None, auto_extract: bool = True, delete_zip: bool = False) -> str:
        """
        OpenDART에서 지정된 접수번호(rcept_no)의 XBRL zip 파일을 다운로드하고 저장함
        auto_extract: 다운로드 후 자동으로 압축 해제할지 여부
        delete_zip: 압축 해제 후 원본 ZIP 파일을 삭제할지 여부
        """
        url = f"https://opendart.fss.or.kr/api/fnlttXbrl.xml"
        params = {
            "crtfc_key": self.api_key,
            "rcept_no": rcept_no,
            "reprt_code": reprt_code
        }

        print(f"[INFO] API 요청: {url}, 파라미터: {params}")

        response = requests.get(url, params=params, stream=True)
        content_type = response.headers.get("Content-Type", "")
        
        # 모든 응답 정보 로깅
        debug_msg = (
            f"[DEBUG] 응답 정보\n"
            f"- 상태 코드: {response.status_code}\n"
            f"- 응답 타입: {content_type}\n"
            f"- 헤더: {response.headers}\n"
            f"- 데이터 크기: {len(response.content)} bytes\n"
            f"- 응답 시작 부분: {response.content[:100]}"
        )
        print(debug_msg)
        
        # 응답 상태 코드만 확인하고 컨텐츠 타입 검사 제거
        if response.status_code != 200:
            raise Exception(f"OpenDART API 응답 에러: {response.status_code}")

        if filename is None:
            filename = f"{rcept_no}_{reprt_code}.zip"

        save_path = self.save_dir / filename
        with open(save_path, "wb") as f:
            f.write(response.content)

        print(f"[INFO] 파일 저장 완료: {save_path}")
        
        # 압축 해제 진행
        extract_path = None
        if auto_extract:
            extract_path = self._extract_zip_file(save_path, delete_zip)
            return extract_path
        
        return str(save_path)
    
    def _extract_zip_file(self, zip_path: Path, delete_zip: bool = False) -> str:
        """
        ZIP 파일을 압축 해제하고 추출된 파일 경로를 반환
        """
        if not zip_path.exists():
            raise FileNotFoundError(f"ZIP 파일이 존재하지 않습니다: {zip_path}")
        
        # 압축 해제할 디렉토리 생성
        extract_folder = zip_path.stem  # .zip 확장자 제외한 파일명
        extract_dir = self.extract_dir / extract_folder
        extract_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # 압축 해제
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            print(f"[INFO] 압축 해제 완료: {extract_dir}")
            
            # 압축 해제 후 원본 ZIP 파일 삭제 옵션이 활성화된 경우
            if delete_zip:
                os.remove(zip_path)
                print(f"[INFO] 원본 ZIP 파일 삭제 완료: {zip_path}")
            
            # 추출된 파일 목록 확인
            extracted_files = list(extract_dir.glob("*"))
            print(f"[INFO] 추출된 파일 수: {len(extracted_files)}")
            
            return str(extract_dir)
            
        except Exception as e:
            print(f"[ERROR] 압축 해제 중 오류 발생: {e}")
            raise