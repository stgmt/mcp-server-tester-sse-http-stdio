# MCP Server Tester - Universal Testing Tool for Model Context Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)](https://nodejs.org)
[![Python Version](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![npm version](https://img.shields.io/npm/v/mcp-server-tester-sse-http-stdio)](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio)
[![PyPI version](https://img.shields.io/pypi/v/mcp-server-tester)](https://pypi.org/project/mcp-server-tester/)
[![Docker Hub](https://img.shields.io/badge/docker-stgmt%2Fmcp--server--tester-blue)](https://hub.docker.com/r/stgmt/mcp-server-tester)
[![Test Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/pulls)

**The most comprehensive MCP (Model Context Protocol) server testing tool** supporting HTTP REST APIs, Server-Sent Events (SSE), and STDIO process communication. Built for testing AI/LLM tools, Anthropic Claude MCP servers, OpenAI-compatible APIs, and custom implementations.

🐍 **Now available for Python!** - Use the same powerful testing capabilities from Python applications with our [Python wrapper](python-wrapper/README.md).

🐳 **Now available on Docker Hub!** - Run tests in containerized environments with our [Docker image](https://hub.docker.com/r/stgmt/mcp-server-tester).

---

## 📑 Table of Contents

- [Why This Tool?](#-why-this-tool)
- [Quick Start](#-quick-start)
  - [Node.js/TypeScript](#nodejs-typescript)
  - [Python](#python)
  - [Docker](#docker)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Features](#-features)
- [Python Wrapper](#-python-wrapper)
- [Docker Support](#-docker-support)
- [Architecture](#-architecture)
- [Troubleshooting](#-troubleshooting)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Why This Tool?

### The Problem
- 🔴 **Self-written test scripts** - Every team reinvents the wheel with custom scripts
- 🔴 **No unified architecture** - Fragmented testing approaches across different transports
- 🔴 **Protocol complexity** - SSE, HTTP, and STDIO each require different handling
- 🔴 **Maintenance nightmare** - Custom scripts break with protocol updates
- 🔴 **Poor readability** - Complex test logic buried in imperative code

### Our Solution
- ✅ **Professional architecture** - Well-designed, extensible testing framework
- ✅ **All MCP protocols** - Complete support for every existing MCP transport
- ✅ **Declarative YAML tests** - Describe test scenarios following BDD best practices
- ✅ **Scenario-based testing** - Write tests as user stories with Given-When-Then structure
- ✅ **Real SSE support** - Native EventSource protocol, not just HTTP POST
- ✅ **TypeScript safety** - Catch errors at compile time
- ✅ **One-line execution** - `npx tsx src/cli.ts tools test.yaml --server-config server.json`
- ✅ **CI/CD ready** - JUnit XML output for any pipeline

---

## 🚀 Quick Start

### Node.js/TypeScript

#### 1. Create test file (test.yaml)
```yaml
tools:
  tests:
    - name: Test server status
      tool: get_status
      params: {}
      expect:
        success: true
        result:
          contains: "status"
```

#### 2. Create server config (server.json)  
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

#### 3. Run tests
```bash
# Install globally
npm install -g mcp-server-tester-sse-http-stdio

# Run tests (✅ ALWAYS specify --server-name!)
npx mcp-server-tester-sse-http-stdio tools test.yaml --server-config server.json --server-name my-server
```

✅ **Server must be running** on specified URL for tests to pass!

#### Test Any Transport in Seconds

**HTTP:**
```bash
npx mcp-server-tester-sse-http-stdio tools examples/crawl4ai-http-tests.yaml \
  --server-config examples/crawl4ai-http-config.json --server-name crawl4ai
```

**SSE:**
```bash
npx mcp-server-tester-sse-http-stdio tools examples/graphiti-sse-tests.yaml \
  --server-config examples/graphiti-sse-config.json --server-name graphiti
```

**STDIO:**
```bash
npx mcp-server-tester-sse-http-stdio tools examples/crawl4ai-stdio-tests.yaml \
  --server-config examples/crawl4ai-stdio-config.json --server-name crawl4ai
```

### Python

#### 1. Install Python wrapper
```bash
# Install from PyPI (requires Node.js + NPM package)
pip install mcp-server-tester
npm install -g mcp-server-tester-sse-http-stdio
```

#### 2. Python API usage
```python
from mcp_server_tester import MCPTester

# Initialize tester
tester = MCPTester()

# Test with configuration files
result = tester.test_server(
    server_config="server.json",
    test_config="test.yaml",
    server_name="my-server"
)

print(f"✅ Tests passed: {result.passed_tests}/{result.total_tests}")
```

#### 3. Python CLI usage
```bash
# Same commands as Node.js version
mcp-server-tester test --server-config server.json --test test.yaml --server-name my-server

# Python-specific features
mcp-server-tester doctor  # Check system dependencies
mcp-server-tester create-server-config  # Interactive config creation
```

📚 **Full Python documentation**: [python-wrapper/README.md](python-wrapper/README.md)

### Docker

The MCP Server Tester is also available as a Docker image, providing a containerized environment with all dependencies pre-installed.

#### Pull the Docker image
```bash
docker pull stgmt/mcp-server-tester
```

#### Run tests with Docker
```bash
# Mount your test files and run tests
docker run -v $(pwd):/workspace stgmt/mcp-server-tester \
  tools /workspace/test.yaml \
  --server-config /workspace/server.json \
  --server-name my-server
```

#### Docker Compose Example
```yaml
version: '3.8'
services:
  mcp-tester:
    image: stgmt/mcp-server-tester
    volumes:
      - ./tests:/workspace/tests
      - ./configs:/workspace/configs
    command: >
      tools /workspace/tests/test.yaml
      --server-config /workspace/configs/server.json
      --server-name my-server
```

🐳 **Docker Hub**: [stgmt/mcp-server-tester](https://hub.docker.com/r/stgmt/mcp-server-tester)

---

## 🚨 Common Pitfalls

### Multiple servers in config
❌ **Wrong:**
```bash
npx mcp-server-tester-sse-http-stdio tools test.yaml --server-config server.json
# Error: Multiple servers found, please specify server name
```

✅ **Correct:**
```bash
npx mcp-server-tester-sse-http-stdio tools test.yaml --server-config server.json --server-name graphiti
```

### Server config format  
❌ **Wrong** (copying from MCP client configs):
```json
{
  "mcpServers": {
    "graphiti": {
      "transport": "sse",
      "url": "http://localhost:8001/sse",
      "description": "My server",  // ❌ Not supported
      "timeout": 30000             // ❌ Not supported
    }
  }
}
```

✅ **Correct** (minimal format):
```json
{
  "mcpServers": {
    "graphiti": {
      "transport": "sse",
      "url": "http://localhost:8001/sse"
    }
  }
}
```

### Test result expectations
❌ **Wrong:**
```yaml
expect:
  success: true
  result:
    matches: true  # ❌ Not supported
```

✅ **Correct:**
```yaml
expect:
  success: true
  result:
    contains: "expected text"  # ✅ or use 'equals'
```

### Server not running
❌ **Error:**
```
Error: Failed to connect: ECONNREFUSED 127.0.0.1:8001
```

✅ **Solution:**
1. Start your MCP server first
2. Verify server is accessible: `curl http://localhost:8001/health`
3. Check server URL in config matches actual server

---

## 📦 Installation

### Requirements
- Node.js >= 18.0.0
- npm >= 8.0.0  
- Python 3.8+ (optional, for STDIO servers)

### From Source
```bash
git clone https://github.com/stgmt/mcp-server-tester-sse-http-stdio.git
cd mcp-server-tester-sse-http-stdio
npm install
npm run build
```

### From NPM
```bash
npm install -g mcp-server-tester-sse-http-stdio
```

### From Docker Hub
```bash
docker pull stgmt/mcp-server-tester
```

### From PyPI (Python)
```bash
pip install mcp-server-tester
```

---

## 📝 Usage Examples

### Basic Test Structure

**YAML Test File:**
```yaml
tools:
  expected_tool_list:
    - tool_name_1
    - tool_name_2
    
  tests:
    - name: Test scenario description
      tool: tool_name
      params:
        param1: value1
      expect:
        success: true
        result:
          contains: "expected text"
```

**Server Configuration:**
```json
{
  "mcpServers": {
    "server_name": {
      "transport": "http|sse|stdio",
      "url": "http://localhost:3000",     // for HTTP/SSE
      "command": "python",                 // for STDIO
      "args": ["server.py", "--stdio"]     // for STDIO
    }
  }
}
```

---

## ⚙️ Configuration

### Transport Types

| Transport | Use Case | Configuration |
|-----------|----------|---------------|
| **HTTP** | REST APIs | `"transport": "http", "url": "..."` |
| **SSE** | Real-time streaming | `"transport": "sse", "url": "..."` |
| **STDIO** | Local processes | `"transport": "stdio", "command": "..."` |

### Command Line Options

```bash
Options:
  --server-config <file>   MCP server configuration (required)
  --server-name <name>     Specific server from config
  --timeout <ms>           Test timeout (default: 10000)
  --debug                  Enable debug output
  --junit-xml [filename]   Generate JUnit XML report
  -t, --transport <type>   Override transport type
  -u, --url <url>          Override server URL
```

---

## ✨ Features

### Core Capabilities
- 🔧 **Universal Protocol Support** - HTTP, SSE, STDIO in one tool
- 📝 **YAML Test Scenarios** - Human-readable test definitions
- 🎯 **BDD Testing** - Given-When-Then test structure
- 🔍 **TypeScript** - Full type safety and IntelliSense
- 📊 **Test Reports** - Console, JSON, JUnit XML formats
- 🚀 **CI/CD Integration** - Jenkins, GitHub Actions, GitLab CI

### Test Types
- **Tools Testing** - Validate tool discovery and execution
- **Compliance Testing** - Protocol compliance verification
- **Eval Testing** - LLM-based evaluation tests
- **Integration Testing** - End-to-end scenarios

---

## 🐍 Python Wrapper

The Python wrapper provides a native Python interface to the MCP Server Tester, making it easy to integrate MCP testing into Python applications and workflows.

### Key Features
- **🔧 Python API** - Native Python classes and methods
- **📦 PyPI Package** - Easy installation with `pip install mcp-server-tester`  
- **🛠️ CLI Commands** - Same powerful CLI, Python-style
- **🧪 Unit Tested** - Comprehensive test coverage with pytest
- **📚 Type Hints** - Full mypy support for better IDE experience
- **🚀 CI/CD Ready** - GitHub Actions for automatic PyPI publishing

### Python vs Node.js
| Feature | Node.js Version | Python Wrapper |
|---------|----------------|-----------------|
| **Installation** | `npm install -g mcp-server-tester-sse-http-stdio` | `pip install mcp-server-tester` |
| **CLI Usage** | `npx mcp-server-tester-sse-http-stdio` | `mcp-server-tester` |
| **API Usage** | TypeScript/JavaScript | Python classes |
| **Dependencies** | Node.js 18+ | Python 3.8+ + Node.js |
| **Test Framework** | vitest | pytest |

### Quick Example
```python
from mcp_server_tester import MCPTester

# Test with dictionaries (no files needed)
server_config = {
    "mcpServers": {
        "my-server": {
            "transport": "sse", 
            "url": "http://localhost:8001/sse"
        }
    }
}

test_config = {
    "tools": {
        "tests": [
            {"name": "basic-test", "calls": [{"tool": "list_files"}]}
        ]
    }
}

tester = MCPTester()
result = tester.test_server(server_config, test_config, server_name="my-server")
print(f"✅ {result.passed_tests}/{result.total_tests} tests passed!")
```

📚 **Full Documentation**: [python-wrapper/README.md](python-wrapper/README.md)

---

## 🐳 Docker Support

The MCP Server Tester is available as a multi-platform Docker image, providing a consistent testing environment across different systems.

### Docker Image Features
- **🎯 Multi-platform Support** - linux/amd64, linux/arm64, linux/arm/v7, darwin/arm64
- **📦 All Dependencies Included** - Node.js, TypeScript, and all required packages
- **🔒 Security Scanned** - Regular vulnerability scanning with Trivy
- **🚀 CI/CD Ready** - Automated builds on every release
- **⚡ Optimized Size** - Minimal Alpine Linux base image

### Installation Methods

#### Docker Hub
```bash
# Pull the latest version
docker pull stgmt/mcp-server-tester

# Pull a specific version
docker pull stgmt/mcp-server-tester:1.4.1

# Pull for specific platform
docker pull --platform linux/arm64 stgmt/mcp-server-tester
```

#### GitHub Container Registry (alternative)
```bash
docker pull ghcr.io/stgmt/mcp-server-tester
```

### Usage Examples

#### Basic Testing
```bash
# Run tests with mounted configuration
docker run -v $(pwd):/workspace stgmt/mcp-server-tester \
  tools /workspace/test.yaml \
  --server-config /workspace/server.json \
  --server-name my-server
```

#### Interactive Shell
```bash
# Start container with shell access
docker run -it --entrypoint /bin/sh stgmt/mcp-server-tester

# Inside container
mcp-server-tester tools test.yaml --server-config server.json --server-name my-server
```

#### Network Testing
```bash
# Test servers on host network
docker run --network host stgmt/mcp-server-tester \
  tools test.yaml \
  --server-config server.json \
  --server-name local-server
```

### Docker Compose Integration

```yaml
version: '3.8'

services:
  # Your MCP server
  mcp-server:
    image: your-mcp-server:latest
    ports:
      - "8001:8001"

  # MCP Server Tester
  tester:
    image: stgmt/mcp-server-tester
    depends_on:
      - mcp-server
    volumes:
      - ./tests:/tests
      - ./configs:/configs
    command: >
      tools /tests/integration.yaml
      --server-config /configs/docker-server.json
      --server-name docker-server
    environment:
      - DEBUG=true
```

### CI/CD Pipeline Integration

#### GitHub Actions
```yaml
name: MCP Server Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run MCP Tests
        run: |
          docker run -v ${{ github.workspace }}:/workspace \
            stgmt/mcp-server-tester \
            tools /workspace/tests/test.yaml \
            --server-config /workspace/configs/server.json \
            --server-name ci-server \
            --junit-xml /workspace/test-results.xml
            
      - name: Publish Test Results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: test-results.xml
```

#### GitLab CI
```yaml
test-mcp-server:
  image: stgmt/mcp-server-tester
  script:
    - mcp-server-tester tools tests/test.yaml --server-config configs/server.json --server-name gitlab-server
  artifacts:
    reports:
      junit: test-results.xml
```

### Building Custom Images

Create a Dockerfile for your specific testing needs:

```dockerfile
FROM stgmt/mcp-server-tester

# Add custom test files
COPY tests/ /app/tests/
COPY configs/ /app/configs/

# Set default command
CMD ["tools", "/app/tests/all.yaml", "--server-config", "/app/configs/server.json"]
```

### Platform Support

| Platform | Architecture | Status |
|----------|-------------|--------|
| Linux | amd64 | ✅ Fully Supported |
| Linux | arm64 | ✅ Fully Supported |
| Linux | arm/v7 | ✅ Fully Supported |
| macOS | arm64 (M1/M2) | ✅ Experimental |
| Windows | amd64 | ⚠️ Use WSL2 |

### Resources
- 🐳 **Docker Hub**: [stgmt/mcp-server-tester](https://hub.docker.com/r/stgmt/mcp-server-tester)
- 📦 **GitHub Packages**: [ghcr.io/stgmt/mcp-server-tester](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/pkgs/container/mcp-server-tester)
- 🔧 **Dockerfile**: [View on GitHub](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/blob/main/Dockerfile)

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐
│   YAML Tests    │
└────────┬────────┘
         │
┌────────▼────────┐
│   Test Runner   │
└────────┬────────┘
         │
┌────────▼────────┐
│  MCP Client     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
┌──────┐  ┌─────┐  ┌───────┐
│ HTTP │  │ SSE │  │ STDIO │
└──────┘  └─────┘  └───────┘
```

### Transport Comparison

| Feature | HTTP | SSE | STDIO |
|---------|------|-----|-------|
| **Protocol** | REST API | EventSource | Process IPC |
| **Connection** | Stateless | Persistent | Direct |
| **Performance** | Medium | High | Highest |
| **Debugging** | Easy | Medium | Hard |
| **Scalability** | High | Medium | Low |

### vs Alternatives

| Feature | Our Tool | MCP Inspector | Manual Testing | Custom Scripts |
|---------|----------|---------------|----------------|----------------|
| SSE Support | ✅ Native | ❌ Limited | ❌ Complex | ⚠️ DIY |
| STDIO Testing | ✅ Full | ⚠️ Partial | ✅ Possible | ✅ Possible |
| YAML Config | ✅ Yes | ❌ No | ❌ No | ❌ No |
| TypeScript | ✅ Full | ⚠️ Partial | ❌ No | ⚠️ Optional |
| CI/CD Ready | ✅ JUnit | ❌ No | ❌ No | ⚠️ DIY |

---

## 🐛 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| "Cannot find module '@modelcontextprotocol/sdk'" | Run `npm install` |
| "MCP error -32000: Connection closed" | Check server is running and URL is correct |
| "Server's protocol version not supported" | Use protocol version "2024-11-05" |
| "Tool not found" | Verify exact tool name (case-sensitive) |

### Debug Mode

```bash
# Enable detailed logging
npx tsx src/cli.ts tools test.yaml --server-config server.json --debug
```

---

## 📚 API Reference

### Test Runner API

```typescript
import { CapabilitiesTestRunner } from './commands/tools/runner.js';

const runner = new CapabilitiesTestRunner(
  toolsConfig,
  options,
  displayManager
);

const result = await runner.run();
```

### Custom Transport Implementation

```typescript
class CustomTransport implements McpTransport {
  async connect(): Promise<void> { /* ... */ }
  async sendRequest(method: string, params: any): Promise<any> { /* ... */ }
  async close(): Promise<void> { /* ... */ }
}
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines  
- Testing requirements
- Pull request process

### Development Commands

```bash
npm run dev          # Development mode
npm test            # Run tests
npm run lint        # Check code style
npm run build       # Production build
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- 📦 [NPM Package](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio)
- 🐛 [Issue Tracker](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/issues)
- 💬 [Telegram Channel](https://t.me/ii_pomogator)
- 📖 [MCP Documentation](https://modelcontextprotocol.io)

---

## ⭐ Support

If this tool helps your development:
- ⭐ **Star** this repository
- 🔄 **Share** with your team
- 🐛 **Report** issues
- 🤝 **Contribute** improvements

Every star helps others discover this tool!