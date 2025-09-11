[🇬🇧 English version](./README.md)

# MCP Server Tester

Высококлассный инструмент для тестирования MCP серверов с поддержкой протокола SSE-HTTP-STDIO, авторизацией по Bearer токену и написанием тестовых сценариев через конфигурационные файлы без необходимости программирования.

## 🚀 Доступен на всех платформах

[![npm version](https://img.shields.io/npm/v/mcp-server-tester-sse-http-stdio.svg)](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio)
[![PyPI version](https://img.shields.io/pypi/v/mcp-server-tester-sse-stdio.svg)](https://pypi.org/project/mcp-server-tester-sse-stdio/)
[![Docker Hub](https://img.shields.io/docker/pulls/stgmt/mcp-server-tester.svg)](https://hub.docker.com/r/stgmt/mcp-server-tester)
[![GitHub Actions](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/workflows/CI/badge.svg)](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/actions)

## 👨‍💻 Автор

Создано [**@ii_pomogator**](https://t.me/ii_pomogator) - Канал ИИ-помогатор в Telegram

---

## ✨ Ключевые возможности

- 🔌 **Полная поддержка SSE-HTTP-STDIO протокола** для MCP серверов
- 🔐 **Bearer токен авторизация** для безопасного тестирования
- 📝 **Декларативные тесты** - пишите сценарии в YAML без программирования
- 🎯 **Множественные assertion типы** - проверяйте любые аспекты ответов
- 📊 **Детальные отчеты** о прохождении тестов
- 🐳 **Docker поддержка** для изолированного тестирования
- 🔄 **CI/CD интеграция** через GitHub Actions

## 📦 Установка

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

## 🚀 Быстрый старт

### Использование через NPM
```bash
npx mcp-server-tester-sse-http-stdio test --test test.yaml --server-config config.json
```

### Использование через Python
```bash
mcp-server-tester test --test test.yaml --server-config config.json
```

### Использование через Docker
```bash
docker run -v $(pwd):/workspace stgmt/mcp-server-tester test --test /workspace/test.yaml
```

## 📝 Пример тестового сценария

```yaml
name: "MCP Server Basic Test"
description: "Проверка базовой функциональности MCP сервера"
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

## 📋 Конфигурация сервера

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

## 🛠️ CLI команды

### Запуск тестов
```bash
mcp-server-tester test --test <test-file> --server-config <config-file> [options]

Options:
  --server-name <name>  Имя сервера из конфигурации
  --verbose            Подробный вывод
  --json-output        Вывод результатов в JSON формате
  --timeout <ms>       Таймаут для тестов (по умолчанию: 30000)
```

### Валидация конфигурации
```bash
mcp-server-tester validate --test <test-file>
```

### Список доступных инструментов сервера
```bash
mcp-server-tester tools --server-config <config-file> --server-name <name>
```

## 🐳 Docker поддержка

### Простой запуск
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

### Поддерживаемые платформы
| Платформа | Архитектура | Статус |
|-----------|-------------|--------|
| Linux | amd64 | ✅ |
| Linux | arm64 | ✅ |
| macOS | amd64 | ✅ |
| macOS | arm64 | ✅ |
| Windows | amd64 | ✅ |

## 🔄 CI/CD интеграция

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

## 📊 Примеры assertion

### Проверка структуры ответа
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

### Проверка массивов
```yaml
expect:
  tools:
    type: "array"
    minItems: 1
    items:
      type: "object"
      required: ["name", "description"]
```

### Условные проверки
```yaml
expect:
  oneOf:
    - status: "success"
      result: { processed: true }
    - status: "pending"
      result: { queued: true }
```

## 🔧 Расширенные возможности

### Переменные окружения
```yaml
tests:
  - name: "Test with env variables"
    env:
      API_KEY: "${TEST_API_KEY}"
      BASE_URL: "${TEST_BASE_URL:-http://localhost:3000}"
```

### Последовательные тесты с зависимостями
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

### Параллельное выполнение
```yaml
parallel_groups:
  - name: "Performance tests"
    tests:
      - name: "Test 1"
      - name: "Test 2"
      - name: "Test 3"
```

## 📚 Документация

- [Полное руководство](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/wiki)
- [API Reference](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/wiki/API)
- [Примеры тестов](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/tree/main/examples)
- [FAQ](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/wiki/FAQ)

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! См. [CONTRIBUTING.md](CONTRIBUTING.md) для деталей.

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE) файл.

## 🔗 Ссылки

- **GitHub**: [stgmt/mcp-server-tester-sse-http-stdio](https://github.com/stgmt/mcp-server-tester-sse-http-stdio)
- **NPM**: [mcp-server-tester-sse-http-stdio](https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio)
- **PyPI**: [mcp-server-tester-sse-stdio](https://pypi.org/project/mcp-server-tester-sse-stdio/)
- **Docker Hub**: [stgmt/mcp-server-tester](https://hub.docker.com/r/stgmt/mcp-server-tester)

## 💬 Поддержка

- [Создать Issue](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/issues)
- [Discussions](https://github.com/stgmt/mcp-server-tester-sse-http-stdio/discussions)
- Email: support@stgmt.dev

---

*Разработано с ❤️ [@ii_pomogator](https://t.me/ii_pomogator)*