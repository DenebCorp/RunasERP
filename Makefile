.PHONY: help up down logs restart clean migrate test lint seed build health

help: ## Mostra esta mensagem de ajuda
	@echo "ERP Runas - Comandos Disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

up: ## Sobe todos os serviços
	docker-compose up -d
	@echo "✓ Serviços iniciados"
	@echo "  - API Gateway: http://localhost:8000"
	@echo "  - RabbitMQ Management: http://localhost:15672"
	@echo "  - pgAdmin: http://localhost:5050"
	@echo "  - Evolution API: http://localhost:8080"

down: ## Para todos os serviços
	docker-compose down
	@echo "✓ Serviços parados"

logs: ## Mostra logs de todos os serviços
	docker-compose logs -f

logs-gateway: ## Mostra logs do API Gateway
	docker-compose logs -f api-gateway

logs-clientes: ## Mostra logs do serviço de clientes
	docker-compose logs -f clientes

logs-produtos: ## Mostra logs do serviço de produtos
	docker-compose logs -f produtos

logs-estoque: ## Mostra logs do serviço de estoque
	docker-compose logs -f estoque

logs-vendas: ## Mostra logs do serviço de vendas
	docker-compose logs -f vendas

logs-financeiro: ## Mostra logs do serviço financeiro
	docker-compose logs -f financeiro

logs-notificacoes: ## Mostra logs do serviço de notificações
	docker-compose logs -f notificacoes

restart: ## Reinicia todos os serviços
	docker-compose restart
	@echo "✓ Serviços reiniciados"

clean: ## Remove todos os containers, volumes e imagens
	docker-compose down -v --rmi all
	@echo "✓ Ambiente limpo"

build: ## Reconstrói todas as imagens
	docker-compose build --no-cache
	@echo "✓ Imagens reconstruídas"

migrate: ## Executa migrations em todos os serviços
	@echo "Executando migrations..."
	docker-compose exec api-gateway alembic upgrade head
	docker-compose exec clientes alembic upgrade head
	docker-compose exec produtos alembic upgrade head
	docker-compose exec estoque alembic upgrade head
	docker-compose exec vendas alembic upgrade head
	docker-compose exec financeiro alembic upgrade head
	docker-compose exec notificacoes alembic upgrade head
	@echo "✓ Migrations executadas"

migrate-create: ## Cria uma nova migration (uso: make migrate-create SERVICE=clientes MSG="mensagem")
	@if [ -z "$(SERVICE)" ]; then \
		echo "Erro: especifique o serviço com SERVICE=nome"; \
		exit 1; \
	fi
	@if [ -z "$(MSG)" ]; then \
		echo "Erro: especifique a mensagem com MSG='mensagem'"; \
		exit 1; \
	fi
	docker-compose exec $(SERVICE) alembic revision --autogenerate -m "$(MSG)"
	@echo "✓ Migration criada para $(SERVICE)"

test: ## Executa todos os testes
	@echo "Executando testes..."
	docker-compose exec api-gateway pytest -v --cov=. --cov-report=html
	docker-compose exec clientes pytest -v --cov=. --cov-report=html
	docker-compose exec produtos pytest -v --cov=. --cov-report=html
	docker-compose exec estoque pytest -v --cov=. --cov-report=html
	docker-compose exec vendas pytest -v --cov=. --cov-report=html
	docker-compose exec financeiro pytest -v --cov=. --cov-report=html
	docker-compose exec notificacoes pytest -v --cov=. --cov-report=html
	@echo "✓ Testes executados"

test-service: ## Executa testes de um serviço específico (uso: make test-service SERVICE=clientes)
	@if [ -z "$(SERVICE)" ]; then \
		echo "Erro: especifique o serviço com SERVICE=nome"; \
		exit 1; \
	fi
	docker-compose exec $(SERVICE) pytest -v --cov=. --cov-report=html
	@echo "✓ Testes executados para $(SERVICE)"

lint: ## Executa linting em todos os serviços
	@echo "Executando linting..."
	docker-compose exec api-gateway ruff check .
	docker-compose exec api-gateway mypy .
	docker-compose exec clientes ruff check .
	docker-compose exec clientes mypy .
	docker-compose exec produtos ruff check .
	docker-compose exec produtos mypy .
	docker-compose exec estoque ruff check .
	docker-compose exec estoque mypy .
	docker-compose exec vendas ruff check .
	docker-compose exec vendas mypy .
	docker-compose exec financeiro ruff check .
	docker-compose exec financeiro mypy .
	docker-compose exec notificacoes ruff check .
	docker-compose exec notificacoes mypy .
	@echo "✓ Linting executado"

seed: ## Popula banco com dados de teste
	@echo "Populando banco de dados..."
	docker-compose exec api-gateway python seed.py
	docker-compose exec clientes python seed.py
	docker-compose exec produtos python seed.py
	docker-compose exec estoque python seed.py
	@echo "✓ Dados de teste inseridos"

health: ## Verifica saúde de todos os serviços
	@echo "Verificando saúde dos serviços..."
	@curl -s http://localhost:8000/health | jq . || echo "❌ API Gateway"
	@curl -s http://localhost:8001/health | jq . || echo "❌ Clientes"
	@curl -s http://localhost:8002/health | jq . || echo "❌ Produtos"
	@curl -s http://localhost:8003/health | jq . || echo "❌ Estoque"
	@curl -s http://localhost:8004/health | jq . || echo "❌ Vendas"
	@curl -s http://localhost:8005/health | jq . || echo "❌ Financeiro"
	@curl -s http://localhost:8006/health | jq . || echo "❌ Notificações"

shell-gateway: ## Abre shell no container do API Gateway
	docker-compose exec api-gateway /bin/bash

shell-db: ## Abre psql no banco de dados (uso: make shell-db DB=clientes)
	@if [ -z "$(DB)" ]; then \
		echo "Erro: especifique o banco com DB=nome"; \
		exit 1; \
	fi
	docker-compose exec db-$(DB) psql -U erp -d $(DB)

ps: ## Lista todos os containers
	docker-compose ps

stats: ## Mostra estatísticas de uso dos containers
	docker stats

backup-db: ## Faz backup de todos os bancos de dados
	@echo "Fazendo backup dos bancos de dados..."
	@mkdir -p backups
	docker-compose exec db-gateway pg_dump -U erp gateway > backups/gateway_$$(date +%Y%m%d_%H%M%S).sql
	docker-compose exec db-clientes pg_dump -U erp clientes > backups/clientes_$$(date +%Y%m%d_%H%M%S).sql
	docker-compose exec db-produtos pg_dump -U erp produtos > backups/produtos_$$(date +%Y%m%d_%H%M%S).sql
	docker-compose exec db-estoque pg_dump -U erp estoque > backups/estoque_$$(date +%Y%m%d_%H%M%S).sql
	docker-compose exec db-vendas pg_dump -U erp vendas > backups/vendas_$$(date +%Y%m%d_%H%M%S).sql
	docker-compose exec db-financeiro pg_dump -U erp financeiro > backups/financeiro_$$(date +%Y%m%d_%H%M%S).sql
	docker-compose exec db-notificacoes pg_dump -U erp notificacoes > backups/notificacoes_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✓ Backups criados em ./backups/"

dev: ## Inicia ambiente de desenvolvimento
	@echo "Iniciando ambiente de desenvolvimento..."
	docker-compose up -d db-gateway db-clientes db-produtos db-estoque db-vendas db-financeiro db-notificacoes rabbitmq redis pgadmin
	@echo "✓ Infraestrutura iniciada"
	@echo "  Agora você pode rodar os serviços localmente"

stop-services: ## Para apenas os microsserviços (mantém infra)
	docker-compose stop api-gateway clientes produtos estoque vendas financeiro notificacoes celery-worker celery-beat

start-services: ## Inicia apenas os microsserviços
	docker-compose start api-gateway clientes produtos estoque vendas financeiro notificacoes celery-worker celery-beat
