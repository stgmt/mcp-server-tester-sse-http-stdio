"""
Tests for CLI functionality.
"""

import json
import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch

from mcp_server_tester.cli import main
from mcp_server_tester.core import MCPTestResult
from mcp_server_tester.exceptions import NodeJSNotFoundError


class TestCLI:
    """Test CLI commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_main_help(self):
        """Test main help command."""
        result = self.runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Python wrapper for mcp-server-tester-sse-http-stdio" in result.output

    def test_test_command_success(self):
        """Test successful test command."""
        test_result = MCPTestResult(
            success=True,
            passed_tests=3,
            total_tests=3,
            failed_tests=[],
            execution_time=1.5,
            output='{"success": true, "passed": 3, "total": 3}',
        )

        with patch("mcp_server_tester.cli.MCPTester") as mock_tester_class:
            mock_tester = Mock()
            mock_tester.test_server.return_value = test_result
            mock_tester_class.return_value = mock_tester

            result = self.runner.invoke(
                main,
                [
                    "test",
                    "--server-config",
                    "server.json",
                    "--test",
                    "test.yaml",
                    "--server-name",
                    "test-server",
                ],
            )

            assert result.exit_code == 0
            assert "success" in result.output

    def test_test_command_failure(self):
        """Test test command with failure."""
        test_result = MCPTestResult(
            success=False,
            passed_tests=1,
            total_tests=3,
            failed_tests=[{"name": "test1", "error": "Failed"}],
            execution_time=1.2,
            output='{"success": false, "failed": 2}',
        )

        with patch("mcp_server_tester.cli.MCPTester") as mock_tester_class:
            mock_tester = Mock()
            mock_tester.test_server.return_value = test_result
            mock_tester_class.return_value = mock_tester

            result = self.runner.invoke(
                main, ["test", "--server-config", "server.json", "--test", "test.yaml"]
            )

            assert result.exit_code == 1
            assert "success" in result.output

    def test_test_command_error(self):
        """Test test command with error."""
        with patch("mcp_server_tester.cli.MCPTester") as mock_tester_class:
            mock_tester_class.side_effect = NodeJSNotFoundError()

            result = self.runner.invoke(
                main, ["test", "--server-config", "server.json", "--test", "test.yaml"]
            )

            assert result.exit_code == 1
            assert "Error:" in result.output
            assert "Node.js not found" in result.output

    def test_tools_command(self):
        """Test tools command with test file."""
        with patch("mcp_server_tester.cli.MCPTester") as mock_tester_class:
            mock_tester = Mock()
            test_result = MCPTestResult(
                success=True,
                passed_tests=5,
                total_tests=5,
                failed_tests=[],
                execution_time=1.23,
                output='{"success": true, "passed": 5, "total": 5}',
            )
            mock_tester.run_tools_test.return_value = test_result
            mock_tester_class.return_value = mock_tester

            result = self.runner.invoke(
                main, ["tools", "test.json", "--server-config", "server.json"]
            )

            assert result.exit_code == 0
            assert "success" in result.output

    def test_validate_command_valid(self):
        """Test validate command with valid config."""
        with patch("mcp_server_tester.cli.MCPTester") as mock_tester_class:
            mock_tester = Mock()
            mock_tester.validate_config.return_value = True
            mock_tester_class.return_value = mock_tester

            result = self.runner.invoke(main, ["validate", "config.json"])

            assert result.exit_code == 0
            assert "✓ Configuration file 'config.json' is valid" in result.output

    def test_validate_command_invalid(self):
        """Test validate command with invalid config."""
        with patch("mcp_server_tester.cli.MCPTester") as mock_tester_class:
            mock_tester = Mock()
            mock_tester.validate_config.return_value = False
            mock_tester_class.return_value = mock_tester

            result = self.runner.invoke(main, ["validate", "config.json"])

            assert result.exit_code == 1
            assert "✗ Configuration file 'config.json' is invalid" in result.output

    def test_doctor_command(self):
        """Test doctor command."""
        with patch("shutil.which") as mock_which, patch("subprocess.run") as mock_run:

            # Mock system tools
            mock_which.side_effect = lambda cmd: {
                "node": "/usr/bin/node",
                "npm": "/usr/bin/npm",
                "npx": "/usr/bin/npx",
            }.get(cmd)

            # Mock version commands
            mock_run.side_effect = [
                Mock(returncode=0, stdout="v18.17.0\n", stderr=""),  # node --version
                Mock(returncode=0, stdout="9.6.7\n", stderr=""),  # npm --version
                Mock(
                    returncode=0, stdout="1.4.1\n", stderr=""
                ),  # npx mcp-server-tester --version
            ]

            result = self.runner.invoke(main, ["doctor"])

            assert result.exit_code == 0
            assert "MCP Server Tester Doctor" in result.output
            assert "✓ Node.js: v18.17.0" in result.output
            assert "✓ NPM: 9.6.7" in result.output
            assert "Ready to test MCP servers!" in result.output

    def test_create_server_config_interactive(self):
        """Test interactive server config creation."""
        # This would be complex to test due to interactive prompts
        # For now, just test that the command exists
        result = self.runner.invoke(main, ["create-server-config", "--help"])
        assert result.exit_code == 0
        assert "Interactive creation of server configuration" in result.output

    def test_create_test_config_interactive(self):
        """Test interactive test config creation."""
        # This would be complex to test due to interactive prompts
        # For now, just test that the command exists
        result = self.runner.invoke(main, ["create-test-config", "--help"])
        assert result.exit_code == 0
        assert "Interactive creation of test configuration" in result.output
