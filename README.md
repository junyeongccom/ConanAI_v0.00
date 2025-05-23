# SKYC 마이크로서비스 아키텍처

이 프로젝트는 마이크로서비스 아키텍처를 기반으로 한 SKYC 시스템입니다.

## 프로젝트 구조

```
SKYC/
├── gateway_service/     # API Gateway (8080)
├── actlog_service/      # 활동 로그 관리 서비스 (8081)
├── company_service/     # 기업 관리 서비스 (8083)
├── esgdsd_service/      # ESG DSD 생성 서비스 (8084)
├── dsdgen_service/      # 재무상태표 DSD 생성 서비스 (8085)
├── user_service/        # 사용자 관리 서비스 (8086)
├── xbrlgen_service/     # XBRL 문서 생성 서비스 (8087)
├── n8n_service/         # n8n 워크플로우 자동화 서비스 (8088)
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
make all

# 특정 서비스만 빌드 및 실행
make build-user
make up-user

# 특정 서비스 로그 확인
make logs-user
```

## 서비스별 포트

- Gateway Service: 8080
- ActLog Service: 8081
- Company Service: 8083
- ESGDSD Service: 8084
- DSDGen Service: 8085
- User Service: 8086
- XBRLGen Service: 8087
- N8N Service: 8088

## API 문서

각 서비스의 API 문서는 다음 URL에서 확인할 수 있습니다:
- http://localhost:8080/docs (Gateway Service)
- http://localhost:8081/docs (ActLog Service)
- http://localhost:8083/docs (Company Service)
- http://localhost:8084/docs (ESGDSD Service)
- http://localhost:8085/docs (DSDGen Service)
- http://localhost:8086/docs (User Service)
- http://localhost:8087/docs (XBRLGen Service)
- http://localhost:8088/docs (N8N Service)

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
make all
```

### 프로덕션 환경

```bash
make prod
```

## 문제 해결

문제가 발생한 경우 다음 명령어로 로그를 확인할 수 있습니다:

```bash
make logs-[service-name]
```

## 라이센스

[라이센스 정보] 