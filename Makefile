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
	docker-compose stop gateway && docker-compose up -d gateway

## user
build-user:
	docker-compose build user

up-user:
	docker-compose up -d user

down-user:
	docker-compose stop user

logs-user:
	docker-compose logs -f user

restart-user:
	docker-compose stop user && docker-compose up -d user

## company
build-company:
	docker-compose build company

up-company:
	docker-compose up -d company

down-company:
	docker-compose stop company

logs-company:
	docker-compose logs -f company

restart-company:
	docker-compose stop company && docker-compose up -d company

## actlog
build-actlog:
	docker-compose build actlog

up-actlog:
	docker-compose up -d actlog

down-actlog:
	docker-compose stop actlog

logs-actlog:
	docker-compose logs -f actlog

restart-actlog:
	docker-compose stop actlog && docker-compose up -d actlog

## finreport
build-finreport:
	docker-compose build finreport

up-finreport:
	docker-compose up -d finreport

down-finreport:
	docker-compose stop finreport

logs-finreport:
	docker-compose logs -f finreport

restart-finreport:
	docker-compose stop finreport && docker-compose up -d finreport

## xbrlgen
build-xbrlgen:
	docker-compose build xbrlgen

up-xbrlgen:
	docker-compose up -d xbrlgen

down-xbrlgen:
	docker-compose stop xbrlgen

logs-xbrlgen:
	docker-compose logs -f xbrlgen

restart-xbrlgen:
	docker-compose stop xbrlgen && docker-compose up -d xbrlgen

