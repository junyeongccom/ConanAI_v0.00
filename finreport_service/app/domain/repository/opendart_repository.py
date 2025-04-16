import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
API_KEY = os.getenv("DART_API_KEY")
SAVE_DIR = Path("/app/app/dart_documents")

class OpenDartRepository:
    def __init__(self):
        self.api_key = API_KEY
        self.save_dir = SAVE_DIR
        self.save_dir.mkdir(parents=True, exist_ok=True)
        # API 키 확인 로깅
        print(f"[INFO] API Key 설정됨: {'*' * 5}{API_KEY[-5:] if API_KEY else 'NOT SET'}")
        print(f"[INFO] 저장 경로: {self.save_dir}")

    def download_xbrl_zip(self, rcept_no: str, reprt_code: str = "11011", filename: str = None) -> str:
        """
        OpenDART에서 지정된 접수번호(rcept_no)의 XBRL zip 파일을 다운로드하고 저장함
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
        return str(save_path)