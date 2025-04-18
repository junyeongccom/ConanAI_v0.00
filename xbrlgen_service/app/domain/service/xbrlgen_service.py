import os
import shutil
from datetime import datetime
import pandas as pd
from app.domain.service.xbrl_converter import XBRLConverter
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

class XBRLGenService:
    async def save_uploaded_excel_file(self, file: UploadFile):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        # 1️⃣ 파일 저장
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2️⃣ 연결재무상태표 시트 파싱 (sheet name: D210000)
        data = self.parse_balance_sheet(filepath)

        # 3. XBRL(XML)로 변환하여 저장
        converter = XBRLConverter()
        xbrl_path = converter.convert_to_xbrl(data, filename)

        return {
            "filename": filename,
            "sheet": "D210000",
            "data": data,
            "xbrl_path": xbrl_path,
            "message": "엑셀 업로드 + 연결재무상태표 파싱 + XBRL 생성 성공!"
        }

    def parse_balance_sheet(self, path: str) -> list:
        try:
            # D210000 시트를 skiprows=5로 읽고 데이터 클렌징
            df = pd.read_excel(path, sheet_name="D210000", skiprows=5)

            # 계정과목 없는 행 제거
            df = df.dropna(subset=[df.columns[0]])

            # 컬럼 정리: 첫 번째 컬럼은 계정과목, 나머지는 연도
            df.columns = ["계정과목"] + [str(col) for col in df.columns[1:]]

            # NaN → 빈 문자열 처리
            df = df.fillna("")

            return df.to_dict(orient="records")

        except Exception as e:
            print("❌ 파싱 실패:", e)
            return []
