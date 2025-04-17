import os
import shutil
from datetime import datetime

UPLOAD_DIR = "uploads"

class XBRLGenService:
    async def save_uploaded_excel_file(self, file):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "filename": filename,
            "message": "업로드 성공!"
        }
