import os
import shutil
from datetime import datetime
import pandas as pd  # ✅ pandas 추가

from fastapi import UploadFile  # 타입 명시용 (선택)

UPLOAD_DIR = "uploads"

class XBRLGenService:
    async def save_uploaded_excel_file(self, file: UploadFile):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        # 파일 저장
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ 저장된 파일을 DataFrame으로 읽기
        df = self.read_excel(filepath)

        return {
            "filename": filename,
            "columns": df.columns.tolist(),  # ✅ 확인용 컬럼 리스트 반환
            "message": "엑셀 업로드 + 파싱 성공!"
        }

    def read_excel(self, path: str) -> pd.DataFrame:
        """엑셀 파일 경로를 받아 DataFrame으로 읽는 메서드"""
        return pd.read_excel(path)
