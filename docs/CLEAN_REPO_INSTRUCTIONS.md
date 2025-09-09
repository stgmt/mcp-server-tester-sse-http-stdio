# 🔄 Инструкции по замене репозитория на чистую версию

## ⚠️ ВНИМАНИЕ: Это удалит всю историю коммитов!

### Вариант 1: Force Push (перезапись истории)

```bash
# Перейти в чистый репозиторий
cd /tmp/mcp-server-tester-clean

# Force push в main ветку (УДАЛИТ ВСЮ ИСТОРИЮ!)
git push -f origin main

# Или если хотите сохранить старую историю в другой ветке:
git push origin main:old-history
git push -f origin main
```

### Вариант 2: Создать новый репозиторий

```bash
# 1. Переименовать старый репозиторий (для backup)
gh repo rename mcp-server-tester-sse-http-stdio-old

# 2. Создать новый репозиторий
gh repo create mcp-server-tester-sse-http-stdio \
  --public \
  --description "🧪 Universal MCP (Model Context Protocol) server tester supporting HTTP, SSE (Server-Sent Events), and STDIO transports. Test AI/LLM tools, Anthropic MCP servers, OpenAI-compatible APIs. TypeScript, YAML configs."

# 3. Перейти в чистый репозиторий
cd /tmp/mcp-server-tester-clean

# 4. Установить remote
git remote set-url origin https://github.com/stgmt/mcp-server-tester-sse-http-stdio.git

# 5. Push чистая версия
git push -u origin main
```

### Вариант 3: Архивировать старую историю

```bash
# 1. В старом репозитории создать архивную ветку
cd /tmp/mcp-server-tester-sse
git checkout -b archive/old-history
git push origin archive/old-history

# 2. Переключиться на чистый репозиторий
cd /tmp/mcp-server-tester-clean

# 3. Force push в main
git push -f origin main
```

## 📁 Что находится в чистом репозитории:

- ✅ Все файлы из текущей версии
- ✅ README с AI/SEO оптимизацией
- ✅ Некоммерческая лицензия
- ✅ Все примеры и тесты
- ❌ НЕТ истории коммитов
- ❌ НЕТ упоминаний о форке
- ❌ НЕТ старых авторов

## 🎯 Результат:

Репозиторий будет выглядеть как только что созданный с одним начальным коммитом:
- "Initial commit - MCP Server Tester v1.4.0"

## ⚡ Быстрая команда для force push:

```bash
cd /tmp/mcp-server-tester-clean && git push -f origin main
```

## 🔍 Проверка:

После push проверьте на GitHub:
- История коммитов должна показывать только 1 коммит
- Все файлы должны быть на месте
- Contributors должен показывать только вас