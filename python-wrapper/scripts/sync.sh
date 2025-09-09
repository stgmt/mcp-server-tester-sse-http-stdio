#!/bin/bash

# 🔄 Скрипт синхронизации команд между NPM и Python версиями
# 
# Использование:
#   ./scripts/sync.sh           # Полная синхронизация
#   ./scripts/sync.sh --dry-run # Только показать изменения без применения
#   ./scripts/sync.sh --help    # Показать справку

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции вывода
info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

# Показать справку
show_help() {
    cat << EOF
🔄 Скрипт синхронизации команд NPM ↔ Python

ИСПОЛЬЗОВАНИЕ:
    ./scripts/sync.sh [ОПЦИИ]

ОПЦИИ:
    --dry-run       Показать изменения без применения
    --force         Принудительная перезапись без backup
    --help          Показать эту справку

ПРИМЕРЫ:
    ./scripts/sync.sh                    # Полная синхронизация
    ./scripts/sync.sh --dry-run         # Предварительный просмотр
    ./scripts/sync.sh --force           # Без backup

ОПИСАНИЕ:
    Этот скрипт автоматически синхронизирует команды, опции и help
    между NPM пакетом mcp-server-tester-sse-http-stdio и Python wrapper.
    
    Шаги выполнения:
    1. Проверка зависимостей (Node.js, NPM пакет)
    2. Извлечение команд из NPM пакета
    3. Генерация синхронизированного Python кода
    4. Backup существующих файлов (если --force не указан)
    5. Обновление Python CLI и Core модулей
    6. Генерация отчета о синхронизации

РЕЗУЛЬТАТ:
    - src/mcp_server_tester/cli_generated.py  # Новый CLI
    - src/mcp_server_tester/core_update.py   # Обновления для core
    - sync_report.md                         # Отчет о синхронизации
    - backups/TIMESTAMP/                     # Backup файлов

EOF
}

# Проверка зависимостей
check_dependencies() {
    info "Проверка зависимостей..."
    
    # Node.js
    if ! command -v node &> /dev/null; then
        error "Node.js не найден. Установите с https://nodejs.org/"
        exit 1
    fi
    
    # NPX
    if ! command -v npx &> /dev/null; then
        error "NPX не найден. Обновите Node.js/NPM"
        exit 1
    fi
    
    # NPM пакет
    if ! npx mcp-server-tester-sse-http-stdio --help &> /dev/null; then
        warning "NPM пакет не найден, устанавливаю..."
        npm install -g mcp-server-tester-sse-http-stdio
    fi
    
    success "Зависимости проверены"
}

# Проверка состояния репозитория
check_repo_state() {
    info "Проверка состояния репозитория..."
    
    if [[ -n $(git status --porcelain) ]]; then
        warning "Есть несохраненные изменения в git"
        if [[ "$FORCE" != "true" ]]; then
            echo "Рекомендуется сделать commit перед синхронизацией"
            read -p "Продолжить? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                info "Синхронизация отменена"
                exit 0
            fi
        fi
    fi
    
    success "Состояние репозитория проверено"
}

# Выполнение синхронизации
run_sync() {
    info "Запуск синхронизации..."
    
    cd "$(dirname "$0")"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        info "DRY RUN: Показываю изменения без применения"
        export DRY_RUN=true
    fi
    
    # Запуск Node.js скрипта синхронизации
    node sync_commands.js
    
    if [[ "$DRY_RUN" != "true" ]]; then
        success "Синхронизация завершена"
        info "Проверьте результаты:"
        echo "  - sync_report.md - отчет о синхронизации"
        echo "  - src/mcp_server_tester/cli_generated.py - новый CLI"
        echo "  - commands_extracted.json - извлеченные команды"
        
        # Показать diff если есть git
        if command -v git &> /dev/null; then
            info "Git diff изменений:"
            git diff --name-only | head -10
        fi
    fi
}

# Парсинг аргументов
FORCE=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            error "Неизвестная опция: $1"
            echo "Используйте --help для справки"
            exit 1
            ;;
    esac
done

# Основная логика
main() {
    info "🔄 Начинаю синхронизацию команд NPM ↔ Python"
    echo
    
    check_dependencies
    check_repo_state
    run_sync
    
    echo
    success "🎉 Синхронизация завершена успешно!"
}

# Запуск если не source'd
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi