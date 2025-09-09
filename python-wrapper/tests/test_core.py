"""
Tests for MCP Server Tester Python wrapper core functionality.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from mcp_server_tester.core import MCPTester, MCPTestResult, MCPTestConfig
from mcp_server_tester.exceptions import (
    NodeJSNotFoundError,
    NPMPackageNotFoundError,
    MCPTestExecutionError,
    MCPConfigurationError,
)


class TestMCPTester:
    """Test MCPTester class."""

    def test_init_success(self):
        """Test successful initialization."""
        with patch("shutil.which", return_value="/usr/bin/node"), patch(
            "subprocess.run"
        ) as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="help text", stderr="")

            tester = MCPTester()
            assert tester.npm_package_name == "mcp-server-tester-sse-http-stdio"

    def test_init_no_nodejs(self):
        """Test initialization fails when Node.js not found."""
        with patch("shutil.which", return_value=None):
            with pytest.raises(NodeJSNotFoundError):
                MCPTester()

    def test_init_no_npm_package(self):
        """Test initialization fails when NPM package not found."""
        with patch("shutil.which", return_value="/usr/bin/node"), patch(
            "subprocess.run"
        ) as mock_run:
            mock_run.return_value = Mock(
                returncode=1, stdout="", stderr="command not found"
            )

            with pytest.raises(NPMPackageNotFoundError):
                MCPTester()

    def test_test_server_with_paths(self):
        """Test server testing with file paths."""
        with patch("shutil.which", return_value="/usr/bin/node"), patch(
            "subprocess.run"
        ) as mock_run_init, patch.object(Path, "exists", return_value=True):

            # Mock initialization check
            mock_run_init.return_value = Mock(returncode=0, stdout="help", stderr="")
            tester = MCPTester()

            # Mock test execution
            test_output = {
                "success": True,
                "passed": 5,
                "total": 5,
                "failed": [],
                "execution_time": 1.23,
            }

            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(
                    returncode=0, stdout=json.dumps(test_output), stderr=""
                )

                result = tester.test_server(
                    server_config="server.json",
                    test_config="test.yaml",
                    server_name="test-server",
                )

                assert isinstance(result, MCPTestResult)
                assert result.success is True
                assert result.passed_tests == 5
                assert result.total_tests == 5
                assert result.failed_tests == []
                assert result.execution_time == 1.23

    def test_test_server_with_dicts(self):
        """Test server testing with config dictionaries."""
        server_config = {
            "mcpServers": {
                "test-server": {"transport": "sse", "url": "http://localhost:8001/sse"}
            }
        }

        test_config = {
            "tools": {
                "tests": [{"name": "test-tool", "calls": [{"tool": "list_files"}]}]
            }
        }

        with patch("shutil.which", return_value="/usr/bin/node"), patch(
            "subprocess.run"
        ) as mock_run_init, patch("tempfile.NamedTemporaryFile") as mock_temp:

            # Mock initialization
            mock_run_init.return_value = Mock(returncode=0, stdout="help", stderr="")
            tester = MCPTester()

            # Mock temp files
            mock_temp.return_value.__enter__.return_value.name = "/tmp/config.json"

            test_output = {"success": True, "passed": 1, "total": 1, "failed": []}

            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(
                    returncode=0, stdout=json.dumps(test_output), stderr=""
                )

                result = tester.test_server(
                    server_config=server_config, test_config=test_config
                )

                assert result.success is True
                assert result.passed_tests == 1

    def test_test_execution_failure(self):
        """Test handling of test execution failure."""
        with patch("shutil.which", return_value="/usr/bin/node"), patch(
            "subprocess.run"
        ) as mock_run_init, patch.object(Path, "exists", return_value=True):

            # Mock initialization
            mock_run_init.return_value = Mock(returncode=0, stdout="help", stderr="")
            tester = MCPTester()

            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(
                    returncode=1, stdout="", stderr="Test failed: Connection refused"
                )

                with pytest.raises(MCPTestExecutionError) as exc_info:
                    tester.test_server("server.json", "test.yaml")

                assert exc_info.value.return_code == 1
                assert "Connection refused" in exc_info.value.stderr

    def test_create_server_config(self):
        """Test server configuration creation."""
        servers = {
            "sse-server": {"transport": "sse", "url": "http://localhost:8001/sse"},
            "stdio-server": {
                "transport": "stdio",
                "command": "python",
                "args": ["-m", "my_server"],
            },
        }

        config_json = MCPTester.create_server_config(servers)
        config = json.loads(config_json)

        assert "mcpServers" in config
        assert "sse-server" in config["mcpServers"]
        assert "stdio-server" in config["mcpServers"]
        assert config["mcpServers"]["sse-server"]["transport"] == "sse"
        assert config["mcpServers"]["stdio-server"]["transport"] == "stdio"

    def test_create_test_config(self):
        """Test test configuration creation."""
        tests = [
            {
                "name": "basic-test",
                "calls": [
                    {"tool": "list_files"},
                    {"tool": "read_file", "arguments": {"path": "test.txt"}},
                ],
            }
        ]

        config_yaml = MCPTester.create_test_config(tests)

        # Basic validation - contains expected structure
        assert "tools:" in config_yaml
        assert "tests:" in config_yaml
        assert "name: basic-test" in config_yaml

    def test_validate_config(self):
        """Test configuration validation."""
        with patch("shutil.which", return_value="/usr/bin/node"), patch(
            "subprocess.run"
        ) as mock_run_init:

            # Mock initialization
            mock_run_init.return_value = Mock(returncode=0, stdout="help", stderr="")
            tester = MCPTester()

            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

                is_valid = tester.validate_config("config.json")
                assert is_valid is True

                # Test invalid config
                mock_run.return_value = Mock(returncode=1, stdout="", stderr="")
                is_valid = tester.validate_config("invalid.json")
                assert is_valid is False


class TestMCPTestResult:
    """Test MCPTestResult dataclass."""

    def test_creation(self):
        """Test MCPTestResult creation."""
        result = MCPTestResult(
            success=True,
            passed_tests=3,
            total_tests=3,
            failed_tests=[],
            execution_time=2.5,
            output="All tests passed",
        )

        assert result.success is True
        assert result.passed_tests == 3
        assert result.total_tests == 3
        assert result.failed_tests == []
        assert result.execution_time == 2.5
        assert result.output == "All tests passed"
        assert result.error == ""


class TestMCPTestConfig:
    """Test MCPTestConfig dataclass."""

    def test_creation(self):
        """Test MCPTestConfig creation."""
        config = MCPTestConfig(
            server_config_path="server.json",
            test_path="test.yaml",
            server_name="my-server",
            timeout=60000,
            verbose=True,
            format="junit",
        )

        assert config.server_config_path == "server.json"
        assert config.test_path == "test.yaml"
        assert config.server_name == "my-server"
        assert config.timeout == 60000
        assert config.verbose is True
        assert config.format == "junit"

    def test_defaults(self):
        """Test default values."""
        config = MCPTestConfig(server_config_path="server.json", test_path="test.yaml")

        assert config.server_name is None
        assert config.timeout == 30000
        assert config.verbose is False
        assert config.format == "json"
        assert config.output_file is None
