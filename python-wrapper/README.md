# MCP Server Tester

Высококлассный инструмент для тестирования MCP серверов с поддержкой протокола SSE-HTTP-STDIO, авторизацией по Bearer токену и написанием тестовых сценариев через конфигурационные файлы без необходимости программирования.

## 🚀 Доступен на всех платформах

[![npm version](https://img.shields.io/npm/v/mcp-server-tester-sse-http-stdio.svg)](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio)
[![PyPI version](https://img.shields.io/pypi/v/mcp-server-tester.svg)](https://pypi.org/project/mcp-server-tester/)
[![Docker Hub](https://img.shields.io/docker/pulls/stgmt/mcp-server-tester.svg)](https://hub.docker.com/r/stgmt/mcp-server-tester)

## 🧪 Python Wrapper - Programmatic Testing Framework

**Universal framework for programmatic unit and integration testing of MCP (Model Context Protocol) servers across all available protocols.**

🔗 **GitHub Repository**: https://github.com/stgmt/mcp-server-tester-sse-http-stdio

## 🎯 What is this?

MCP Server Tester is a comprehensive tool for automated testing of MCP servers, supporting:

- **📋 Unit Testing** - testing individual tools and functions
- **🔄 Integration Testing** - checking interaction between components  
- **🌐 Protocol Testing** - support for all MCP protocols (HTTP, SSE, STDIO)
- **🤖 LLM Evaluation** - testing using large language models
- **📊 Compliance Checks** - MCP specification compliance

### Supported protocols:
- ✅ **HTTP** - REST API interface
- ✅ **SSE (Server-Sent Events)** - streaming data transfer  
- ✅ **STDIO** - standard input/output for processes

## 🚀 Three ways to use

| Method | Installation | Advantages | Use Case |
|--------|-----------|------------|----------|
| **🐍 Python** | `pip install mcp-server-tester` | Programmable API | Python integration |
| **🐳 Docker** | `docker pull stgmt/mcp-server-tester` | No dependencies | Isolated testing |
| **📦 NPM** | `npm install -g mcp-server-tester-sse-http-stdio` | Maximum performance | Native performance |

## 📦 Quick Start

### Python API (Recommended for programming)

```bash
pip install mcp-server-tester
```

```python
from mcp_server_tester import MCPTester

# Initialize tester
tester = MCPTester()

# Programmatic testing
result = tester.test_server(
    server_config="config.json",
    test_config="test.yaml", 
    server_name="my-server"
)

print(f"✅ {result.passed_tests}/{result.total_tests} tests passed")
print(f"⏱️ Execution time: {result.execution_time:.1f}s")

# Integration into unit tests
def test_mcp_integration():
    result = tester.test_server(server_config, test_config, "my-server")
    assert result.success, f"MCP tests failed: {result.failed_tests}"
```

### Docker (Recommended for CI/CD)

```bash
# Quick check without installing dependencies
docker run --rm stgmt/mcp-server-tester --help

# Testing with local files
docker run --rm \
  -v $(pwd):/workspace \
  stgmt/mcp-server-tester \
  tools /workspace/test.yaml \
  --server-config /workspace/config.json \
  --server-name my-server

# Multi-architecture support (AMD64, ARM64)
docker run --rm --platform linux/arm64 stgmt/mcp-server-tester --version
```

### CLI commands

```bash
# Unit testing of tools
mcp-server-tester test --server-config config.json --test test.yaml --server-name my-server

# Integration testing for protocol compliance
mcp-server-tester compliance --server-config config.json --server-name my-server

# LLM Evaluation tests (requires ANTHROPIC_API_KEY)
mcp-server-tester evals --server-config config.json --test eval.yaml --server-name my-server

# System diagnostics
mcp-server-tester doctor

# Interactive configuration creation
mcp-server-tester create-server-config
mcp-server-tester create-test-config
```

## 🔧 Programmatic Testing

### Server configuration (server-config.json)
```json
{
  "mcpServers": {
    "my-server": {
      "transport": "sse",
      "url": "http://localhost:8001/sse"
    }
  }
}
```

### Test scenarios (test.yaml)
```yaml
tools:
  tests:
    - name: "Unit: Test file listing"
      tool: "list_files"
      params: {}
      expect:
        success: true
        
    - name: "Integration: Search and process"
      tool: "search_files"
      params:
        query: "test"
      expect:
        success: true
        result_contains: ["results"]
```

### Python programming tests
```python
# Creating tests in code
test_config = {
    "tools": {
        "tests": [
            {
                "name": "Unit: Basic functionality",
                "tool": "list_files",
                "params": {},
                "expect": {"success": True}
            },
            {
                "name": "Integration: Complex workflow", 
                "tool": "process_data",
                "params": {"data": "test"},
                "expect": {
                    "success": True,
                    "result_contains": ["processed"]
                }
            }
        ]
    }
}

# Execute programmatic tests
result = tester.test_server(server_config, test_config, "my-server")

# Analyze results
for test_result in result.test_results:
    print(f"Test: {test_result.name}")
    print(f"Status: {'PASSED' if test_result.success else 'FAILED'}")
    if not test_result.success:
        print(f"Error: {test_result.error}")
```

## 📊 Supported Platforms

### Architectures
- ✅ **AMD64** (Intel/AMD x86_64)
- ✅ **ARM64** (Apple Silicon M1/M2/M3, ARM servers)
- ✅ **Multi-platform Docker** with automatic architecture selection

### Operating Systems  
- ✅ **Linux** (all distributions)
- ✅ **macOS** (Intel and Apple Silicon)
- ✅ **Windows** (with Docker Desktop or WSL2)
- ✅ **Cloud platforms** (AWS, GCP, Azure)

## 🌐 Links and Resources

### Main Resources
- 📦 **NPM**: https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio
- 🐍 **PyPI**: https://pypi.org/project/mcp-server-tester/
- 🐳 **Docker Hub**: https://hub.docker.com/r/stgmt/mcp-server-tester
- 📖 **GitHub**: https://github.com/stgmt/mcp-server-tester-sse-http-stdio

### MCP Protocol
- 🔗 **MCP Specification**: https://modelcontextprotocol.io
- 📚 **MCP Documentation**: https://docs.anthropic.com/en/docs/build-with-claude/model-context-protocol

## 📈 Usage Examples

### In Python projects
```python
# Integration with pytest
def test_mcp_server_integration():
    tester = MCPTester()
    result = tester.test_server("config.json", "tests.yaml", "my-server")
    assert result.success, f"MCP integration failed: {result.error_details}"
```

### In CI/CD (GitHub Actions)
```yaml
- name: Test MCP Server
  run: |
    docker run --rm --network host \
      -v ${{ github.workspace }}:/workspace \
      stgmt/mcp-server-tester \
      tools /workspace/test-config.yaml \
      --server-config /workspace/server-config.json
```

### In development
```bash
# Quick check during development
docker run --rm --network host \
  -v $(pwd):/workspace \
  stgmt/mcp-server-tester \
  doctor
```

---

**🎯 MCP Server Tester - unified solution for comprehensive testing of MCP servers of all types and protocols!**