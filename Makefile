# TradeForge AaaS - Makefile
# Author: Ary HH
# Email: cateryatechnology@proton.me
# GitHub: https://github.com/cateryatechnology
# © 2026

.PHONY: help install start stop restart logs clean test format lint

help: ## Show this help message
	@echo "════════════════════════════════════════════════════════════════"
	@echo "   TradeForge AaaS - Available Commands"
	@echo "════════════════════════════════════════════════════════════════"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

install: ## Install dependencies using Poetry
	@echo "📦 Installing backend dependencies..."
	cd backend && poetry install
	@echo "📦 Installing frontend dependencies..."
	cd frontend && pip install -r requirements.txt
	@echo "✅ Dependencies installed"

start: ## Start all services with Docker Compose
	@echo "🚀 Starting TradeForge AaaS..."
	cd docker && docker-compose up -d
	@echo "✅ Services started"
	@echo "   Frontend: http://localhost:8501"
	@echo "   Backend:  http://localhost:8000"
	@echo "   API Docs: http://localhost:8000/docs"

stop: ## Stop all services
	@echo "🛑 Stopping TradeForge AaaS..."
	cd docker && docker-compose down
	@echo "✅ Services stopped"

restart: stop start ## Restart all services

logs: ## View logs from all services
	cd docker && docker-compose logs -f

logs-backend: ## View backend logs only
	cd docker && docker-compose logs -f backend

logs-frontend: ## View frontend logs only
	cd docker && docker-compose logs -f frontend

build: ## Build Docker images
	@echo "🔨 Building Docker images..."
	cd docker && docker-compose build
	@echo "✅ Build complete"

clean: ## Remove containers, volumes, and images
	@echo "🧹 Cleaning up..."
	cd docker && docker-compose down -v --rmi local
	@echo "✅ Cleanup complete"

ps: ## Show running containers
	cd docker && docker-compose ps

shell-backend: ## Open shell in backend container
	cd docker && docker-compose exec backend /bin/bash

shell-frontend: ## Open shell in frontend container
	cd docker && docker-compose exec frontend /bin/bash

shell-postgres: ## Open PostgreSQL shell
	cd docker && docker-compose exec postgres psql -U tradeforge -d tradeforge_db

shell-redis: ## Open Redis CLI
	cd docker && docker-compose exec redis redis-cli

migrate: ## Run database migrations
	cd docker && docker-compose exec backend alembic upgrade head

migrate-create: ## Create new migration (usage: make migrate-create MSG="message")
	cd docker && docker-compose exec backend alembic revision --autogenerate -m "$(MSG)"

test: ## Run tests
	cd backend && poetry run pytest tests/ -v

test-cov: ## Run tests with coverage
	cd backend && poetry run pytest tests/ -v --cov=app --cov-report=html

format: ## Format code with Black and isort
	cd backend && poetry run black app/
	cd backend && poetry run isort app/

lint: ## Run linters
	cd backend && poetry run flake8 app/
	cd backend && poetry run mypy app/

dev-backend: ## Run backend in development mode (without Docker)
	cd backend && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Run frontend in development mode (without Docker)
	cd frontend && streamlit run app.py

setup-env: ## Create .env file from .env.example
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ .env file created. Please edit it with your configuration."; \
	else \
		echo "⚠️  .env file already exists"; \
	fi

backup-db: ## Backup database
	@echo "💾 Creating database backup..."
	cd docker && docker-compose exec postgres pg_dump -U tradeforge tradeforge_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created"

restore-db: ## Restore database (usage: make restore-db FILE=backup.sql)
	@echo "📥 Restoring database from $(FILE)..."
	cd docker && docker-compose exec -T postgres psql -U tradeforge -d tradeforge_db < $(FILE)
	@echo "✅ Database restored"

init: setup-env ## Initialize project (first time setup)
	@echo "🎯 Initializing TradeForge AaaS..."
	@echo "   1. Created .env file"
	@echo "   2. Next: Edit .env with your API keys"
	@echo "   3. Then: make start"
	@echo ""
	@echo "✅ Initialization complete"

# Development shortcuts
backend: dev-backend ## Alias for dev-backend
frontend: dev-frontend ## Alias for dev-frontend
up: start ## Alias for start
down: stop ## Alias for stop
