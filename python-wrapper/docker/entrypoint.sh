#!/bin/bash

# 🐳 MCP Server Tester Docker Entrypoint
# 
# Provides flexible container usage for all variants:
# - NPM commands (npx)
# - Python commands (mcp-server-tester) 
# - Direct bash/node/python calls

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m' 
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Functions for beautiful output
info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }
header() { echo -e "${PURPLE}🐳 $1${NC}"; }

# Show container information
show_container_info() {
    header "MCP Server Tester Docker Container v1.4.1"
    echo
    echo "📦 Available tools:"
    echo "  • Node.js: $(node --version)"
    echo "  • NPM: $(npm --version)" 
    echo "  • Python: $(python3 --version)"
    echo "  • mcp-server-tester-sse-http-stdio: $(npx mcp-server-tester-sse-http-stdio --version)"
    echo "  • mcp-server-tester (Python): $(mcp-server-tester --version)"
    echo
}

# Show usage help
show_help() {
    show_container_info
    
    echo "🚀 Usage methods:"
    echo
    echo "1️⃣ NPM package (TypeScript/JavaScript):"
    echo "   docker run --rm -v \$(pwd):/workspace mcp-server-tester \\"
    echo "     npx mcp-server-tester-sse-http-stdio tools test.yaml --server-config config.json"
    echo
    echo "2️⃣ Python package:"
    echo "   docker run --rm -v \$(pwd):/workspace mcp-server-tester \\"
    echo "     mcp-server-tester test --server-config config.json --test test.yaml"
    echo
    echo "3️⃣ Interactive mode:"
    echo "   docker run --rm -it -v \$(pwd):/workspace mcp-server-tester bash"
    echo
    echo "4️⃣ One-time commands:"
    echo "   docker run --rm mcp-server-tester node --version"
    echo "   docker run --rm mcp-server-tester python3 -c \"import sys; print(sys.version)\""
    echo
    echo "📋 Testing examples:"
    echo "   # HTTP MCP server"
    echo "   docker run --rm -v \$(pwd):/workspace mcp-server-tester \\"
    echo "     tools http-test.yaml --server-config http-config.json --server-name my-server"
    echo
    echo "   # SSE MCP server"  
    echo "   docker run --rm -v \$(pwd):/workspace mcp-server-tester \\"
    echo "     tools sse-test.yaml --server-config sse-config.json --server-name graphiti"
    echo
    echo "   # STDIO MCP server"
    echo "   docker run --rm -v \$(pwd):/workspace mcp-server-tester \\"
    echo "     tools stdio-test.yaml --server-config stdio-config.json --server-name local-server"
    echo
    echo "🔧 Additional commands:"
    echo "   compliance  - MCP protocol compliance check"
    echo "   evals       - LLM evaluation tests" 
    echo "   schema      - Show JSON configuration schema"
    echo "   doctor      - System dependencies check"
    echo
    echo "📖 Documentation: https://github.com/stgmt/mcp-server-tester-sse-http-stdio"
}

# System check function
run_doctor() {
    header "🏥 MCP Server Tester Doctor (Docker)"
    echo
    
    info "Checking Node.js..."
    if command -v node &> /dev/null; then
        success "Node.js: $(node --version)"
    else
        error "Node.js not found"
    fi
    
    info "Checking NPM..."
    if command -v npm &> /dev/null; then
        success "NPM: $(npm --version)"
    else
        error "NPM not found"
    fi
    
    info "Checking Python..."
    if command -v python3 &> /dev/null; then
        success "Python: $(python3 --version)"
    else
        error "Python not found"
    fi
    
    info "Checking NPM package..."
    if npx mcp-server-tester-sse-http-stdio --help &> /dev/null; then
        success "mcp-server-tester-sse-http-stdio: available"
    else
        error "mcp-server-tester-sse-http-stdio unavailable"
    fi
    
    info "Checking Python package..."
    if mcp-server-tester --help &> /dev/null; then
        success "mcp-server-tester: available"
    else
        error "mcp-server-tester unavailable"  
    fi
    
    echo
    success "🎯 Container ready for MCP server testing!"
}

# Process arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

# Special container commands
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

# Check if first argument is MCP tester command
MCP_COMMANDS=("tools" "evals" "compliance" "schema" "documentation" "test" "create-server-config" "create-test-config")

for cmd in "${MCP_COMMANDS[@]}"; do
    if [ "$1" = "$cmd" ]; then
        # This is MCP tester command - use Python wrapper
        info "Executing MCP tester command via Python wrapper: $*"
        exec mcp-server-tester "$@"
    fi
done

# Check if this is NPX command
if [ "$1" = "npx" ]; then
    info "Executing NPX command: $*"
    exec "$@"
fi

# For all other commands - execute as is
info "Executing command: $*"
exec "$@"