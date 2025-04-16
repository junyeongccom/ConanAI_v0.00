import zipfile
from pathlib import Path

class XBRLParserRepository:
    def __init__(self):
        # 도커 컨테이너에서의 볼륨 마운트 경로로 수정
        self.zip_root = Path("/app/app/dart_documents")
        self.extract_root = self.zip_root / "extracted"
        self.extract_root.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] ZIP 파일 저장 경로: {self.zip_root}")
        print(f"[INFO] 압축 해제 경로: {self.extract_root}")

    def unzip_xbrl_files(self, zip_filename: str) -> list[str]:
        # 확장자 확인 및 추가
        if not zip_filename.lower().endswith('.zip'):
            zip_filename = f"{zip_filename}.zip"
        
        zip_path = self.zip_root / zip_filename
        print(f"[INFO] 압축 해제할 파일 경로: {zip_path}")
        
        if not zip_path.exists():
            raise FileNotFoundError(f"ZIP 파일이 존재하지 않습니다: {zip_path}")

        extract_folder = zip_filename.replace(".zip", "")
        extract_dir = self.extract_root / extract_folder
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            print(f"[INFO] 압축 해제 완료: {extract_dir}")

        # 추출된 파일 목록 반환
        extracted_files = [str(p.name) for p in extract_dir.glob("*") if p.is_file()]
        print(f"[INFO] 추출된 파일: {extracted_files}")
        return extracted_files