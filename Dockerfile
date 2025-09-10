# 🐳 MCP Server Tester - Universal Docker Image
# 
# 🔗 GitHub Repository: https://github.com/stgmt/mcp-server-tester-sse-http-stdio
# 📦 NPM Package: https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio
# 🐍 PyPI Package: https://pypi.org/project/mcp-server-tester/
# 🐳 Docker Hub: https://hub.docker.com/r/stgmt/mcp-server-tester-sse-http-stdio
# 
# Supports all 3 usage methods:
# 1. NPM package (Node.js/TypeScript)
# 2. Python package 
# 3. Docker container (this file)
#
# Usage:
#   docker run --rm -v $(pwd):/workspace mcp-server-tester-sse-http-stdio tools test.yaml --server-config config.json

FROM node:20-alpine

# Metadata
LABEL maintainer="MCP Server Tester Team"
LABEL version="1.4.1" 
LABEL description="Universal MCP Server Tester with NPM, Python, and Docker support"
LABEL org.opencontainers.image.source="https://github.com/stgmt/mcp-server-tester-sse-http-stdio"
LABEL org.opencontainers.image.url="https://github.com/stgmt/mcp-server-tester-sse-http-stdio"
LABEL org.opencontainers.image.documentation="https://github.com/stgmt/mcp-server-tester-sse-http-stdio#readme"

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    build-base \
    curl \
    git \
    bash \
    jq

# Create symbolic link for python
RUN ln -sf python3 /usr/bin/python

# Install global NPM package
RUN npm install -g mcp-server-tester-sse-http-stdio

# Create working directory
WORKDIR /app

# Copy Python wrapper sources
COPY python-wrapper/src/ ./src/
COPY python-wrapper/requirements.txt ./
COPY python-wrapper/setup.py ./
COPY python-wrapper/pyproject.toml ./
COPY python-wrapper/README.md ./

# Update ca-certificates to fix SSL issues
RUN apk update && apk add --no-cache ca-certificates && update-ca-certificates

# Install Python dependencies and package (bypass Alpine restrictions)
RUN pip3 install --break-system-packages --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --break-system-packages --no-cache-dir -r requirements.txt && \
    pip3 install --break-system-packages --no-cache-dir -e .

# Create entrypoint script
COPY python-wrapper/docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Create convenient aliases
RUN echo 'alias mcp-tester="mcp-server-tester"' >> /etc/bash.bashrc && \
    echo 'alias mcp-test="mcp-server-tester test"' >> /etc/bash.bashrc

# Working directory for user files
WORKDIR /workspace

# Add useful utilities to PATH
ENV PATH="/usr/local/bin:${PATH}"

# Default environment settings
ENV MCP_TESTER_DEFAULT_TIMEOUT=30000
ENV MCP_TESTER_DEFAULT_FORMAT=console

# Exposed ports (for testing local servers)
EXPOSE 8000 8001 8080

# Container health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node --version && python3 --version && mcp-server-tester --version || exit 1

# Entrypoint for flexible usage
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command - show help
CMD ["--help"]