FROM python:3.10-slim

# 1. 작업 디렉토리 설정
WORKDIR /app

# 2. requirements 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 실제 앱 코드만 복사 (app/ 폴더 내부 내용만 /app/에 복사됨)
COPY . .

# 4. 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8087"]
