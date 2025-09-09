"""
Exceptions for MCP Server Tester Python wrapper.
"""


class MCPTesterError(Exception):
    """Base exception for all MCP Tester errors."""
    pass


class NodeJSNotFoundError(MCPTesterError):
    """Raised when Node.js is not found on the system."""
    
    def __init__(self, message: str = "Node.js not found. Please install Node.js >= 18.0.0"):
        super().__init__(message)


class NPMPackageNotFoundError(MCPTesterError):
    """Raised when mcp-server-tester-sse-http-stdio NPM package is not found."""
    
    def __init__(self, message: str = "NPM package 'mcp-server-tester-sse-http-stdio' not found. Run: npm install -g mcp-server-tester-sse-http-stdio"):
        super().__init__(message)


class MCPTestExecutionError(MCPTesterError):
    """Raised when test execution fails."""
    
    def __init__(self, message: str, return_code: int = 1, stderr: str = ""):
        super().__init__(message)
        self.return_code = return_code
        self.stderr = stderr


class MCPConfigurationError(MCPTesterError):
    """Raised when configuration is invalid."""
    pass