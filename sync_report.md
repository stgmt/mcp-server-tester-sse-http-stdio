# 🔄 Отчет о синхронизации NPM ↔ Python (Python версия)

## Статистика
- **Всего команд:** 7
- **Всего опций:** 29
- **Дата синхронизации:** 2025-09-10T00:57:56.772591

## Синхронизированные команды

### `tools`
- **Описание:** [test-file]  Run MCP server tools tests (direct API testing).
- **Опций:** 8
- **Опции:**
  - `--server-config`: MCP server configuration file (JSON)
  - `--server-name`: Specific server name to use from config (if multiple
  - `--timeout`: Test timeout in milliseconds (default: "10000")
  - `--debug`: Enable debug output with additional details
  - `--junit-xml`: [filename]  Generate JUnit XML output (default: junit.xml)
  - `--transport`: Transport type: stdio|http
  - `--url`: Server URL for HTTP transport
  - `--help`: Show help for command

### `Use`
- **Описание:** "mcp-server-tester schema" to see test file
- **Опций:** 2
- **Опции:**
  - `--version`: output the version number
  - `--help`: Show help for command

### `evals`
- **Описание:** [test-file]  Run LLM evaluation tests (end-to-end testing
- **Опций:** 8
- **Опции:**
  - `--server-config`: MCP server configuration file (JSON)
  - `--server-name`: Specific server name to use from config (if multiple
  - `--timeout`: Test timeout in milliseconds (default: "10000")
  - `--debug`: Enable debug output with additional details
  - `--junit-xml`: [filename]  Generate JUnit XML output (default: junit.xml)
  - `--transport`: Transport type: stdio|http
  - `--url`: Server URL for HTTP transport
  - `--help`: Show help for command

### `with`
- **Описание:** real LLMs). Requires ANTHROPIC_API_KEY. Use
- **Опций:** 2
- **Опции:**
  - `--version`: output the version number
  - `--help`: Show help for command

### `compliance`
- **Описание:** Run MCP protocol compliance checks
- **Опций:** 6
- **Опции:**
  - `--server-config`: MCP server configuration file (JSON)
  - `--server-name`: Specific server name to use from config (if multiple
  - `--categories`: Test categories to run (comma-separated)
  - `--output`: Output format: console, json (default: "console")
  - `--timeout`: Overall timeout for compliance tests (default:
  - `--help`: Show help for command

### `schema`
- **Описание:** Display JSON schema for test configuration files
- **Опций:** 1
- **Опции:**
  - `--help`: Show help for command

### `help`
- **Описание:** display help for command
- **Опций:** 2
- **Опции:**
  - `--version`: output the version number
  - `--help`: Show help for command


## Использование

```bash
# NPM версия
npx mcp-server-tester-sse-http-stdio tools test.yaml --server-config config.json

# Python версия (синхронизированная)  
mcp-server-tester tools test.yaml --server-config config.json
```

## Примечания
- Генерировано Python скриптом (fallback)
- Команды делегируются NPX напрямую 
- Полная совместимость с NPM версией
