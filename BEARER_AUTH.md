# Поддержка Bearer Token авторизации в MCP Server Tester

## Обзор

MCP Server Tester теперь поддерживает Bearer token авторизацию для HTTP и SSE транспортов. Это позволяет тестировать MCP серверы, требующие аутентификацию.

## Использование

### 1. Через конфигурационный файл

Создайте JSON файл конфигурации с полем `bearerToken`:

```json
{
  "mcpServers": {
    "my-secure-server": {
      "transport": "http",
      "url": "https://api.example.com/mcp",
      "bearerToken": "your-bearer-token-here"
    }
  }
}
```

Запустите тесты:

```bash
node dist/cli.js tools test-file.yaml --server-config config-with-auth.json
```

### 2. Через URL параметры

Можно передать токен через URL параметр `token`:

```bash
node dist/cli.js tools test-file.yaml --url "https://api.example.com/mcp?token=your-bearer-token"
```

Токен будет автоматически извлечен из URL и использован для авторизации.

## Поддерживаемые транспорты

- **HTTP** (`StreamableHTTPClientTransport`) - Bearer токен добавляется в заголовок Authorization всех HTTP запросов
- **SSE** (`SSEClientTransport`) - Bearer токен добавляется в заголовки как для SSE соединения, так и для POST запросов

## Примеры конфигураций

### HTTP транспорт с авторизацией

```json
{
  "mcpServers": {
    "crawl4ai-remote": {
      "transport": "http",
      "url": "https://your-domain.com/mcp",
      "bearerToken": "sk_mt_your_token_here"
    }
  }
}
```

### SSE транспорт с авторизацией

```json
{
  "mcpServers": {
    "streaming-server": {
      "transport": "sse",
      "url": "https://your-domain.com/sse",
      "bearerToken": "Bearer_your_token_here"
    }
  }
}
```

## Безопасность

⚠️ **Важно**: Никогда не коммитьте файлы с реальными Bearer токенами в Git репозиторий!

Рекомендации:
1. Используйте переменные окружения в конфигурационных файлах
2. Добавьте конфигурационные файлы с токенами в `.gitignore`
3. Храните токены в защищенных хранилищах секретов

## Техническая реализация

Bearer токен поддержка реализована через:

1. Расширение интерфейсов `ServerConfig` и `TransportOptions` с полем `bearerToken`
2. Модификация транспортных фабрик для передачи заголовков авторизации
3. Обновление JSON схемы валидации для поддержки нового поля

Изменённые файлы:
- `src/shared/core/types.ts` - добавлено поле bearerToken в интерфейсы
- `src/shared/core/mcp-client.ts` - реализована передача токена в транспорты
- `src/schemas/server-config-schema.json` - обновлена схема валидации

## Проверка работы

Для проверки авторизации с Bearer токеном:

1. Создайте тестовый конфиг с токеном
2. Запустите тесты:

```bash
cd mcp-server-tester-sse-http-stdio
npm run build
REQUEST_TIMEOUT=30 node dist/cli.js tools test-all-tools.yaml --server-config server-remote-https-auth.json
```

Успешный результат:
```
📋 Tools Tests
✅ Tool discovery: 6/6 expected tools found
✅ Test md tool - Convert to Markdown: PASSED
✅ Test html tool - Get HTML content: PASSED
✅ Test execute_js - Run JavaScript: PASSED
✅ Test crawl - Multiple URLs: PASSED

📊 Results: 4/4 tests passed
```