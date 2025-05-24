# SKYC 마이크로서비스 아키텍처

이 프로젝트는 마이크로서비스 아키텍처를 기반으로 한 SKYC 시스템입니다.

## 프로젝트 구조

```
SKYC/
├── gateway_service/     # API Gateway (8080)
├── stocktrend_service/  # 주식 트렌드 분석 서비스 (8082)
├── irsummary_service/   # IR 리포트 분석 및 요약 서비스 (8083)
├── esgdsd_service/      # ESG DSD 생성 서비스 (8084)
├── dsdgen_service/      # 재무상태표 DSD 생성 서비스 (8085)
├── chatbot-service/     # 챗봇 서비스 (8082)
├── docker-compose.yml   # 전체 서비스 배포 설정
└── Makefile            # 서비스별 빌드 및 실행 명령어
```

## 기술 스택

- Python
- FastAPI
- Docker
- Docker Compose
- PostgreSQL
- ML/AI (PyTorch, OpenCV, Tesseract)
- PDF Processing (Camelot, pdfplumber)
- OpenAI GPT-3.5-turbo

## 개발 환경 설정

### 필수 요구사항

- Docker
- Docker Compose
- Python 3.8 이상
- Make
- Tesseract OCR
- Poppler-utils

### 환경 설정

1. 저장소 클론
```bash
git clone [repository-url]
cd SKYC
```

2. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 필요한 환경 변수를 설정
```

3. 서비스별 빌드 및 실행
```bash
# 전체 서비스 빌드 및 실행
make up

# 특정 서비스만 빌드 및 실행
make build-gateway
make up-gateway

# IR Summary 서비스 실행
make build-irsummary
make up-irsummary

# 특정 서비스 로그 확인
make logs-gateway
make logs-irsummary
```

## 서비스별 포트

- Gateway Service: 8080
- StockTrend Service: 8082
- IRSummary Service: 8083
- ESGDSD Service: 8084
- DSDGen Service: 8085
- Chatbot Service: 8082

## API 문서

각 서비스의 API 문서는 다음 URL에서 확인할 수 있습니다:
- http://localhost:8080/docs (Gateway Service)
- http://localhost:8082/docs (StockTrend Service)
- http://localhost:8083/docs (IRSummary Service)
- http://localhost:8084/docs (ESGDSD Service)
- http://localhost:8085/docs (DSDGen Service)

## 서비스별 기능

### IRSummary Service (8083)
IR 리포트 PDF 파일을 업로드하여 다음 정보를 자동 추출합니다:
- 투자 의견, 목표주가, 타겟 PER
- 2Q24 / 2025 / 2026 실적 전망 수치
- 주요 요약 내용 (GPT-3.5-turbo 기반)

**주요 기능:**
- PDF 표 추출 (Camelot, pdfplumber)
- Rule 기반 주요 지표 파싱
- OpenAI API를 통한 자연어 요약
- JSON 형태로 구조화된 데이터 반환

**실행 방법:**
```bash
# IRSummary 서비스만 빌드 및 실행
make build-irsummary
make up-irsummary

# 로그 확인
make logs-irsummary

# 서비스 중지
make down-irsummary

# 서비스 재시작
make restart-irsummary
```

## 개발 가이드

### 새로운 기능 개발

1. 기능 브랜치 생성
```bash
git checkout -b feature/[기능명]
```

2. 개발 및 테스트
3. PR 생성 및 코드 리뷰
4. 메인 브랜치 머지

### 코드 스타일

- PEP 8 스타일 가이드 준수
- Black 포맷터 사용
- Flake8 린터 사용

## 배포

### 개발 환경

```bash
make up
```

### 프로덕션 환경

```bash
make prod
```

## 문제 해결

문제가 발생한 경우 다음 명령어로 로그를 확인할 수 있습니다:

```bash
make logs-[service-name]
make logs-irsummary
```

## 라이센스

[라이센스 정보] 