#!/bin/bash

# 🐳 MCP Server Tester Docker Entrypoint
# 
# Обеспечивает гибкое использование контейнера для всех вариантов:
# - NPM команды (npx)
# - Python команды (mcp-server-tester) 
# - Прямые вызовы bash/node/python

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m' 
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Функции для красивого вывода
info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }
header() { echo -e "${PURPLE}🐳 $1${NC}"; }

# Показать информацию о контейнере
show_container_info() {
    header "MCP Server Tester Docker Container v1.0.0"
    echo
    echo "📦 Доступные инструменты:"
    echo "  • Node.js: $(node --version)"
    echo "  • NPM: $(npm --version)" 
    echo "  • Python: $(python3 --version)"
    echo "  • mcp-server-tester-sse-http-stdio: $(npx mcp-server-tester-sse-http-stdio --version)"
    echo "  • mcp-server-tester (Python): $(mcp-server-tester --version)"
    echo
}

# Показать справку по использованию
show_help() {
    show_container_info
    
    echo "🚀 Способы использования:"
    echo
    echo "1️⃣ NPM пакет (TypeScript/JavaScript):"
    echo "   docker run --rm -v \$(pwd):/workspace mcp-server-tester \\"
    echo "     npx mcp-server-tester-sse-http-stdio tools test.yaml --server-config config.json"
    echo
    echo "2️⃣ Python пакет:"
    echo "   docker run --rm -v \$(pwd):/workspace mcp-server-tester \\"
    echo "     mcp-server-tester test --server-config config.json --test test.yaml"
    echo
    echo "3️⃣ Интерактивный режим:"
    echo "   docker run --rm -it -v \$(pwd):/workspace mcp-server-tester bash"
    echo
    echo "4️⃣ Одноразовые команды:"
    echo "   docker run --rm mcp-server-tester node --version"
    echo "   docker run --rm mcp-server-tester python3 -c \"import sys; print(sys.version)\""
    echo
    echo "📋 Примеры тестирования:"
    echo "   # HTTP MCP сервер"
    echo "   docker run --rm -v \$(pwd):/workspace mcp-server-tester \\"
    echo "     tools http-test.yaml --server-config http-config.json --server-name my-server"
    echo
    echo "   # SSE MCP сервер"  
    echo "   docker run --rm -v \$(pwd):/workspace mcp-server-tester \\"
    echo "     tools sse-test.yaml --server-config sse-config.json --server-name graphiti"
    echo
    echo "   # STDIO MCP сервер"
    echo "   docker run --rm -v \$(pwd):/workspace mcp-server-tester \\"
    echo "     tools stdio-test.yaml --server-config stdio-config.json --server-name local-server"
    echo
    echo "🔧 Дополнительные команды:"
    echo "   compliance  - Проверка соответствия протоколу MCP"
    echo "   evals       - LLM evaluation тесты" 
    echo "   schema      - Показать JSON схему конфигурации"
    echo "   doctor      - Проверка системных зависимостей"
    echo
    echo "📖 Документация: https://github.com/stgmt/mcp-server-tester-sse-http-stdio"
}

# Функция проверки системы
run_doctor() {
    header "🏥 MCP Server Tester Doctor (Docker)"
    echo
    
    info "Проверка Node.js..."
    if command -v node &> /dev/null; then
        success "Node.js: $(node --version)"
    else
        error "Node.js не найден"
    fi
    
    info "Проверка NPM..."
    if command -v npm &> /dev/null; then
        success "NPM: $(npm --version)"
    else
        error "NPM не найден"
    fi
    
    info "Проверка Python..."
    if command -v python3 &> /dev/null; then
        success "Python: $(python3 --version)"
    else
        error "Python не найден"
    fi
    
    info "Проверка NPM пакета..."
    if npx mcp-server-tester-sse-http-stdio --help &> /dev/null; then
        success "mcp-server-tester-sse-http-stdio: доступен"
    else
        error "mcp-server-tester-sse-http-stdio недоступен"
    fi
    
    info "Проверка Python пакета..."
    if mcp-server-tester --help &> /dev/null; then
        success "mcp-server-tester: доступен"
    else
        error "mcp-server-tester недоступен"  
    fi
    
    echo
    success "🎯 Контейнер готов к тестированию MCP серверов!"
}

# Обработка аргументов
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

# Специальные команды контейнера
case "$1" in
    --help|-h|help)
        show_help
        exit 0
        ;;
    --version|-v|version)
        show_container_info
        exit 0
        ;;
    doctor)
        run_doctor
        exit 0
        ;;
    info)
        show_container_info
        exit 0
        ;;
esac

# Проверяем, является ли первый аргумент командой MCP tester
MCP_COMMANDS=("tools" "evals" "compliance" "schema" "documentation" "test" "create-server-config" "create-test-config")

for cmd in "${MCP_COMMANDS[@]}"; do
    if [ "$1" = "$cmd" ]; then
        # Это команда MCP tester - используем Python wrapper
        info "Выполняется команда MCP tester через Python wrapper: $*"
        exec mcp-server-tester "$@"
    fi
done

# Проверяем, является ли это NPX командой
if [ "$1" = "npx" ]; then
    info "Выполняется NPX команда: $*"
    exec "$@"
fi

# Для всех остальных команд - выполняем как есть
info "Выполняется команда: $*"
exec "$@"