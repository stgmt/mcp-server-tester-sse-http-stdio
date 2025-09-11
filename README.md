[🇷🇺 Русская версия](./README.ru.md)

# MCP Server Tester - High-performance testing framework for MCP servers with SSE-HTTP-STDIO protocol support, Bearer token authorization, and declarative test scenarios

A high-performance tool for testing MCP servers with SSE-HTTP-STDIO protocol support, Bearer token authorization, and test scenario writing through configuration files without programming.

## 🚀 Available on All Platforms

[![npm version](https://img.shields.io/npm/v/mcp-server-tester-sse-http-stdio.svg)](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio)
[![PyPI version](https://img.shields.io/pypi/v/mcp-server-tester-sse-stdio.svg)](https://pypi.org/project/mcp-server-tester-sse-stdio/)
[![Docker Hub](https://img.shields.io/docker/pulls/stgmt/mcp-server-tester.svg)](https://hub.docker.com/r/stgmt/mcp-server-tester)
[![GitHub Actions](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/workflows/CI/badge.svg)](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/actions)

## 👨‍💻 Author

Created by [**@ii_pomogator**](https://t.me/ii_pomogator) - AI Assistant Channel on Telegram

---

## ✨ Key Features

- 🔌 **Full SSE-HTTP-STDIO protocol support** for MCP servers
- 🔐 **Bearer token authorization** for secure testing
- 📝 **Declarative tests** - write scenarios in YAML without programming
- 🎯 **Multiple assertion types** - verify any aspects of responses
- 📊 **Detailed reports** on test execution
- 🐳 **Docker support** for isolated testing
- 🔄 **CI/CD integration** via GitHub Actions

## 📦 Installation

### NPM (Node.js)
```bash
npm install -g mcp-server-tester-sse-http-stdio
```

### PyPI (Python)
```bash
pip install mcp-server-tester-sse-stdio
```

### Docker
```bash
docker pull stgmt/mcp-server-tester
```

## 🚀 Quick Start

### Using NPM
```bash
npx mcp-server-tester-sse-http-stdio test --test test.yaml --server-config config.json
```

### Using Python
```bash
mcp-server-tester test --test test.yaml --server-config config.json
```

### Using Docker
```bash
docker run -v $(pwd):/workspace stgmt/mcp-server-tester test --test /workspace/test.yaml
```

## 📝 Example Test Scenario

```yaml
name: "MCP Server Basic Test"
description: "Testing basic MCP server functionality"
timeout: 30000

tests:
  - name: "Initialize connection"
    type: "initialize"
    params:
      protocolVersion: "1.0.0"
      capabilities:
        tools: true
    expect:
      status: "success"
      capabilities:
        tools: true

  - name: "List available tools"
    type: "tools/list"
    expect:
      status: "success"
      tools:
        - name: "echo"
          description: "Echo tool"

  - name: "Call echo tool"
    type: "tools/call"
    params:
      name: "echo"
      arguments:
        message: "Hello, MCP!"
    expect:
      status: "success"
      result:
        message: "Hello, MCP!"
```

## 📋 Server Configuration

```json
{
  "mcpServers": {
    "test-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "BEARER_TOKEN": "your-secret-token"
      },
      "transport": {
        "type": "sse",
        "config": {
          "url": "http://localhost:3000/sse",
          "headers": {
            "Authorization": "Bearer your-secret-token"
          }
        }
      }
    }
  }
}
```

## 🛠️ CLI Commands

### Run Tests
```bash
mcp-server-tester test --test <test-file> --server-config <config-file> [options]

Options:
  --server-name <name>  Server name from configuration
  --verbose            Verbose output
  --json-output        Output results in JSON format
  --timeout <ms>       Test timeout (default: 30000)
```

### Validate Configuration
```bash
mcp-server-tester validate --test <test-file>
```

### List Available Server Tools
```bash
mcp-server-tester tools --server-config <config-file> --server-name <name>
```

## 🐳 Docker Support

### Simple Run
```bash
docker run -v $(pwd):/workspace stgmt/mcp-server-tester \
  test --test /workspace/test.yaml --server-config /workspace/config.json
```

### Docker Compose
```yaml
version: '3.8'
services:
  mcp-tester:
    image: stgmt/mcp-server-tester
    volumes:
      - ./tests:/workspace/tests
      - ./config:/workspace/config
    command: test --test /workspace/tests/test.yaml --server-config /workspace/config/server.json
```

### Supported Platforms
| Platform | Architecture | Status |
|----------|--------------|--------|
| Linux | amd64 | ✅ |
| Linux | arm64 | ✅ |
| macOS | amd64 | ✅ |
| macOS | arm64 | ✅ |
| Windows | amd64 | ✅ |

## 🔄 CI/CD Integration

### GitHub Actions
```yaml
name: MCP Server Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run MCP Server Tests
        run: |
          docker run -v ${{ github.workspace }}:/workspace \
            stgmt/mcp-server-tester test \
            --test /workspace/tests/test.yaml \
            --server-config /workspace/config.json
```

### GitLab CI
```yaml
mcp-tests:
  image: stgmt/mcp-server-tester
  script:
    - mcp-server-tester test --test tests/test.yaml --server-config config.json
```

## 📊 Assertion Examples

### Response Structure Validation
```yaml
expect:
  status: "success"
  result:
    type: "object"
    properties:
      message:
        type: "string"
        pattern: "^Hello.*"
      count:
        type: "number"
        minimum: 0
```

### Array Validation
```yaml
expect:
  tools:
    type: "array"
    minItems: 1
    items:
      type: "object"
      required: ["name", "description"]
```

### Conditional Validation
```yaml
expect:
  oneOf:
    - status: "success"
      result: { processed: true }
    - status: "pending"
      result: { queued: true }
```

## 🔧 Advanced Features

### Environment Variables
```yaml
tests:
  - name: "Test with env variables"
    env:
      API_KEY: "${TEST_API_KEY}"
      BASE_URL: "${TEST_BASE_URL:-http://localhost:3000}"
```

### Sequential Tests with Dependencies
```yaml
tests:
  - name: "Create resource"
    id: "create"
    type: "tools/call"
    params:
      name: "create_resource"
    capture:
      resource_id: "$.result.id"
  
  - name: "Get created resource"
    depends_on: ["create"]
    type: "tools/call"
    params:
      name: "get_resource"
      arguments:
        id: "${resource_id}"
```

### Parallel Execution
```yaml
parallel_groups:
  - name: "Performance tests"
    tests:
      - name: "Test 1"
      - name: "Test 2"
      - name: "Test 3"
```

## 📚 Documentation

- [Complete Guide](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/wiki)
- [API Reference](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/wiki/API)
- [Test Examples](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/tree/main/examples)
- [FAQ](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/wiki/FAQ)

## 🤝 Contributing

We welcome contributions to the project! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🔗 Links

- **GitHub**: [stgmt/mcp-server-tester-sse-http-stdio](https://github.com/stgmt/mcp-server-tester-sse-http-stdio)
- **NPM**: [mcp-server-tester-sse-http-stdio](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio)
- **PyPI**: [mcp-server-tester-sse-stdio](https://pypi.org/project/mcp-server-tester-sse-stdio/)
- **Docker Hub**: [stgmt/mcp-server-tester](https://hub.docker.com/r/stgmt/mcp-server-tester)

## 💬 Support

- [Create Issue](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/issues)
- [Discussions](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/discussions)
- Email: support@stgmt.dev

---

*Developed with ❤️ by [@ii_pomogator](https://t.me/ii_pomogator)*