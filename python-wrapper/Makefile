# 🔄 Makefile для MCP Server Tester Python Wrapper
#
# Основные команды:
#   make sync       - Синхронизация с NPM пакетом
#   make test       - Запуск тестов  
#   make build      - Сборка пакета
#   make install    - Локальная установка
#   make clean      - Очистка
#   make help       - Показать справку

.PHONY: help sync sync-node sync-python test build install clean check-deps lint format

# Переменные
PYTHON := python3
NPM_PACKAGE := mcp-server-tester-sse-http-stdio
SOURCE_DIR := src/mcp_server_tester
SCRIPTS_DIR := scripts
TESTS_DIR := tests

# Цвета для вывода
GREEN := \033[0;32m
BLUE := \033[0;34m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

# По умолчанию показываем справку
help:
	@echo "$(BLUE)🔄 MCP Server Tester Python Wrapper$(NC)"
	@echo ""
	@echo "$(GREEN)Доступные команды:$(NC)"
	@echo "  $(YELLOW)sync$(NC)          - Синхронизация команд с NPM пакетом"  
	@echo "  $(YELLOW)sync-node$(NC)     - Синхронизация через Node.js (предпочтительно)"
	@echo "  $(YELLOW)sync-python$(NC)   - Синхронизация через Python (fallback)"
	@echo "  $(YELLOW)test$(NC)          - Запуск всех тестов"
	@echo "  $(YELLOW)test-quick$(NC)    - Быстрые тесты без интеграционных"
	@echo "  $(YELLOW)build$(NC)         - Сборка wheel пакета"
	@echo "  $(YELLOW)install$(NC)       - Локальная установка в editable режиме"
	@echo "  $(YELLOW)publish$(NC)       - Публикация в PyPI"
	@echo "  $(YELLOW)clean$(NC)         - Очистка временных файлов"
	@echo "  $(YELLOW)lint$(NC)          - Проверка кода (flake8, mypy)"
	@echo "  $(YELLOW)format$(NC)        - Форматирование кода (black)"
	@echo "  $(YELLOW)check-deps$(NC)    - Проверка зависимостей"
	@echo ""
	@echo "$(GREEN)Примеры:$(NC)"
	@echo "  make sync                    # Полная синхронизация"
	@echo "  make test                    # Все тесты"  
	@echo "  make build install           # Сборка и установка"
	@echo ""

# Проверка зависимостей
check-deps:
	@echo "$(BLUE)🔍 Проверка зависимостей...$(NC)"
	@command -v $(PYTHON) >/dev/null || (echo "$(RED)❌ Python 3 не найден$(NC)" && exit 1)
	@command -v node >/dev/null || echo "$(YELLOW)⚠️  Node.js не найден - будет использован Python fallback$(NC)"
	@command -v npx >/dev/null || echo "$(YELLOW)⚠️  NPX не найден - будет использован Python fallback$(NC)"
	@$(PYTHON) -c "import click, yaml, requests" 2>/dev/null || (echo "$(RED)❌ Не все Python зависимости установлены$(NC)" && exit 1)
	@echo "$(GREEN)✅ Основные зависимости доступны$(NC)"

# Главная команда синхронизации (выбирает лучший доступный метод)
sync: check-deps
	@echo "$(BLUE)🔄 Запуск синхронизации команд...$(NC)"
	@if command -v node >/dev/null && command -v npx >/dev/null; then \
		echo "$(GREEN)→ Используется Node.js синхронизатор$(NC)"; \
		$(MAKE) sync-node; \
	else \
		echo "$(YELLOW)→ Используется Python fallback синхронизатор$(NC)"; \
		$(MAKE) sync-python; \
	fi

# Синхронизация через Node.js (предпочтительный метод)
sync-node:
	@echo "$(BLUE)🟢 Node.js синхронизация...$(NC)"
	@cd $(SCRIPTS_DIR) && chmod +x sync.sh && ./sync.sh

# Синхронизация через Python (fallback)
sync-python:
	@echo "$(BLUE)🐍 Python fallback синхронизация...$(NC)"
	@cd $(SCRIPTS_DIR) && $(PYTHON) sync_commands.py

# Dry-run синхронизация (показать изменения без применения)
sync-dry-run:
	@echo "$(BLUE)👁️  Dry-run синхронизация...$(NC)"
	@cd $(SCRIPTS_DIR) && ./sync.sh --dry-run

# Тесты
test: check-deps
	@echo "$(BLUE)🧪 Запуск всех тестов...$(NC)"
	@$(PYTHON) -m pytest $(TESTS_DIR)/ -v --tb=short

test-quick: check-deps
	@echo "$(BLUE)⚡ Быстрые тесты...$(NC)"
	@$(PYTHON) -m pytest $(TESTS_DIR)/ -v -k "not integration" --tb=short

test-integration: check-deps
	@echo "$(BLUE)🔗 Интеграционные тесты...$(NC)"
	@$(PYTHON) -m pytest $(TESTS_DIR)/ -v -k "integration" --tb=short

# Линтинг и форматирование
lint: check-deps
	@echo "$(BLUE)🔍 Проверка кода...$(NC)"
	@$(PYTHON) -m flake8 $(SOURCE_DIR)/ $(TESTS_DIR)/ --max-line-length=88
	@$(PYTHON) -m mypy $(SOURCE_DIR)/ --ignore-missing-imports

format: check-deps
	@echo "$(BLUE)🎨 Форматирование кода...$(NC)"
	@$(PYTHON) -m black $(SOURCE_DIR)/ $(TESTS_DIR)/

# Сборка
build: check-deps lint test-quick
	@echo "$(BLUE)📦 Сборка пакета...$(NC)"
	@$(PYTHON) -m pip install --upgrade build
	@$(PYTHON) -m build
	@echo "$(GREEN)✅ Пакет собран в dist/$(NC)"

# Локальная установка
install: check-deps
	@echo "$(BLUE)📥 Локальная установка...$(NC)"
	@$(PYTHON) -m pip install -e .
	@echo "$(GREEN)✅ Пакет установлен в editable режиме$(NC)"

# Установка с зависимостями разработки
install-dev: check-deps
	@echo "$(BLUE)🛠️  Установка для разработки...$(NC)"
	@$(PYTHON) -m pip install -e ".[dev]"
	@echo "$(GREEN)✅ Пакет установлен с dev зависимостями$(NC)"

# Публикация в PyPI
publish: build
	@echo "$(BLUE)📤 Публикация в PyPI...$(NC)"
	@$(PYTHON) -m pip install --upgrade twine
	@$(PYTHON) -m twine upload dist/*
	@echo "$(GREEN)✅ Пакет опубликован в PyPI$(NC)"

# Публикация в Test PyPI 
publish-test: build
	@echo "$(BLUE)🧪 Публикация в Test PyPI...$(NC)"
	@$(PYTHON) -m pip install --upgrade twine
	@$(PYTHON) -m twine upload --repository testpypi dist/*
	@echo "$(GREEN)✅ Пакет опубликован в Test PyPI$(NC)"

# ======================================
# 🐳 DOCKER КОМАНДЫ
# ======================================

# Сборка Docker образа
docker-build:
	@echo "$(BLUE)🐳 Сборка Docker образа...$(NC)"
	@docker build -t mcp-server-tester:latest .
	@docker build -t mcp-server-tester:1.0.0 .
	@echo "$(GREEN)✅ Docker образ собран$(NC)"

# Запуск Docker контейнера (показать справку)
docker-run: docker-build
	@echo "$(BLUE)🚀 Запуск Docker контейнера...$(NC)"
	@docker run --rm mcp-server-tester:latest

# Интерактивный режим Docker
docker-shell: docker-build
	@echo "$(BLUE)🐚 Интерактивный режим Docker...$(NC)"
	@docker run --rm -it -v $(shell pwd):/workspace mcp-server-tester:latest bash

# Тест Docker образа
docker-test: docker-build
	@echo "$(BLUE)🧪 Тестирование Docker образа...$(NC)"
	@docker run --rm mcp-server-tester:latest doctor
	@docker run --rm mcp-server-tester:latest --version
	@echo "$(GREEN)✅ Docker образ протестирован$(NC)"

# Публикация Docker образа в Docker Hub
docker-publish: docker-build docker-test
	@echo "$(BLUE)📤 Публикация Docker образа...$(NC)"
	@docker tag mcp-server-tester:latest stgmt/mcp-server-tester:latest
	@docker tag mcp-server-tester:1.0.0 stgmt/mcp-server-tester:1.0.0
	@docker push stgmt/mcp-server-tester:latest
	@docker push stgmt/mcp-server-tester:1.0.0
	@echo "$(GREEN)✅ Docker образ опубликован$(NC)"

# Запуск с docker-compose
docker-compose-up:
	@echo "$(BLUE)🐳 Запуск через docker-compose...$(NC)"
	@docker-compose up --build

# Запуск в режиме разработки
docker-compose-dev:
	@echo "$(BLUE)🛠️  Режим разработки через docker-compose...$(NC)"
	@docker-compose --profile dev up --build -d mcp-tester-dev
	@docker-compose exec mcp-tester-dev bash

# Примеры использования
docker-examples:
	@echo "$(BLUE)📋 Запуск примеров через docker-compose...$(NC)"
	@docker-compose --profile examples up --build

# Очистка Docker ресурсов
docker-clean:
	@echo "$(BLUE)🧹 Очистка Docker ресурсов...$(NC)"
	@docker-compose down --volumes --remove-orphans || true
	@docker rmi mcp-server-tester:latest mcp-server-tester:1.0.0 || true
	@docker system prune -f
	@echo "$(GREEN)✅ Docker ресурсы очищены$(NC)"

# Полная сборка всех артефактов (Python, NPM, Docker)
build-all: build docker-build
	@echo "$(GREEN)✅ Все артефакты собраны:$(NC)"
	@echo "  📦 Python wheel: dist/"
	@echo "  🐳 Docker образ: mcp-server-tester:latest"

# Очистка
clean:
	@echo "$(BLUE)🧹 Очистка временных файлов...$(NC)"
	@rm -rf build/ dist/ *.egg-info/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name ".coverage" -delete
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@echo "$(GREEN)✅ Очистка завершена$(NC)"

# Полная очистка включая backup и сгенерированные файлы
clean-all: clean
	@echo "$(BLUE)🗑️  Полная очистка...$(NC)"
	@rm -rf backups/
	@rm -f commands_extracted.json sync_report.md
	@rm -f $(SOURCE_DIR)/cli_generated.py
	@echo "$(GREEN)✅ Полная очистка завершена$(NC)"

# Проверка статуса синхронизации
sync-status:
	@echo "$(BLUE)📊 Статус синхронизации...$(NC)"
	@if [ -f "sync_report.md" ]; then \
		echo "$(GREEN)✅ Найден отчет о синхронизации$(NC)"; \
		grep -E "Всего команд|Дата синхронизации" sync_report.md || true; \
	else \
		echo "$(YELLOW)⚠️  Отчет о синхронизации не найден$(NC)"; \
		echo "Запустите: make sync"; \
	fi
	@if [ -f "$(SOURCE_DIR)/cli_generated.py" ]; then \
		echo "$(GREEN)✅ Найден сгенерированный CLI$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  Сгенерированный CLI не найден$(NC)"; \
	fi

# Демонстрация работы пакета
demo: install
	@echo "$(BLUE)🎬 Демонстрация работы пакета...$(NC)"
	@echo "$(YELLOW)1. Проверка системы:$(NC)"
	@mcp-server-tester doctor
	@echo ""
	@echo "$(YELLOW)2. Показать справку:$(NC)"  
	@mcp-server-tester --help
	@echo ""
	@echo "$(GREEN)✅ Демонстрация завершена$(NC)"

# CI/CD команды
ci-test: check-deps lint test

ci-build: ci-test build

ci-publish: ci-build publish

# Информация о проекте
info:
	@echo "$(BLUE)ℹ️  Информация о проекте$(NC)"
	@echo "Название: MCP Server Tester Python Wrapper"
	@echo "Версия: 1.0.0"
	@echo "NPM пакет: $(NPM_PACKAGE)"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Директория исходников: $(SOURCE_DIR)"
	@echo "Директория тестов: $(TESTS_DIR)"
	@if command -v node >/dev/null; then \
		echo "Node.js: $(shell node --version)"; \
	fi
	@if [ -f "sync_report.md" ]; then \
		echo "Последняя синхронизация: $(shell grep "Дата синхронизации" sync_report.md | cut -d: -f2- | xargs)"; \
	fi