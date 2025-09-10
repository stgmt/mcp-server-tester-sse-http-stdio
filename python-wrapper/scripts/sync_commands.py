#!/usr/bin/env python3

"""
🔄 Alternative Python script for NPM ↔ Python command synchronization

Used when Node.js is unavailable or as a fallback.
Parses NPX command output and generates synchronized code.
"""

import subprocess
import json
import re
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class CommandOption:
    """CLI command option."""
    name: str
    alias: Optional[str] = None
    description: str = ""
    required: bool = False
    has_value: bool = True
    default: Optional[str] = None


@dataclass 
class Command:
    """CLI command."""
    name: str
    description: str = ""
    options: List[CommandOption] = field(default_factory=list)
    args: List[str] = field(default_factory=list)


class PythonCommandSyncer:
    """Python command synchronizer (fallback when Node.js is unavailable)."""
    
    def __init__(self, npm_package: str = "mcp-server-tester-sse-http-stdio"):
        self.npm_package = npm_package
        self.commands: List[Command] = []
    
    def check_npm_availability(self) -> bool:
        """Checks NPM package availability."""
        try:
            result = subprocess.run(
                ["npx", self.npm_package, "--help"],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def extract_commands(self) -> List[Command]:
        """Extracts commands from NPM package."""
        print("🔍 Extracting commands from NPM package...")
        
        if not self.check_npm_availability():
            raise Exception(
                f"NPM package {self.npm_package} is unavailable. "
                f"Run: npm install -g {self.npm_package}"
            )
        
        # Get main help
        result = subprocess.run(
            ["npx", self.npm_package, "--help"],
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"Failed to get help: {result.stderr}")
            
        help_text = result.stdout
        print(f"✅ Successfully extracted help from {self.npm_package}")
        
        # Parse commands
        commands = self._parse_help_text(help_text)
        self.commands = commands
        
        return commands
    
    def _parse_help_text(self, help_text: str) -> List[Command]:
        """Parses help text and extracts commands."""
        commands = []
        lines = help_text.split('\n')
        
        in_commands_section = False
        
        for line in lines:
            line = line.strip()
            
            if 'Commands:' in line:
                in_commands_section = True
                continue
                
            if in_commands_section and line and not line.startswith('help'):
                # Parse command line like: "tools [options] [test-file]  Description"
                match = re.match(r'(\w+)(?:\s+\[options\])?(?:\s+\[.*?\])?\s+(.*)', line)
                if match:
                    cmd_name = match.group(1)
                    description = match.group(2).strip()
                    
                    command = Command(
                        name=cmd_name,
                        description=description
                    )
                    commands.append(command)
                    
        return commands
        
    def generate_cli_code(self) -> str:
        """Generates synchronized CLI code."""
        if not self.commands:
            self.extract_commands()
            
        code_parts = []
        
        # Header
        code_parts.append('"""')
        code_parts.append('MCP Server Tester Python CLI - Auto-synchronized with NPM package')
        code_parts.append('"""')
        code_parts.append('')
        code_parts.append('import click')
        code_parts.append('from typing import Optional')
        code_parts.append('from .core import MCPTester')
        code_parts.append('')
        code_parts.append('@click.group()')
        code_parts.append('@click.version_option(version="1.4.1")')
        code_parts.append('def main():')
        code_parts.append('    """MCP Server Tester CLI."""')
        code_parts.append('    pass')
        code_parts.append('')
        
        # Generate commands
        for cmd in self.commands:
            code_parts.extend(self._generate_command_code(cmd))
            
        return '\n'.join(code_parts)
    
    def _generate_command_code(self, cmd: Command) -> List[str]:
        """Generates code for a single command."""
        lines = []
        
        lines.append(f'@main.command()')
        lines.append(f'def {cmd.name}():')
        lines.append(f'    """{cmd.description}"""')
        lines.append(f'    tester = MCPTester()')
        lines.append(f'    # TODO: Implement {cmd.name} functionality')
        lines.append(f'    pass')
        lines.append('')
        
        return lines


if __name__ == "__main__":
    syncer = PythonCommandSyncer()
    try:
        commands = syncer.extract_commands()
        print(f"📋 Found {len(commands)} commands:")
        for cmd in commands:
            print(f"  • {cmd.name}: {cmd.description}")
            
        # Generate synchronized code
        code = syncer.generate_cli_code()
        
        # Save to file
        output_path = Path(__file__).parent.parent / "src" / "mcp_server_tester" / "cli_sync.py"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
            
        print(f"✅ Synchronized CLI code saved to {output_path}")
        
    except Exception as e:
        print(f"❌ Synchronization failed: {e}")
