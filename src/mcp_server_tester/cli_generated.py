"""
Command-line interface for MCP Server Tester Python wrapper.
Auto-generated from NPM package commands - DO NOT EDIT MANUALLY!
Use scripts/sync_commands.py to regenerate.
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import Optional

import click

from .core import MCPTester
from .exceptions import MCPTesterError



@click.group()
@click.version_option(version="1.0.0")
def main() -> None:
    """Python wrapper for mcp-server-tester-sse-http-stdio NPM package."""
    pass



@main.command()
@click.option("--server-config", help="MCP server configuration file (JSON)")
@click.option("--server-name", help="Specific server name to use from config (if multiple")
@click.option("--timeout", default='"10000"', help="Test timeout in milliseconds (default: \"10000\")")
@click.option("--debug", is_flag=True, help="Enable debug output with additional details")
@click.option("--junit-xml", default='junit.xml', is_flag=True, help="[filename]  Generate JUnit XML output (default: junit.xml)")
@click.option("--transport", help="Transport type: stdio|http")
@click.option("--url", help="Server URL for HTTP transport")
@click.option("--help", is_flag=True, help="Show help for command")
def tools(server_config, server_name, timeout, debug, junit_xml, transport, url, help):
    """[test-file]  Run MCP server tools tests (direct API testing)."""
    try:
        # Delegate to NPM package directly
        cmd = ["npx", "mcp-server-tester-sse-http-stdio", "tools"]
        if server_config:
            cmd.extend(["--server-config", str(server_config)])
        if server_name:
            cmd.extend(["--server-name", str(server_name)])
        if timeout:
            cmd.extend(["--timeout", str(timeout)])
        if debug:
            cmd.append("--debug")
        if junit_xml:
            cmd.append("--junit-xml")
        if transport:
            cmd.extend(["--transport", str(transport)])
        if url:
            cmd.extend(["--url", str(url)])
        if help:
            cmd.append("--help")

        # Execute command
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )

        # Output result
        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        sys.exit(result.returncode)

    except subprocess.TimeoutExpired:
        click.echo("Timeout executing tools command", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {{e}}", err=True)
        sys.exit(1)


@main.command()
@click.option("--version", is_flag=True, help="output the version number")
@click.option("--help", is_flag=True, help="Show help for command")
def Use(version, help):
    """"mcp-server-tester schema" to see test file"""
    try:
        # Delegate to NPM package directly
        cmd = ["npx", "mcp-server-tester-sse-http-stdio", "Use"]
        if version:
            cmd.append("--version")
        if help:
            cmd.append("--help")

        # Execute command
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )

        # Output result
        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        sys.exit(result.returncode)

    except subprocess.TimeoutExpired:
        click.echo("Timeout executing Use command", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {{e}}", err=True)
        sys.exit(1)


@main.command()
@click.option("--server-config", help="MCP server configuration file (JSON)")
@click.option("--server-name", help="Specific server name to use from config (if multiple")
@click.option("--timeout", default='"10000"', help="Test timeout in milliseconds (default: \"10000\")")
@click.option("--debug", is_flag=True, help="Enable debug output with additional details")
@click.option("--junit-xml", default='junit.xml', is_flag=True, help="[filename]  Generate JUnit XML output (default: junit.xml)")
@click.option("--transport", help="Transport type: stdio|http")
@click.option("--url", help="Server URL for HTTP transport")
@click.option("--help", is_flag=True, help="Show help for command")
def evals(server_config, server_name, timeout, debug, junit_xml, transport, url, help):
    """[test-file]  Run LLM evaluation tests (end-to-end testing"""
    try:
        # Delegate to NPM package directly
        cmd = ["npx", "mcp-server-tester-sse-http-stdio", "evals"]
        if server_config:
            cmd.extend(["--server-config", str(server_config)])
        if server_name:
            cmd.extend(["--server-name", str(server_name)])
        if timeout:
            cmd.extend(["--timeout", str(timeout)])
        if debug:
            cmd.append("--debug")
        if junit_xml:
            cmd.append("--junit-xml")
        if transport:
            cmd.extend(["--transport", str(transport)])
        if url:
            cmd.extend(["--url", str(url)])
        if help:
            cmd.append("--help")

        # Execute command
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )

        # Output result
        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        sys.exit(result.returncode)

    except subprocess.TimeoutExpired:
        click.echo("Timeout executing evals command", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {{e}}", err=True)
        sys.exit(1)


@main.command()
@click.option("--version", is_flag=True, help="output the version number")
@click.option("--help", is_flag=True, help="Show help for command")
def with(version, help):
    """real LLMs). Requires ANTHROPIC_API_KEY. Use"""
    try:
        # Delegate to NPM package directly
        cmd = ["npx", "mcp-server-tester-sse-http-stdio", "with"]
        if version:
            cmd.append("--version")
        if help:
            cmd.append("--help")

        # Execute command
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )

        # Output result
        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        sys.exit(result.returncode)

    except subprocess.TimeoutExpired:
        click.echo("Timeout executing with command", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {{e}}", err=True)
        sys.exit(1)


@main.command()
@click.option("--server-config", help="MCP server configuration file (JSON)")
@click.option("--server-name", help="Specific server name to use from config (if multiple")
@click.option("--categories", help="Test categories to run (comma-separated)")
@click.option("--output", default='"console"', help="Output format: console, json (default: \"console\")")
@click.option("--timeout", help="Overall timeout for compliance tests (default:")
@click.option("--help", is_flag=True, help="Show help for command")
def compliance(server_config, server_name, categories, output, timeout, help):
    """Run MCP protocol compliance checks"""
    try:
        # Delegate to NPM package directly
        cmd = ["npx", "mcp-server-tester-sse-http-stdio", "compliance"]
        if server_config:
            cmd.extend(["--server-config", str(server_config)])
        if server_name:
            cmd.extend(["--server-name", str(server_name)])
        if categories:
            cmd.extend(["--categories", str(categories)])
        if output:
            cmd.extend(["--output", str(output)])
        if timeout:
            cmd.extend(["--timeout", str(timeout)])
        if help:
            cmd.append("--help")

        # Execute command
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )

        # Output result
        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        sys.exit(result.returncode)

    except subprocess.TimeoutExpired:
        click.echo("Timeout executing compliance command", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {{e}}", err=True)
        sys.exit(1)


@main.command()
@click.option("--help", is_flag=True, help="Show help for command")
def schema(help):
    """Display JSON schema for test configuration files"""
    try:
        # Delegate to NPM package directly
        cmd = ["npx", "mcp-server-tester-sse-http-stdio", "schema"]
        if help:
            cmd.append("--help")

        # Execute command
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )

        # Output result
        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        sys.exit(result.returncode)

    except subprocess.TimeoutExpired:
        click.echo("Timeout executing schema command", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {{e}}", err=True)
        sys.exit(1)


@main.command()
@click.option("--version", is_flag=True, help="output the version number")
@click.option("--help", is_flag=True, help="Show help for command")
def help(version, help):
    """display help for command"""
    try:
        # Delegate to NPM package directly
        cmd = ["npx", "mcp-server-tester-sse-http-stdio", "help"]
        if version:
            cmd.append("--version")
        if help:
            cmd.append("--help")

        # Execute command
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )

        # Output result
        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)

        sys.exit(result.returncode)

    except subprocess.TimeoutExpired:
        click.echo("Timeout executing help command", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {{e}}", err=True)
        sys.exit(1)



if __name__ == "__main__":
    main()
