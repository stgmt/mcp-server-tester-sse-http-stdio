"""
Core functionality for MCP Server Tester Python wrapper.
"""

import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
import yaml

from .exceptions import (
    NodeJSNotFoundError,
    NPMPackageNotFoundError,
    MCPTestExecutionError,
    MCPConfigurationError,
)


@dataclass
class MCPTestResult:
    """Result of MCP server test execution."""

    success: bool
    passed_tests: int
    total_tests: int
    failed_tests: List[Dict[str, Any]]
    execution_time: float
    output: str
    error: str = ""


@dataclass
class MCPTestConfig:
    """Configuration for MCP server testing."""

    server_config_path: str
    test_path: str
    server_name: Optional[str] = None
    timeout: int = 30000  # milliseconds
    verbose: bool = False
    format: str = "json"  # json, junit, tap
    output_file: Optional[str] = None


class MCPTester:
    """Python wrapper for mcp-server-tester-sse-http-stdio NPM package."""

    def __init__(self, npm_package_name: str = "mcp-server-tester-sse-http-stdio"):
        self.npm_package_name = npm_package_name
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Check if Node.js and NPM package are available."""
        # Check Node.js
        if not shutil.which("node"):
            raise NodeJSNotFoundError()

        # Check NPM package
        try:
            result = subprocess.run(
                ["npx", self.npm_package_name, "--help"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                raise NPMPackageNotFoundError()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            raise NPMPackageNotFoundError()

    def test_server(
        self,
        server_config: Union[str, Path, Dict[str, Any]],
        test_config: Union[str, Path, Dict[str, Any]],
        server_name: Optional[str] = None,
        timeout: int = 30000,
        verbose: bool = False,
        format: str = "json",
        output_file: Optional[str] = None,
    ) -> MCPTestResult:
        """
        Test MCP server with given configuration.

        Args:
            server_config: Path to server config file or config dict
            test_config: Path to test config file or config dict
            server_name: Name of server to test (required if multiple servers in config)
            timeout: Timeout in milliseconds
            verbose: Enable verbose output
            format: Output format (json, junit, tap)
            output_file: Path to save output file

        Returns:
            MCPTestResult with test execution results

        Raises:
            MCPTestExecutionError: If test execution fails
            MCPConfigurationError: If configuration is invalid
        """

        # Handle config files vs dicts
        server_config_path = self._prepare_config(server_config, "server_config")
        test_config_path = self._prepare_config(test_config, "test_config")

        # Build command
        cmd = ["npx", self.npm_package_name]
        cmd.extend(["--server-config", server_config_path])
        cmd.extend(["--test", test_config_path])

        if server_name:
            cmd.extend(["--server-name", server_name])
        if timeout != 30000:
            cmd.extend(["--timeout", str(timeout)])
        if verbose:
            cmd.append("--verbose")
        if format != "json":
            cmd.extend(["--format", format])
        if output_file:
            cmd.extend(["--output", output_file])

        # Execute command
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout / 1000.0,  # Convert to seconds
                cwd=Path.cwd(),
            )

            # Parse results
            return self._parse_result(result, format)

        except subprocess.TimeoutExpired:
            raise MCPTestExecutionError(f"Test execution timed out after {timeout}ms")
        except Exception as e:
            raise MCPTestExecutionError(f"Test execution failed: {str(e)}")

    def _prepare_config(
        self, config: Union[str, Path, Dict[str, Any]], config_type: str
    ) -> str:
        """Prepare configuration file path or create temporary file from dict."""
        if isinstance(config, (str, Path)):
            config_path = Path(config)
            if not config_path.exists():
                raise MCPConfigurationError(
                    f"{config_type} file not found: {config_path}"
                )
            return str(config_path)

        elif isinstance(config, dict):
            # Create temporary config file
            import tempfile

            suffix = ".yaml" if config_type == "test_config" else ".json"

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=suffix, delete=False
            ) as tmp_file:
                if suffix == ".yaml":
                    yaml.dump(config, tmp_file, default_flow_style=False)
                else:
                    json.dump(config, tmp_file, indent=2)
                return tmp_file.name

        else:
            raise MCPConfigurationError(
                f"Invalid {config_type} type. Expected str, Path, or dict."
            )

    def _parse_result(
        self, result: subprocess.CompletedProcess, format: str
    ) -> MCPTestResult:
        """Parse command execution result into MCPTestResult."""

        if result.returncode != 0:
            raise MCPTestExecutionError(
                f"Test execution failed with return code {result.returncode}",
                return_code=result.returncode,
                stderr=result.stderr,
            )

        if format == "json":
            try:
                output_data = json.loads(result.stdout)
                return MCPTestResult(
                    success=output_data.get("success", False),
                    passed_tests=output_data.get("passed", 0),
                    total_tests=output_data.get("total", 0),
                    failed_tests=output_data.get("failed", []),
                    execution_time=output_data.get("execution_time", 0.0),
                    output=result.stdout,
                )
            except json.JSONDecodeError:
                # Fallback for non-JSON output
                return MCPTestResult(
                    success=result.returncode == 0,
                    passed_tests=1 if result.returncode == 0 else 0,
                    total_tests=1,
                    failed_tests=(
                        []
                        if result.returncode == 0
                        else [{"error": "JSON parsing failed"}]
                    ),
                    execution_time=0.0,
                    output=result.stdout,
                    error=result.stderr,
                )
        else:
            # For non-JSON formats, return basic result
            return MCPTestResult(
                success=result.returncode == 0,
                passed_tests=1 if result.returncode == 0 else 0,
                total_tests=1,
                failed_tests=(
                    [] if result.returncode == 0 else [{"error": "Test failed"}]
                ),
                execution_time=0.0,
                output=result.stdout,
                error=result.stderr,
            )

    def list_tools(
        self,
        server_config: Union[str, Path, Dict[str, Any]],
        server_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List available tools from MCP server."""
        # This would use the tools listing functionality
        cmd = ["npx", self.npm_package_name, "tools"]
        cmd.extend(
            ["--server-config", self._prepare_config(server_config, "server_config")]
        )
        if server_name:
            cmd.extend(["--server-name", server_name])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise MCPTestExecutionError(
                "Failed to list tools", result.returncode, result.stderr
            )

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return []

    def validate_config(self, config_path: Union[str, Path]) -> bool:
        """Validate MCP server configuration."""
        cmd = ["npx", self.npm_package_name, "validate", str(config_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0

    @staticmethod
    def create_server_config(
        servers: Dict[str, Dict[str, Any]],
        output_path: Optional[Union[str, Path]] = None,
    ) -> str:
        """Create server configuration file."""
        config = {"mcpServers": servers}

        if output_path:
            config_path = Path(output_path)
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            return str(config_path)
        else:
            return json.dumps(config, indent=2)

    @staticmethod
    def create_test_config(
        tests: List[Dict[str, Any]], output_path: Optional[Union[str, Path]] = None
    ) -> str:
        """Create test configuration file."""
        config = {"tools": {"tests": tests}}

        if output_path:
            config_path = Path(output_path)
            with open(config_path, "w") as f:
                yaml.dump(config, f, default_flow_style=False)
            return str(config_path)
        else:
            return yaml.dump(config, default_flow_style=False)
