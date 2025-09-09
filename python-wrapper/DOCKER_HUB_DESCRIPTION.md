# 🧪 MCP Server Tester - Universal Testing Framework

**Comprehensive framework for programmatic unit and integration testing of MCP (Model Context Protocol) servers across all available protocols.**

## 🎯 What is MCP Server Tester?

A complete testing solution supporting:
- **📋 Unit Testing** - Individual tool and function testing
- **🔄 Integration Testing** - Component interaction verification  
- **🌐 Protocol Testing** - HTTP, SSE, and STDIO protocol support
- **🤖 LLM Evaluation** - AI-powered testing capabilities
- **📊 Compliance Checks** - MCP specification validation

## 🚀 Quick Start

### Basic Usage
```bash
# Quick system check
docker run --rm stgmt/mcp-server-tester --version

# Test MCP server with local configs
docker run --rm --network host \
  -v $(pwd):/workspace \
  stgmt/mcp-server-tester \
  tools /workspace/test.yaml \
  --server-config /workspace/config.json \
  --server-name my-server
```

### Example: Test Real Graphiti MCP Server
```bash
docker run --rm --network host \
  -v /path/to/project:/workspace \
  stgmt/mcp-server-tester \
  tools /workspace/test-graphiti-mcp.yaml \
  --server-config /workspace/server-config.json \
  --server-name graphiti-local
```

**Result:**
```
📋 Tools Tests
✅ Tool discovery: 8/8 expected tools found
✅ Add simple text episode: PASSED
✅ Search for nodes: PASSED
✅ Search for facts/edges: PASSED
📊 Results: 8/8 tests passed (7.6s)
```

## 🏗️ Multi-Platform Support

| Architecture | Status | Platforms |
|--------------|--------|-----------|
| **AMD64** | ✅ Supported | Intel/AMD x86_64, Cloud servers |
| **ARM64** | ✅ Supported | Apple Silicon (M1/M2/M3), ARM servers |

## 📦 Available Formats

| Format | Installation | Use Case |
|--------|--------------|----------|
| **🐳 Docker** | `docker pull stgmt/mcp-server-tester` | Isolated testing, CI/CD |
| **📦 NPM** | `npm install -g mcp-server-tester-sse-http-stdio` | Maximum performance |
| **🐍 Python** | `pip install mcp-server-tester` | Python integration |

## 🔧 Supported Protocols

- ✅ **HTTP** - REST API interface
- ✅ **SSE (Server-Sent Events)** - Streaming data
- ✅ **STDIO** - Standard input/output for processes

## 🌐 Links & Resources

- **📖 GitHub Repository**: https://github.com/stgmt/mcp-server-tester-sse-http-stdio
- **📦 NPM Package**: https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio
- **🐍 PyPI Package**: https://pypi.org/project/mcp-server-tester/
- **🔗 MCP Protocol**: https://modelcontextprotocol.io

## 📋 Available Commands

```bash
# System diagnostics
docker run --rm stgmt/mcp-server-tester doctor

# Tools testing
docker run --rm -v $(pwd):/workspace stgmt/mcp-server-tester \
  tools /workspace/test.yaml --server-config /workspace/config.json

# Compliance checking
docker run --rm -v $(pwd):/workspace stgmt/mcp-server-tester \
  compliance --server-config /workspace/config.json

# Interactive mode
docker run --rm -it -v $(pwd):/workspace stgmt/mcp-server-tester bash
```

## ⚡ Performance

- **Cold start**: ~1.2s
- **Test execution**: ~6-8s for 8 comprehensive tests
- **Memory usage**: ~120MB (optimized Alpine Linux)
- **Image size**: ~200MB (multi-platform)

**🎯 Ready for production use across all major platforms and architectures!**