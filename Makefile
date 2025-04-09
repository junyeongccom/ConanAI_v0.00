# HC_MSA/Makefile
##사용예시
# make build-oauth       # OAuth 서비스 빌드
# make up-logging        # Logging 서비스 실행
# make logs-gateway      # Gateway 로그 보기
# make clean             # 전체 컨테이너 + 볼륨 정리



DOCKER_COMPOSE = docker compose -f docker-compose.yml

# -------------------------------
# 🚀 Build (서비스별)
# -------------------------------

build-gateway:
	$(DOCKER_COMPOSE) build gateway

build-oauth:
	$(DOCKER_COMPOSE) build oauth

build-logging:
	$(DOCKER_COMPOSE) build logging

build-disclosure:
	$(DOCKER_COMPOSE) build disclosure

build-companies:
	$(DOCKER_COMPOSE) build companies

build-roles:
	$(DOCKER_COMPOSE) build roles

build-audit:
	$(DOCKER_COMPOSE) build audit

build-chatbot:
	$(DOCKER_COMPOSE) build chatbot

build-esg:
	$(DOCKER_COMPOSE) build esg

build-all:
	$(DOCKER_COMPOSE) build

# -------------------------------
# 🔼 Up (서비스 실행)
# -------------------------------

up-gateway:
	$(DOCKER_COMPOSE) up gateway

up-oauth:
	$(DOCKER_COMPOSE) up oauth

up-logging:
	$(DOCKER_COMPOSE) up logging

up-disclosure:
	$(DOCKER_COMPOSE) up disclosure

up-companies:
	$(DOCKER_COMPOSE) up companies

up-roles:
	$(DOCKER_COMPOSE) up roles

up-audit:
	$(DOCKER_COMPOSE) up audit

up-chatbot:
	$(DOCKER_COMPOSE) up chatbot

up-esg:
	$(DOCKER_COMPOSE) up esg

up-all:
	$(DOCKER_COMPOSE) up

# -------------------------------
# 🔻 Down (모든 서비스 중지)
# -------------------------------

down:
	$(DOCKER_COMPOSE) down

# -------------------------------
# 🔁 Restart (서비스별)
# -------------------------------

restart-gateway:
	$(DOCKER_COMPOSE) restart gateway

restart-oauth:
	$(DOCKER_COMPOSE) restart oauth

restart-logging:
	$(DOCKER_COMPOSE) restart logging

restart-all:
	$(DOCKER_COMPOSE) restart

# -------------------------------
# 📋 Logs (서비스별)
# -------------------------------

logs-gateway:
	$(DOCKER_COMPOSE) logs -f gateway

logs-oauth:
	$(DOCKER_COMPOSE) logs -f oauth

logs-logging:
	$(DOCKER_COMPOSE) logs -f logging

logs-all:
	$(DOCKER_COMPOSE) logs -f

# -------------------------------
# 🧼 Clean (volume 포함 삭제)
# -------------------------------

clean:
	$(DOCKER_COMPOSE) down -v --remove-orphans
