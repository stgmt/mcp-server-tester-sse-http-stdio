"""
Command-line interface for MCP Server Tester Python wrapper.
"""

import sys
import json
from pathlib import Path
from typing import Optional

import click
import yaml

from .core import MCPTester
from .exceptions import MCPTesterError


@click.group()
@click.version_option(version="1.0.0")
def main():
    """Python wrapper for mcp-server-tester-sse-http-stdio NPM package."""
    pass


@main.command()
@click.option("--server-config", "-s", required=True, help="Path to server configuration file")
@click.option("--test", "-t", required=True, help="Path to test configuration file") 
@click.option("--server-name", "-n", help="Name of server to test (required if multiple servers)")
@click.option("--timeout", default=30000, help="Timeout in milliseconds (default: 30000)")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--format", "-f", default="json", type=click.Choice(["json", "junit", "tap"]), help="Output format")
@click.option("--output", "-o", help="Output file path")
def test(
    server_config: str,
    test: str, 
    server_name: Optional[str],
    timeout: int,
    verbose: bool,
    format: str,
    output: Optional[str]
):
    """Test MCP server with given configuration."""
    try:
        tester = MCPTester()
        result = tester.test_server(
            server_config=server_config,
            test_config=test,
            server_name=server_name,
            timeout=timeout,
            verbose=verbose,
            format=format,
            output_file=output
        )
        
        if format == "json":
            click.echo(result.output)
        else:
            click.echo(result.output)
            
        # Exit with appropriate code
        sys.exit(0 if result.success else 1)
        
    except MCPTesterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--server-config", "-s", required=True, help="Path to server configuration file")
@click.option("--server-name", "-n", help="Name of server to test (required if multiple servers)")
def tools(server_config: str, server_name: Optional[str]):
    """List available tools from MCP server."""
    try:
        tester = MCPTester()
        tools_list = tester.list_tools(server_config, server_name)
        click.echo(json.dumps(tools_list, indent=2))
        
    except MCPTesterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("config_path")
def validate(config_path: str):
    """Validate MCP server configuration file."""
    try:
        tester = MCPTester()
        is_valid = tester.validate_config(config_path)
        
        if is_valid:
            click.echo(f"✓ Configuration file '{config_path}' is valid")
            sys.exit(0)
        else:
            click.echo(f"✗ Configuration file '{config_path}' is invalid", err=True)
            sys.exit(1)
            
    except MCPTesterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--output", "-o", help="Output file path (default: server-config.json)")
def create_server_config(output: Optional[str]):
    """Interactive creation of server configuration file."""
    servers = {}
    
    while True:
        server_name = click.prompt("Enter server name (or 'done' to finish)")
        if server_name.lower() == 'done':
            break
            
        transport = click.prompt(
            "Select transport", 
            type=click.Choice(["sse", "stdio", "http"])
        )
        
        server_config = {"transport": transport}
        
        if transport == "sse":
            url = click.prompt("Enter SSE URL (e.g., http://localhost:8001/sse)")
            server_config["url"] = url
        elif transport == "stdio":
            command = click.prompt("Enter command (e.g., python)")
            args = click.prompt("Enter arguments (space-separated, optional)", default="")
            server_config["command"] = command
            if args:
                server_config["args"] = args.split()
        elif transport == "http":
            url = click.prompt("Enter HTTP URL (e.g., http://localhost:8000)")
            server_config["url"] = url
            
        servers[server_name] = server_config
    
    if not servers:
        click.echo("No servers configured.")
        return
        
    output_path = output or "server-config.json"
    config_json = MCPTester.create_server_config(servers, output_path)
    
    click.echo(f"✓ Server configuration saved to '{output_path}'")


@main.command()
@click.option("--output", "-o", help="Output file path (default: test-config.yaml)")
def create_test_config(output: Optional[str]):
    """Interactive creation of test configuration file."""
    tests = []
    
    while True:
        test_name = click.prompt("Enter test name (or 'done' to finish)")
        if test_name.lower() == 'done':
            break
            
        test_config = {"name": test_name}
        
        # Add test calls
        calls = []
        while True:
            tool_name = click.prompt("Enter tool name to test (or 'done' for this test)")
            if tool_name.lower() == 'done':
                break
                
            call_config = {"tool": tool_name}
            
            # Add arguments
            has_args = click.confirm("Does this tool call have arguments?", default=False)
            if has_args:
                args_str = click.prompt("Enter arguments as JSON")
                try:
                    call_config["arguments"] = json.loads(args_str)
                except json.JSONDecodeError:
                    click.echo("Invalid JSON, skipping arguments")
            
            calls.append(call_config)
            
        if calls:
            test_config["calls"] = calls
            tests.append(test_config)
    
    if not tests:
        click.echo("No tests configured.")
        return
        
    output_path = output or "test-config.yaml"  
    config_yaml = MCPTester.create_test_config(tests, output_path)
    
    click.echo(f"✓ Test configuration saved to '{output_path}'")


@main.command()
def doctor():
    """Check system requirements and NPM package status."""
    import shutil
    import subprocess
    
    click.echo("🏥 MCP Server Tester Doctor")
    click.echo("=" * 30)
    
    # Check Node.js
    node_path = shutil.which("node")
    if node_path:
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            node_version = result.stdout.strip()
            click.echo(f"✓ Node.js: {node_version} at {node_path}")
        except Exception:
            click.echo("✗ Node.js: Found but version check failed", err=True)
    else:
        click.echo("✗ Node.js: Not found", err=True)
        click.echo("  Install from: https://nodejs.org/")
    
    # Check NPM
    npm_path = shutil.which("npm")
    if npm_path:
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            npm_version = result.stdout.strip()
            click.echo(f"✓ NPM: {npm_version} at {npm_path}")
        except Exception:
            click.echo("✗ NPM: Found but version check failed", err=True)
    else:
        click.echo("✗ NPM: Not found", err=True)
    
    # Check NPX
    npx_path = shutil.which("npx")
    if npx_path:
        click.echo(f"✓ NPX: Available at {npx_path}")
    else:
        click.echo("✗ NPX: Not found", err=True)
    
    # Check MCP Tester NPM package
    try:
        result = subprocess.run(
            ["npx", "mcp-server-tester-sse-http-stdio", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            click.echo(f"✓ mcp-server-tester-sse-http-stdio: {version}")
        else:
            click.echo("✗ mcp-server-tester-sse-http-stdio: Package error", err=True)
    except subprocess.TimeoutExpired:
        click.echo("✗ mcp-server-tester-sse-http-stdio: Timeout", err=True)
    except Exception:
        click.echo("✗ mcp-server-tester-sse-http-stdio: Not available", err=True)
        click.echo("  Install with: npm install -g mcp-server-tester-sse-http-stdio")
    
    click.echo("\n🎯 Ready to test MCP servers!")


if __name__ == "__main__":
    main()