# 모든 명령어 앞에 'make' 를 붙여서 실행해야 함
# 🔧 공통 명령어
up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose down && docker-compose up -d --build

ps:
	docker-compose ps


# 🚀 마이크로서비스별 명령어

## gateway
build-gateway:
	docker-compose build gateway

up-gateway:
	docker-compose up -d gateway

down-gateway:
	docker-compose stop gateway

logs-gateway:
	docker-compose logs -f gateway

restart-gateway:
	docker-compose down gateway && docker-compose up -d --build gateway

## stocktrend
build-stocktrend:
	docker-compose build stocktrend

up-stocktrend:
	docker-compose up -d stocktrend

down-stocktrend:
	docker-compose stop stocktrend

logs-stocktrend:
	docker-compose logs -f stocktrend

restart-stocktrend:
	docker-compose down stocktrend && docker-compose up -d --build stocktrend


## dsdgen
build-dsdgen:
	docker-compose build dsdgen

up-dsdgen:
	docker-compose up -d dsdgen

down-dsdgen:
	docker-compose stop dsdgen

logs-dsdgen:
	docker-compose logs -f dsdgen

restart-dsdgen:
	docker-compose down dsdgen && docker-compose up -d --build dsdgen

## esgdsd
build-esgdsd:
	docker-compose build esgdsd

up-esgdsd:
	docker-compose up -d esgdsd

down-esgdsd:
	docker-compose stop esgdsd

logs-esgdsd:
	docker-compose logs -f esgdsd

restart-esgdsd:
	docker-compose down esgdsd && docker-compose up -d --build esgdsd

## chatbot
build-chatbot:
	docker-compose build chatbot

up-chatbot:
	docker-compose up -d chatbot

down-chatbot:
	docker-compose stop chatbot

logs-chatbot:
	docker-compose logs -f chatbot

restart-chatbot:
	docker-compose down chatbot && docker-compose up -d --build chatbot

## n8n
n8n_build:
	docker-compose build n8n

n8n_up:
	docker-compose up -d n8n

n8n_down:
	docker-compose stop n8n

n8n_logs:
	docker-compose logs -f n8n

n8n_restart:
	docker-compose down n8n && docker-compose up -d --build n8n


