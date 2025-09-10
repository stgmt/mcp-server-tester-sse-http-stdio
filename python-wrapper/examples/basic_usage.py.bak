#!/usr/bin/env python3
"""
Basic usage example for MCP Server Tester Python wrapper.
"""

import json
from pathlib import Path
from mcp_server_tester import MCPTester


def main():
    """Basic usage example."""
    
    # Initialize the tester
    print("🔧 Initializing MCP Server Tester...")
    try:
        tester = MCPTester()
        print("✅ Tester initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("💡 Run 'mcp-server-tester doctor' to check dependencies")
        return
    
    # Example 1: Testing with configuration dictionaries
    print("\\n📋 Example 1: Testing with configuration dictionaries")
    
    server_config = {
        "mcpServers": {
            "example-server": {
                "transport": "sse",
                "url": "http://localhost:8001/sse"
            }
        }
    }
    
    test_config = {
        "tools": {
            "tests": [
                {
                    "name": "Basic functionality test",
                    "calls": [
                        {"tool": "list_files"},
                        {
                            "tool": "read_file", 
                            "arguments": {"path": "README.md"}
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        print("🚀 Running tests...")
        result = tester.test_server(
            server_config=server_config,
            test_config=test_config,
            server_name="example-server",
            timeout=10000,  # 10 seconds
            verbose=True
        )
        
        print_test_results(result)
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
    
    # Example 2: Creating configuration files
    print("\\n📋 Example 2: Creating configuration files")
    
    # Create server configuration
    servers = {
        "local-sse-server": {
            "transport": "sse", 
            "url": "http://localhost:8001/sse"
        },
        "local-stdio-server": {
            "transport": "stdio",
            "command": "python",
            "args": ["-m", "my_mcp_server", "--port", "8002"]
        }
    }
    
    server_config_path = "example-server-config.json"
    tester.create_server_config(servers, server_config_path)
    print(f"✅ Server configuration created: {server_config_path}")
    
    # Create test configuration
    tests = [
        {
            "name": "File operations test",
            "calls": [
                {"tool": "list_files"},
                {"tool": "read_file", "arguments": {"path": "test.txt"}},
                {"tool": "write_file", "arguments": {"path": "output.txt", "content": "Hello!"}}
            ]
        },
        {
            "name": "Error handling test", 
            "calls": [
                {"tool": "nonexistent_tool", "expect_error": True}
            ]
        }
    ]
    
    test_config_path = "example-test-config.yaml"
    tester.create_test_config(tests, test_config_path)
    print(f"✅ Test configuration created: {test_config_path}")
    
    # Example 3: Configuration validation
    print("\\n📋 Example 3: Configuration validation")
    
    try:
        is_valid = tester.validate_config(server_config_path)
        if is_valid:
            print(f"✅ Configuration '{server_config_path}' is valid")
        else:
            print(f"❌ Configuration '{server_config_path}' is invalid")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
    
    # Example 4: Testing with files
    print("\\n📋 Example 4: Testing with configuration files")
    
    if Path(server_config_path).exists() and Path(test_config_path).exists():
        try:
            result = tester.test_server(
                server_config=server_config_path,
                test_config=test_config_path,
                server_name="local-sse-server",
                format="json"
            )
            
            print_test_results(result)
            
        except Exception as e:
            print(f"❌ File-based test failed: {e}")
    
    # Cleanup
    cleanup_files = [server_config_path, test_config_path]
    for file_path in cleanup_files:
        if Path(file_path).exists():
            Path(file_path).unlink()
            print(f"🧹 Cleaned up: {file_path}")


def print_test_results(result):
    """Print formatted test results."""
    print(f"\\n📊 Test Results:")
    print(f"   Success: {'✅' if result.success else '❌'} {result.success}")
    print(f"   Passed:  {result.passed_tests}/{result.total_tests}")
    print(f"   Time:    {result.execution_time:.2f}s")
    
    if result.failed_tests:
        print(f"\\n❌ Failed Tests ({len(result.failed_tests)}):")
        for i, failed_test in enumerate(result.failed_tests, 1):
            test_name = failed_test.get('name', f'Test {i}')
            error = failed_test.get('error', 'Unknown error')
            print(f"   {i}. {test_name}: {error}")
    
    if result.error:
        print(f"\\n🔍 Error Details:")
        print(f"   {result.error}")


if __name__ == "__main__":
    main()