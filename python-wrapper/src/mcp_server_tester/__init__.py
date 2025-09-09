"""
Python wrapper for mcp-server-tester-sse-http-stdio NPM package.

This package provides a Python interface to the TypeScript/Node.js MCP Server Tester,
enabling easy testing of Model Context Protocol servers from Python applications.
"""

__version__ = "1.0.0"
__author__ = "stgmt"
__email__ = "your-email@example.com"

from .core import MCPTester, MCPTestResult, MCPTestConfig
from .exceptions import MCPTesterError, NodeJSNotFoundError, NPMPackageNotFoundError

__all__ = [
    "MCPTester",
    "MCPTestResult",
    "MCPTestConfig",
    "MCPTesterError",
    "NodeJSNotFoundError",
    "NPMPackageNotFoundError",
]
