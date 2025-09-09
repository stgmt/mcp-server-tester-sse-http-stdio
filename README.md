# MCP Server Tester - Universal Testing Tool for Model Context Protocol

[![License: Non-Commercial](https://img.shields.io/badge/License-Non--Commercial-orange.svg)](./LICENSE-COMMERCIAL)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)](https://nodejs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![npm version](https://img.shields.io/npm/v/mcp-server-tester-sse-http-stdio)](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio)
[![Test Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/pulls)

**The most comprehensive MCP (Model Context Protocol) server testing tool** supporting HTTP REST APIs, Server-Sent Events (SSE), and STDIO process communication. Built for testing AI/LLM tools, Anthropic Claude MCP servers, OpenAI-compatible APIs, and custom implementations.

---

## 📑 Table of Contents

- [Why This Tool?](#-why-this-tool)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Features](#-features)
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

```bash
# Install globally
npm install -g mcp-server-tester-sse-http-stdio

# Or use directly with npx
npx mcp-server-tester-sse-http-stdio tools test.yaml --server-config server.json
```

### Test Any Transport in Seconds

**HTTP:**
```bash
npx tsx src/cli.ts tools examples/crawl4ai-http-tests.yaml \
  --server-config examples/crawl4ai-http-config.json
```

**SSE:**
```bash
npx tsx src/cli.ts tools examples/graphiti-sse-tests.yaml \
  --server-config examples/graphiti-sse-config.json
```

**STDIO:**
```bash
npx tsx src/cli.ts tools examples/crawl4ai-stdio-tests.yaml \
  --server-config examples/crawl4ai-stdio-config.json
```

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

### From NPM (when published)
```bash
npm install -g mcp-server-tester-sse-http-stdio
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

**Non-Commercial Use License** - see [LICENSE-COMMERCIAL](LICENSE-COMMERCIAL)

For commercial licensing, contact the author.

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