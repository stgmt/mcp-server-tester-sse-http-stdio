#!/usr/bin/env python3

"""
🔄 Альтернативный Python скрипт синхронизации команд NPM ↔ Python

Используется когда Node.js недоступен или как fallback.
Парсит выходные данные NPX команд и генерирует синхронизированный код.
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
    """Опция команды CLI."""
    option: str
    description: str
    required: bool = False
    has_value: bool = True
    default: Optional[str] = None


@dataclass 
class Command:
    """CLI команда."""
    name: str
    description: str
    options: List[CommandOption] = field(default_factory=list)
    usage: str = ""
    examples: List[str] = field(default_factory=list)


class PythonCommandSynchronizer:
    """Синхронизатор команд на Python (fallback когда Node.js недоступен)."""
    
    def __init__(self):
        self.npm_package = "mcp-server-tester-sse-http-stdio" 
        self.commands: Dict[str, Command] = {}
    
    def check_npm_package(self) -> bool:
        """Проверяет доступность NPM пакета."""
        try:
            result = subprocess.run(
                ["npx", self.npm_package, "--help"],
                capture_output=True,
                text=True,
                timeout=15
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def extract_commands(self) -> Dict[str, Command]:
        """Извлекает команды из NPM пакета."""
        print("🔍 Извлекаю команды из NPM пакета...")
        
        if not self.check_npm_package():
            raise RuntimeError(
                f"NPM пакет {self.npm_package} недоступен. "
                "Установите: npm install -g mcp-server-tester-sse-http-stdio"
            )
        
        # Получаем основной help
        main_help = self._get_help("")
        self._parse_main_help(main_help)
        
        # Получаем help для каждой команды
        for cmd_name in list(self.commands.keys()):
            cmd_help = self._get_help(cmd_name)
            if cmd_help:
                self._parse_command_help(cmd_name, cmd_help)
        
        print(f"✅ Извлечено {len(self.commands)} команд")
        return self.commands
    
    def _get_help(self, command: str) -> str:
        """Получает help текст для команды."""
        cmd = ["npx", self.npm_package]
        if command:
            cmd.append(command)
        cmd.append("--help")
        
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10
            )
            return result.stdout if result.returncode == 0 else ""
        except subprocess.TimeoutExpired:
            print(f"⚠️ Timeout при получении help для {command or 'main'}")
            return ""
    
    def _parse_main_help(self, help_text: str) -> None:
        """Парсит основной help для поиска команд."""
        lines = help_text.split('\n')
        in_commands = False
        
        for line in lines:
            if 'Commands:' in line:
                in_commands = True
                continue
            elif in_commands and line.strip() and not line.startswith(' '):
                break
            elif in_commands and line.strip():
                # Парсим строку команды: "  tools [options]  Run MCP server tools tests"
                match = re.match(r'\s+(\w+)(?:\s+\[.*?\])?\s+(.+)$', line)
                if match:
                    cmd_name, description = match.groups()
                    self.commands[cmd_name] = Command(
                        name=cmd_name,
                        description=description.strip()
                    )
    
    def _parse_command_help(self, cmd_name: str, help_text: str) -> None:
        """Парсит help конкретной команды."""
        if cmd_name not in self.commands:
            return
        
        command = self.commands[cmd_name]
        lines = help_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.rstrip()
            
            if 'Usage:' in line:
                current_section = 'usage'
            elif 'Options:' in line:
                current_section = 'options'
            elif 'Examples:' in line:
                current_section = 'examples'
            elif current_section == 'usage' and line.strip():
                command.usage = line.strip()
                current_section = None
            elif current_section == 'options' and line.strip():
                option = self._parse_option_line(line)
                if option:
                    command.options.append(option)
            elif current_section == 'examples' and line.strip().startswith('$'):
                command.examples.append(line.strip())
    
    def _parse_option_line(self, line: str) -> Optional[CommandOption]:
        """Парсит строку опции."""
        # Примеры строк:
        # "  --server-config <file>   MCP server configuration (required)"
        # "  -v, --verbose            Enable verbose output" 
        # "  --timeout <ms>          Test timeout (default: 10000)"
        
        option_match = re.match(
            r'\s*(-\w|--[\w-]+)(?:,?\s*(--?[\w-]+))?\s*(?:<[^>]+>)?\s*(.*)$',
            line
        )
        
        if not option_match:
            return None
        
        short_opt, long_opt, description = option_match.groups()
        option_name = long_opt or short_opt
        
        if not option_name:
            return None
        
        # Определяем свойства опции
        has_value = '<' in line or '>' in line
        required = 'required' in description.lower()
        
        # Извлекаем default значение
        default_match = re.search(r'default:\s*([^)]+)', description, re.I)
        default_val = default_match.group(1).strip() if default_match else None
        
        return CommandOption(
            option=option_name,
            description=description.strip(),
            required=required,
            has_value=has_value,
            default=default_val
        )
    
    def generate_python_cli(self) -> str:
        """Генерирует Python CLI код."""
        print("🐍 Генерирую Python CLI код...")
        
        code_parts = [
            self._generate_header(),
            self._generate_main_group(),
        ]
        
        # Генерируем команды
        for command in self.commands.values():
            code_parts.append(self._generate_command(command))
        
        code_parts.append(self._generate_footer())
        
        return '\n'.join(code_parts)
    
    def _generate_header(self) -> str:
        """Генерирует заголовок файла."""
        return '''"""
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


'''
    
    def _generate_main_group(self) -> str:
        """Генерирует главную группу команд."""
        return '''@click.group()
@click.version_option(version="1.0.0")
def main() -> None:
    """Python wrapper for mcp-server-tester-sse-http-stdio NPM package."""
    pass


'''
    
    def _generate_command(self, command: Command) -> str:
        """Генерирует код команды."""
        lines = [f'@main.command()']
        
        # Генерируем опции Click
        for option in command.options:
            lines.append(self._generate_click_option(option))
        
        # Генерируем функцию
        params = [self._option_to_param(opt.option) for opt in command.options]
        func_signature = f"def {command.name}({', '.join(params)}):"
        
        lines.extend([
            func_signature,
            f'    """{command.description}"""',
            '    try:',
            '        # Делегируем NPM пакету напрямую',
            f'        cmd = ["npx", "mcp-server-tester-sse-http-stdio", "{command.name}"]',
        ])
        
        # Добавляем параметры к команде
        for option in command.options:
            param_name = self._option_to_param(option.option)
            if option.has_value:
                lines.append(f'        if {param_name}:')
                lines.append(f'            cmd.extend(["{option.option}", str({param_name})])')
            else:
                lines.append(f'        if {param_name}:')
                lines.append(f'            cmd.append("{option.option}")')
        
        lines.extend([
            '',
            '        # Выполняем команду',
            '        result = subprocess.run(',
            '            cmd, capture_output=True, text=True, timeout=30',
            '        )',
            '',
            '        # Выводим результат',
            '        if result.stdout:',
            '            click.echo(result.stdout)',
            '        if result.stderr:',
            '            click.echo(result.stderr, err=True)',
            '',
            '        sys.exit(result.returncode)',
            '',
            '    except subprocess.TimeoutExpired:',
            f'        click.echo("Timeout executing {command.name} command", err=True)',
            '        sys.exit(1)',
            '    except Exception as e:',
            '        click.echo(f"Error: {{e}}", err=True)',
            '        sys.exit(1)',
            '',
            ''
        ])
        
        return '\n'.join(lines)
    
    def _generate_click_option(self, option: CommandOption) -> str:
        """Генерирует Click опцию."""
        parts = [f'@click.option("{option.option}"']
        
        if option.required:
            parts.append('required=True')
        
        if option.default:
            parts.append(f'default={repr(option.default)}')
        
        if not option.has_value:
            parts.append('is_flag=True')
        
        if option.description:
            # Экранируем кавычки в описании
            desc = option.description.replace('"', '\\"')
            parts.append(f'help="{desc}"')
        
        return f"{parts[0]}, {', '.join(parts[1:])})"
    
    def _option_to_param(self, option_name: str) -> str:
        """Преобразует имя опции в имя параметра Python."""
        return option_name.lstrip('-').replace('-', '_')
    
    def _generate_footer(self) -> str:
        """Генерирует футер файла."""
        return '''
if __name__ == "__main__":
    main()
'''
    
    def save_results(self, cli_code: str) -> None:
        """Сохраняет результаты генерации."""
        print("💾 Сохраняю результаты...")
        
        # Создаем директории
        src_dir = Path("../src/mcp_server_tester")
        src_dir.mkdir(parents=True, exist_ok=True)
        
        backup_dir = Path("../backups")
        backup_dir.mkdir(exist_ok=True)
        
        # Backup существующего файла
        cli_path = src_dir / "cli.py"
        if cli_path.exists():
            import shutil
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"cli_{timestamp}.py.backup"
            shutil.copy2(cli_path, backup_path)
            print(f"📦 Backup: {backup_path}")
        
        # Сохраняем новый CLI
        generated_path = src_dir / "cli_generated.py"
        with open(generated_path, 'w', encoding='utf-8') as f:
            f.write(cli_code)
        
        print(f"✅ Сохранено: {generated_path}")
        
        # Сохраняем команды в JSON для отладки
        commands_json = {
            name: {
                "description": cmd.description,
                "options": [
                    {
                        "option": opt.option,
                        "description": opt.description,
                        "required": opt.required,
                        "has_value": opt.has_value,
                        "default": opt.default
                    }
                    for opt in cmd.options
                ],
                "usage": cmd.usage,
                "examples": cmd.examples
            }
            for name, cmd in self.commands.items()
        }
        
        with open("../commands_extracted.json", 'w', encoding='utf-8') as f:
            json.dump(commands_json, f, indent=2, ensure_ascii=False)
        
        print("✅ Сохранено: ../commands_extracted.json")
    
    def generate_report(self) -> str:
        """Генерирует отчет о синхронизации."""
        total_options = sum(len(cmd.options) for cmd in self.commands.values())
        
        report = f"""# 🔄 Отчет о синхронизации NPM ↔ Python (Python версия)

## Статистика
- **Всего команд:** {len(self.commands)}
- **Всего опций:** {total_options}
- **Дата синхронизации:** {__import__('datetime').datetime.now().isoformat()}

## Синхронизированные команды

"""
        
        for name, command in self.commands.items():
            report += f"### `{name}`\n"
            report += f"- **Описание:** {command.description}\n"
            report += f"- **Опций:** {len(command.options)}\n"
            
            if command.options:
                report += "- **Опции:**\n"
                for opt in command.options:
                    required_mark = " (обязательная)" if opt.required else ""
                    report += f"  - `{opt.option}`: {opt.description}{required_mark}\n"
            
            report += "\n"
        
        report += """
## Использование

```bash
# NPM версия
npx mcp-server-tester-sse-http-stdio tools test.yaml --server-config config.json

# Python версия (синхронизированная)  
mcp-server-tester tools test.yaml --server-config config.json
```

## Примечания
- Генерировано Python скриптом (fallback)
- Команды делегируются NPX напрямую 
- Полная совместимость с NPM версией
"""
        
        return report
    
    def sync(self) -> None:
        """Главный метод синхронизации."""
        print("🚀 Начинаю синхронизацию команд (Python версия)...")
        print()
        
        try:
            # Извлекаем команды
            commands = self.extract_commands()
            
            # Генерируем код
            cli_code = self.generate_python_cli()
            
            # Сохраняем результаты
            self.save_results(cli_code)
            
            # Генерируем отчет
            report = self.generate_report()
            with open("../sync_report.md", 'w', encoding='utf-8') as f:
                f.write(report)
            
            print()
            print("✅ Синхронизация завершена успешно!")
            print("📁 Результаты:")
            print("  - ../src/mcp_server_tester/cli_generated.py")
            print("  - ../commands_extracted.json") 
            print("  - ../sync_report.md")
            
        except Exception as e:
            print(f"❌ Ошибка синхронизации: {e}")
            raise


if __name__ == "__main__":
    synchronizer = PythonCommandSynchronizer()
    synchronizer.sync()