# 🐳 MCP Server Tester - Universal Docker Image
# 
# 🔗 GitHub Repository: https://github.com/stgmt/mcp-server-tester-sse-http-stdio
# 📦 NPM Package: https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio
# 🐍 PyPI Package: https://pypi.org/project/mcp-server-tester/
# 🐳 Docker Hub: https://hub.docker.com/r/stgmt/mcp-server-tester
# 
# Поддерживает все 3 способа использования:
# 1. NPM пакет (Node.js/TypeScript)
# 2. Python пакет 
# 3. Docker контейнер (этот файл)
#
# Использование:
#   docker run --rm -v $(pwd):/workspace mcp-server-tester tools test.yaml --server-config config.json

FROM node:20-alpine

# Метаданные
LABEL maintainer="MCP Server Tester Team"
LABEL version="1.4.1" 
LABEL description="Universal MCP Server Tester with NPM, Python, and Docker support"
LABEL org.opencontainers.image.source="https://github.com/stgmt/mcp-server-tester-sse-http-stdio"
LABEL org.opencontainers.image.url="https://github.com/stgmt/mcp-server-tester-sse-http-stdio"
LABEL org.opencontainers.image.documentation="https://github.com/stgmt/mcp-server-tester-sse-http-stdio#readme"

# Установка системных зависимостей
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    build-base \
    curl \
    git \
    bash \
    jq

# Создание символической ссылки для python
RUN ln -sf python3 /usr/bin/python

# Установка глобального NPM пакета
RUN npm install -g mcp-server-tester-sse-http-stdio

# Создание рабочей директории
WORKDIR /app

# Копирование Python wrapper исходников
COPY src/ ./src/
COPY requirements.txt ./
COPY setup.py ./
COPY pyproject.toml ./
COPY README.md ./

# Обновляем ca-certificates для решения SSL проблем
RUN apk update && apk add --no-cache ca-certificates && update-ca-certificates

# Установка Python зависимостей и пакета (обходим ограничения Alpine)
RUN pip3 install --break-system-packages --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --break-system-packages --no-cache-dir -r requirements.txt && \
    pip3 install --break-system-packages --no-cache-dir -e .

# Создание entrypoint скрипта
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Создание удобных алиасов
RUN echo 'alias mcp-tester="mcp-server-tester"' >> /etc/bash.bashrc && \
    echo 'alias mcp-test="mcp-server-tester test"' >> /etc/bash.bashrc

# Рабочая директория для пользовательских файлов
WORKDIR /workspace

# Добавляем полезные утилиты в PATH
ENV PATH="/usr/local/bin:${PATH}"

# Установка по умолчанию
ENV MCP_TESTER_DEFAULT_TIMEOUT=30000
ENV MCP_TESTER_DEFAULT_FORMAT=console

# Открытые порты (для тестирования локальных серверов)
EXPOSE 8000 8001 8080

# Проверка здоровья контейнера
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node --version && python3 --version && mcp-server-tester --version || exit 1

# Entrypoint для гибкого использования
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Команда по умолчанию - показать help
CMD ["--help"]