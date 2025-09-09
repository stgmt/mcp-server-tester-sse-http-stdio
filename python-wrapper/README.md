# MCP Server Tester Python Wrapper

[![PyPI version](https://badge.fury.io/py/mcp-server-tester.svg)](https://badge.fury.io/py/mcp-server-tester)
[![Python Support](https://img.shields.io/pypi/pyversions/mcp-server-tester.svg)](https://pypi.org/project/mcp-server-tester/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python wrapper for the [mcp-server-tester-sse-http-stdio](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio) NPM package.

This package provides a Python interface to test Model Context Protocol (MCP) servers using multiple transport protocols (SSE, STDIO, HTTP).

## 🚀 Features

- **Multiple Transport Protocols**: SSE, STDIO, HTTP support
- **Python Integration**: Native Python API with type hints
- **CLI Interface**: Command-line tools for testing
- **Interactive Configuration**: Easy setup wizards
- **Comprehensive Testing**: Unit tests with pytest
- **Cross-Platform**: Works on Windows, macOS, Linux

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 18.0.0+** (required for underlying NPM package)
- **NPM package**: `mcp-server-tester-sse-http-stdio`

## 🛠 Installation

### 1. Install Python package

```bash
pip install mcp-server-tester
```

### 2. Install NPM dependency

```bash
# Global installation (recommended)
npm install -g mcp-server-tester-sse-http-stdio

# Or using npx (will download on demand)
npx mcp-server-tester-sse-http-stdio --help
```

### 3. Verify installation

```bash
mcp-server-tester doctor
```

## 🏃‍♂️ Quick Start

### Python API

```python
from mcp_server_tester import MCPTester

# Initialize tester
tester = MCPTester()

# Test with configuration files
result = tester.test_server(
    server_config="server-config.json",
    test_config="test-config.yaml", 
    server_name="my-server"
)

print(f"✅ Tests passed: {result.passed_tests}/{result.total_tests}")
print(f"⏱️ Execution time: {result.execution_time:.2f}s")

# Test with configuration dictionaries
server_config = {
    "mcpServers": {
        "test-server": {
            "transport": "sse",
            "url": "http://localhost:8001/sse"
        }
    }
}

test_config = {
    "tools": {
        "tests": [
            {
                "name": "basic-test",
                "calls": [
                    {"tool": "list_files"},
                    {"tool": "read_file", "arguments": {"path": "test.txt"}}
                ]
            }
        ]
    }
}

result = tester.test_server(server_config, test_config)
```

### CLI Usage

```bash
# Test MCP server
mcp-server-tester test \\
    --server-config server.json \\
    --test test.yaml \\
    --server-name my-server

# List available tools
mcp-server-tester tools --server-config server.json --server-name my-server

# Validate configuration
mcp-server-tester validate server.json

# Interactive configuration creation
mcp-server-tester create-server-config --output server.json
mcp-server-tester create-test-config --output test.yaml

# System diagnostics
mcp-server-tester doctor
```

## 📁 Configuration Files

### Server Configuration (JSON)

```json
{
  "mcpServers": {
    "sse-server": {
      "transport": "sse",
      "url": "http://localhost:8001/sse"
    },
    "stdio-server": {
      "transport": "stdio", 
      "command": "python",
      "args": ["-m", "my_mcp_server"]
    },
    "http-server": {
      "transport": "http",
      "url": "http://localhost:8000"
    }
  }
}
```

### Test Configuration (YAML)

```yaml
tools:
  tests:
    - name: "Basic functionality test"
      calls:
        - tool: "list_files"
        - tool: "read_file"
          arguments:
            path: "example.txt"
        - tool: "write_file"
          arguments:
            path: "output.txt"
            content: "Hello, World!"

    - name: "Error handling test"
      calls:
        - tool: "nonexistent_tool"
          expect_error: true
```

## 🔧 Advanced Usage

### Custom Test Results Processing

```python
from mcp_server_tester import MCPTester

tester = MCPTester()

result = tester.test_server("server.json", "test.yaml")

if result.success:
    print(f"✅ All {result.total_tests} tests passed!")
    print(f"Execution time: {result.execution_time:.2f}s")
else:
    print(f"❌ {len(result.failed_tests)} tests failed:")
    for failed_test in result.failed_tests:
        print(f"  - {failed_test.get('name', 'Unknown')}: {failed_test.get('error', 'Unknown error')}")
```

### Configuration Helpers

```python
from mcp_server_tester import MCPTester

# Create server configuration programmatically
servers = {
    "production-server": {
        "transport": "sse",
        "url": "https://api.example.com/mcp/sse"
    },
    "local-server": {
        "transport": "stdio",
        "command": "python", 
        "args": ["-m", "my_server", "--debug"]
    }
}

config_json = MCPTester.create_server_config(servers, "servers.json")
print("Server configuration created!")

# Create test configuration
tests = [
    {
        "name": "API Integration Test",
        "calls": [
            {"tool": "get_user", "arguments": {"user_id": 123}},
            {"tool": "list_products", "arguments": {"category": "electronics"}}
        ]
    }
]

config_yaml = MCPTester.create_test_config(tests, "api-tests.yaml")
print("Test configuration created!")
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mcp_server_tester --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run with verbose output
pytest -v
```

## 🛠 Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/stgmt/mcp-server-tester-python.git
cd mcp-server-tester-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install in development mode with dev dependencies
pip install -e .[dev]

# Install NPM dependency
npm install -g mcp-server-tester-sse-http-stdio

# Run tests
pytest
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## 🚨 Common Pitfalls

### ❌ Wrong: Missing server-name parameter
```bash
# This fails when multiple servers exist in config
mcp-server-tester test --server-config multi-server.json --test test.yaml
```

### ✅ Correct: Specify server name
```bash
mcp-server-tester test --server-config multi-server.json --test test.yaml --server-name specific-server
```

### ❌ Wrong: Node.js not installed
```python
from mcp_server_tester import MCPTester
tester = MCPTester()  # Raises NodeJSNotFoundError
```

### ✅ Correct: Install Node.js first
```bash
# Install Node.js from https://nodejs.org/
# Then verify:
mcp-server-tester doctor
```

### ❌ Wrong: NPM package not found
```bash
npx mcp-server-tester-sse-http-stdio --help  # Command not found
```

### ✅ Correct: Install NPM package
```bash
npm install -g mcp-server-tester-sse-http-stdio
# Or let npx handle it automatically
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [mcp-server-tester-sse-http-stdio](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio) - The underlying NPM package
- [Model Context Protocol](https://github.com/anthropics/model-context-protocol) - Official MCP specification

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/stgmt/mcp-server-tester-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/stgmt/mcp-server-tester-python/discussions)
- **NPM Package Issues**: [NPM Package Issues](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/issues)

---

**Made with ❤️ by the MCP community**