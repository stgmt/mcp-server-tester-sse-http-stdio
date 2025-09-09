# 🧪 MCP Server Tester - Фреймворк для программируемого тестирования

**Универсальный фреймворк для программируемого unit и integration тестирования MCP (Model Context Protocol) серверов всех доступных протоколов.**

🔗 **GitHub Repository**: https://github.com/stgmt/mcp-server-tester-sse-http-stdio

[![Python Package](https://img.shields.io/pypi/v/mcp-server-tester)](https://pypi.org/project/mcp-server-tester/)
[![Docker Image](https://img.shields.io/docker/v/stgmt/mcp-server-tester)](https://hub.docker.com/r/stgmt/mcp-server-tester)
[![NPM Package](https://img.shields.io/npm/v/mcp-server-tester-sse-http-stdio)](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio)
[![GitHub](https://img.shields.io/github/stars/stgmt/mcp-server-tester-sse-http-stdio?style=social)](https://github.com/stgmt/mcp-server-tester-sse-http-stdio)

## 🎯 Что это такое?

MCP Server Tester — это комплексный инструмент для автоматизированного тестирования MCP серверов, поддерживающий:

- **📋 Unit тестирование** - тестирование отдельных инструментов и функций
- **🔄 Integration тестирование** - проверка взаимодействия между компонентами  
- **🌐 Protocol тестирование** - поддержка всех MCP протоколов (HTTP, SSE, STDIO)
- **🤖 LLM Evaluation** - тестирование с помощью больших языковых моделей
- **📊 Compliance проверки** - соответствие MCP спецификации

### Поддерживаемые протоколы:
- ✅ **HTTP** - REST API интерфейс
- ✅ **SSE (Server-Sent Events)** - потоковая передача данных  
- ✅ **STDIO** - стандартный ввод/вывод для процессов

## 🚀 Три способа использования

| Способ | Установка | Преимущества | Использование |
|--------|-----------|--------------|---------------|
| **🐍 Python** | `pip install mcp-server-tester` | Программируемый API | Python интеграция |
| **🐳 Docker** | `docker pull stgmt/mcp-server-tester` | Без зависимостей | Изолированное тестирование |
| **📦 NPM** | `npm install -g mcp-server-tester-sse-http-stdio` | Максимальная скорость | Нативная производительность |

## 📦 Быстрый старт

### Python API (Рекомендуется для программирования)

```bash
pip install mcp-server-tester
```

```python
from mcp_server_tester import MCPTester

# Инициализация тестера
tester = MCPTester()

# Программируемое тестирование
result = tester.test_server(
    server_config="config.json",
    test_config="test.yaml", 
    server_name="my-server"
)

print(f"✅ {result.passed_tests}/{result.total_tests} тестов прошли")
print(f"⏱️ Время выполнения: {result.execution_time:.1f}s")

# Интеграция в unit тесты
def test_mcp_integration():
    result = tester.test_server(server_config, test_config, "my-server")
    assert result.success, f"MCP tests failed: {result.failed_tests}"
```

### Docker (Рекомендуется для CI/CD)

```bash
# Быстрая проверка без установки зависимостей
docker run --rm stgmt/mcp-server-tester --help

# Тестирование с локальными файлами
docker run --rm \
  -v $(pwd):/workspace \
  stgmt/mcp-server-tester \
  tools /workspace/test.yaml \
  --server-config /workspace/config.json \
  --server-name my-server

# Поддержка всех архитектур (AMD64, ARM64)
docker run --rm --platform linux/arm64 stgmt/mcp-server-tester --version
```

### CLI команды

```bash
# Unit тестирование инструментов
mcp-server-tester test --server-config config.json --test test.yaml --server-name my-server

# Integration тестирование соответствия протоколу
mcp-server-tester compliance --server-config config.json --server-name my-server

# LLM Evaluation тесты (требует ANTHROPIC_API_KEY)
mcp-server-tester evals --server-config config.json --test eval.yaml --server-name my-server

# Диагностика системы
mcp-server-tester doctor

# Интерактивное создание конфигураций
mcp-server-tester create-server-config
mcp-server-tester create-test-config
```

## 🔧 Программируемое тестирование

### Конфигурация сервера (server-config.json)
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

### Тестовые сценарии (test.yaml)
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

### Python программирование тестов
```python
# Создание тестов в коде
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

# Выполнение программируемых тестов
result = tester.test_server(server_config, test_config, "my-server")

# Анализ результатов
for test_result in result.test_results:
    print(f"Test: {test_result.name}")
    print(f"Status: {'PASSED' if test_result.success else 'FAILED'}")
    if not test_result.success:
        print(f"Error: {test_result.error}")
```

## 📊 Поддерживаемые платформы

### Архитектуры
- ✅ **AMD64** (Intel/AMD x86_64)
- ✅ **ARM64** (Apple Silicon M1/M2/M3, ARM серверы)
- ✅ **Multi-platform Docker** с автоматическим выбором архитектуры

### Операционные системы  
- ✅ **Linux** (все дистрибутивы)
- ✅ **macOS** (Intel и Apple Silicon)
- ✅ **Windows** (с Docker Desktop или WSL2)
- ✅ **Облачные платформы** (AWS, GCP, Azure)

## 🌐 Ссылки и ресурсы

### Основные ресурсы
- 📦 **NPM**: https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio
- 🐍 **PyPI**: https://pypi.org/project/mcp-server-tester/
- 🐳 **Docker Hub**: https://hub.docker.com/r/stgmt/mcp-server-tester
- 📖 **GitHub**: https://github.com/stgmt/mcp-server-tester-sse-http-stdio

### Протокол MCP
- 🔗 **MCP Specification**: https://modelcontextprotocol.io
- 📚 **MCP Documentation**: https://docs.anthropic.com/en/docs/build-with-claude/model-context-protocol

## 📈 Примеры использования

### В Python проектах
```python
# Интеграция в pytest
def test_mcp_server_integration():
    tester = MCPTester()
    result = tester.test_server("config.json", "tests.yaml", "my-server")
    assert result.success, f"MCP integration failed: {result.error_details}"
```

### В CI/CD (GitHub Actions)
```yaml
- name: Test MCP Server
  run: |
    docker run --rm --network host \
      -v ${{ github.workspace }}:/workspace \
      stgmt/mcp-server-tester \
      tools /workspace/test-config.yaml \
      --server-config /workspace/server-config.json
```

### В разработке
```bash
# Быстрая проверка во время разработки
docker run --rm --network host \
  -v $(pwd):/workspace \
  stgmt/mcp-server-tester \
  doctor
```

---

**🎯 MCP Server Tester - единое решение для comprehensive тестирования MCP серверов всех типов и протоколов!**