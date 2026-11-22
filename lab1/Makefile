# ЛР1 — Контейнерні мережі Docker
#   make       — стягнути образи, зібрати й запустити основне завдання
#   make help  — список усіх команд

COMPOSE     := docker compose -f docker-compose.yml
COMPOSE_ADV := docker compose -f docker-compose.advanced.yml
NETSHOOT    := nicolaka/netshoot:v0.13@sha256:a20c2531bf35436ed3766cd6cfe89d352b050ccc4d7005ce6400adf97503da1b
URL         := http://localhost:8080/

.DEFAULT_GOAL := all
.PHONY: all help pull build up ps logs test down clean \
        adv adv-up adv-ps adv-test adv-down reset

all: up test ## Стягнути образи, зібрати app, запустити і перевірити (основне)

help: ## Показати цю довідку
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

pull: ## Стягнути всі образи з Docker Hub (nginx, redis, python, netshoot)
	$(COMPOSE) pull --ignore-buildable
	docker pull python:3.12.16-alpine@sha256:c5ba3deef00c7758561a0f03c26f44f10589263d40e732b8748e0d1f38f6dd89
	docker pull $(NETSHOOT)

build: ## Зібрати образ застосунку lab1-app:1.0
	$(COMPOSE) build

up: pull build ## Запустити основну топологію (proxy -> app -> db)
	@$(COMPOSE_ADV) down -v 2>/dev/null || true
	$(COMPOSE) up -d
	$(COMPOSE) ps

ps: ## Стан контейнерів основної топології
	$(COMPOSE) ps

logs: ## Логи основної топології (Ctrl+C — вихід)
	$(COMPOSE) logs -f

test: ## Перевірити: застосунок доступний через proxy, порти app/db закриті
	@echo "--- Чекаю, поки proxy відповість..."
	@for i in $$(seq 1 20); do curl -sf $(URL) >/dev/null && break; sleep 1; done
	@echo "--- Запит через proxy ($(URL)):"
	@curl -s $(URL)
	@echo "--- Порти app (8000) і db (6379) з хоста мають бути закриті:"
	@curl -s --max-time 2 http://localhost:8000/ >/dev/null && echo "  8000 ВІДКРИТИЙ (помилка!)" || echo "  8000 закритий — OK"
	@curl -s --max-time 2 http://localhost:6379/ >/dev/null && echo "  6379 ВІДКРИТИЙ (помилка!)" || echo "  6379 закритий — OK"

down: ## Зупинити й видалити основну топологію (разом з мережею і томами)
	$(COMPOSE) down -v

adv: adv-up adv-test ## Стягнути, зібрати, запустити й перевірити додаткове завдання

adv-up: pull build ## Запустити розширену топологію (frontend/backend, 2 репліки, healthcheck)
	@$(COMPOSE) down -v 2>/dev/null || true
	@$(COMPOSE_ADV) down -v 2>/dev/null || true
	$(COMPOSE_ADV) up -d --wait
	$(COMPOSE_ADV) ps

adv-ps: ## Стан контейнерів розширеної топології
	$(COMPOSE_ADV) ps

adv-test: ## Кілька запитів через proxy — видно чергування реплік app
	@for i in 1 2 3 4 5 6; do curl -s $(URL); done

adv-down: ## Зупинити розширену топологію
	$(COMPOSE_ADV) down -v

clean: down adv-down ## Прибрати все: обидві топології + ручні контейнери/мережу з кроків 3–8
	-docker rm -f proxy app db 2>/dev/null
	-docker network rm lab1-net 2>/dev/null

reset: clean all ## Повне відтворення з нуля (для скріну «відтворюваність»)
