#!/usr/bin/env node

/**
 * Automatic synchronization of commands and help between NPM and Python versions
 * 
 * This script:
 * 1. Parses NPM package mcp-server-tester-sse-http-stdio
 * 2. Extracts all commands, options and help text
 * 3. Generates synchronized Python CLI code
 * 4. Updates Python wrapper for full compatibility
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

class CommandSynchronizer {
    constructor() {
        this.npmPackageName = 'mcp-server-tester-sse-http-stdio';
        this.commands = new Map();
    }

    /**
     * Extracts command information from NPM package
     */
    async extractNpmCommands() {
        console.log('🔍 Extracting command information from NPM package...');
        
        try {
            // Get main help
            const mainHelp = execSync(`npx ${this.npmPackageName} --help`, { 
                encoding: 'utf8',
                timeout: 10000 
            });
            
            this.parseMainHelp(mainHelp);
            
            // Get help for each command
            for (const [commandName] of this.commands) {
                await this.extractCommandHelp(commandName);
            }
            
            console.log(`✅ Extracted ${this.commands.size} commands`);
            return this.commands;
            
        } catch (error) {
            throw new Error(`Command extraction error: ${error.message}`);
        }
    }

    /**
     * Parses main help to get list of commands
     */
    parseMainHelp(helpText) {
        const lines = helpText.split('\n');
        let inCommandsSection = false;
        
        for (const line of lines) {
            if (line.includes('Commands:')) {
                inCommandsSection = true;
                continue;
            }
            
            if (inCommandsSection) {
                if (line.trim() === '' || line.startsWith('Examples:') || line.startsWith('Learn more:')) {
                    break;
                }
                
                const match = line.match(/^\s*(\w+)(?:\s+\[options\])?\s+(.+)$/);
                if (match) {
                    const [, commandName, description] = match;
                    this.commands.set(commandName, {
                        name: commandName,
                        description: description.trim(),
                        options: [],
                        usage: '',
                        examples: []
                    });
                }
            }
        }
    }

    /**
     * Extracts detailed help for specific command
     */
    async extractCommandHelp(commandName) {
        try {
            const commandHelp = execSync(`npx ${this.npmPackageName} ${commandName} --help`, {
                encoding: 'utf8',
                timeout: 10000
            });
            
            const command = this.commands.get(commandName);
            if (command) {
                this.parseCommandHelp(command, commandHelp);
            }
        } catch (error) {
            console.warn(`⚠️ Could not get help for command ${commandName}: ${error.message}`);
        }
    }

    /**
     * Parses help for specific command
     */
    parseCommandHelp(command, helpText) {
        const lines = helpText.split('\n');
        let currentSection = null;
        
        for (const line of lines) {
            if (line.includes('Usage:')) {
                currentSection = 'usage';
                continue;
            } else if (line.includes('Options:')) {
                currentSection = 'options';
                continue;
            } else if (line.includes('Examples:')) {
                currentSection = 'examples';
                continue;
            }
            
            if (currentSection === 'usage' && line.trim()) {
                command.usage = line.trim();
            } else if (currentSection === 'options') {
                const optionMatch = line.match(/^\s*(-\w|--[\w-]+)(?:\s*<.*?>)?(?:\s*(.+))?$/);
                if (optionMatch) {
                    const [, option, description] = optionMatch;
                    command.options.push({
                        option: option.trim(),
                        description: (description || '').trim(),
                        required: line.includes('(required)'),
                        hasValue: line.includes('<') || line.includes('[')
                    });
                }
            } else if (currentSection === 'examples' && line.trim().startsWith('$')) {
                command.examples.push(line.trim());
            }
        }
    }

    /**
     * Generates Python CLI code
     */
    generatePythonCli(commands) {
        console.log('🐍 Generating Python CLI code...');
        
        let pythonCode = this.generateCliHeader();
        
        // Generate commands
        for (const [, command] of commands) {
            pythonCode += this.generatePythonCommand(command);
        }
        
        pythonCode += this.generateCliFooter();
        
        return pythonCode;
    }

    /**
     * Generates Python CLI file header
     */
    generateCliHeader() {
        return `"""
Command-line interface for MCP Server Tester Python wrapper.
Auto-generated from NPM package commands - DO NOT EDIT MANUALLY!
Use scripts/sync_commands.js to regenerate.
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
def main() -> None:
    """Python wrapper for mcp-server-tester-sse-http-stdio NPM package."""
    pass


`;
    }

    /**
     * Generates Python code for one command
     */
    generatePythonCommand(command) {
        let code = `@main.command()\n`;
        
        // Add options
        for (const option of command.options) {
            code += this.generateClickOption(option);
        }
        
        // Generate function
        const params = command.options
            .map(opt => this.getParameterName(opt.option))
            .join(', ');
        
        code += `def ${command.name}(${params}):\n`;
        code += `    """${command.description}"""\n`;
        code += `    try:\n`;
        code += `        tester = MCPTester()\n`;
        
        // Generate method call
        if (command.name === 'tools') {
            code += this.generateToolsCall(command);
        } else if (command.name === 'evals') {
            code += this.generateEvalsCall(command);
        } else if (command.name === 'compliance') {
            code += this.generateComplianceCall(command);
        } else if (command.name === 'schema') {
            code += this.generateSchemaCall(command);
        } else if (command.name === 'documentation') {
            code += this.generateDocsCall(command);
        }
        
        code += `        
    except MCPTesterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


`;
        
        return code;
    }

    /**
     * Generates Click option
     */
    generateClickOption(option) {
        const paramName = this.getParameterName(option.option);
        let clickOption = `@click.option("${option.option}"`;
        
        if (option.hasValue && !option.option.includes('flag')) {
            if (option.required) {
                clickOption += `, required=True`;
            }
            clickOption += `, help="${option.description}"`;
        } else {
            clickOption += `, is_flag=True, help="${option.description}"`;
        }
        
        clickOption += `)\n`;
        return clickOption;
    }

    /**
     * Gets parameter name from option
     */
    getParameterName(option) {
        return option.replace(/^--?/, '').replace(/-/g, '_');
    }

    /**
     * Генерирует специфичные вызовы для каждой команды
     */
    generateToolsCall(command) {
        return `        # Делегируем NPM пакету с правильным синтаксисом
        result = tester.run_tools_test(
            test_config=test,
            server_config=server_config,
            server_name=server_name,
            verbose=verbose
        )
        click.echo(result.output)
        sys.exit(0 if result.success else 1)`;
    }

    generateEvalsCall(command) {
        return `        result = tester.run_evals(
            test_config=test,
            server_config=server_config,
            server_name=server_name,
            verbose=verbose
        )
        click.echo(result.output)
        sys.exit(0 if result.success else 1)`;
    }

    generateComplianceCall(command) {
        return `        result = tester.run_compliance_check(
            server_config=server_config,
            server_name=server_name,
            categories=categories,
            output=output
        )
        click.echo(result.output)
        sys.exit(0 if result.success else 1)`;
    }

    generateSchemaCall(command) {
        return `        schema_data = tester.get_schema()
        click.echo(json.dumps(schema_data, indent=2))`;
    }

    generateDocsCall(command) {
        return `        documentation = tester.get_documentation()
        click.echo(documentation)`;
    }

    /**
     * Генерирует подвал Python CLI файла
     */
    generateCliFooter() {
        return `
if __name__ == "__main__":
    main()
`;
    }

    /**
     * Генерирует обновленный core.py с правильными методами делегирования
     */
    generateCoreUpdate(commands) {
        console.log('🔧 Генерирую обновленный core.py...');
        
        let coreCode = `    def run_tools_test(self, test_config, server_config, server_name=None, verbose=False):
        """Запускает tools тесты через NPM пакет с правильным синтаксисом."""
        server_config_path = self._prepare_config(server_config, "server_config")
        test_config_path = self._prepare_config(test_config, "test_config")

        cmd = ["npx", self.npm_package_name, "tools", test_config_path]
        cmd.extend(["--server-config", server_config_path])
        
        if server_name:
            cmd.extend(["--server-name", server_name])
        if verbose:
            cmd.append("--verbose")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return self._parse_result(result, "json")
        except Exception as e:
            raise MCPTestExecutionError(f"Tools test failed: {str(e)}")
`;

        return coreCode;
    }

    /**
     * Сохраняет результаты синхронизации
     */
    async saveResults(commands, pythonCliCode, coreUpdate) {
        const resultsDir = '../src/mcp_server_tester';
        
        // Создаем backup
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const backupDir = `../backups/${timestamp}`;
        
        if (fs.existsSync(path.join(resultsDir, 'cli.py'))) {
            fs.mkdirSync(backupDir, { recursive: true });
            fs.copyFileSync(
                path.join(resultsDir, 'cli.py'),
                path.join(backupDir, 'cli.py.backup')
            );
            console.log(`📦 Backup создан: ${backupDir}`);
        }
        
        // Сохраняем новый CLI
        fs.writeFileSync(path.join(resultsDir, 'cli_generated.py'), pythonCliCode);
        console.log('✅ Сохранен cli_generated.py');
        
        // Сохраняем JSON с командами для отладки
        const commandsJson = JSON.stringify([...commands.entries()], null, 2);
        fs.writeFileSync('../commands_extracted.json', commandsJson);
        console.log('✅ Сохранен commands_extracted.json');
        
        // Генерируем отчет
        this.generateReport(commands);
    }

    /**
     * Генерирует отчет о синхронизации
     */
    generateReport(commands) {
        let report = `# 🔄 Отчет о синхронизации NPM ↔ Python

## Синхронизированные команды

`;

        for (const [name, command] of commands) {
            report += `### \`${name}\`
- **Описание:** ${command.description}
- **Опции:** ${command.options.length}
- **Примеры:** ${command.examples.length}

`;
        }

        report += `
## Статистика
- Всего команд: ${commands.size}
- Всего опций: ${[...commands.values()].reduce((sum, cmd) => sum + cmd.options.length, 0)}
- Дата синхронизации: ${new Date().toISOString()}

## Использование
\`\`\`bash
# NPM версия
npx mcp-server-tester-sse-http-stdio tools test.yaml --server-config config.json

# Python версия (синхронизированная)
mcp-server-tester tools test.yaml --server-config config.json
\`\`\`
`;

        fs.writeFileSync('../sync_report.md', report);
        console.log('✅ Сохранен sync_report.md');
    }

    /**
     * Главный метод синхронизации
     */
    async sync() {
        console.log('🚀 Starting NPM ↔ Python command synchronization...\n');
        
        try {
            // 1. Извлекаем команды из NPM
            const commands = await this.extractNpmCommands();
            
            // 2. Генерируем Python код
            const pythonCliCode = this.generatePythonCli(commands);
            const coreUpdate = this.generateCoreUpdate(commands);
            
            // 3. Сохраняем результаты
            await this.saveResults(commands, pythonCliCode, coreUpdate);
            
            console.log('\n✅ Синхронизация завершена успешно!');
            console.log('📁 Результаты сохранены в ../src/mcp_server_tester/');
            console.log('📊 Отчет: ../sync_report.md');
            
        } catch (error) {
            console.error('❌ Ошибка синхронизации:', error.message);
            process.exit(1);
        }
    }
}

// Запускаем синхронизацию
const synchronizer = new CommandSynchronizer();
synchronizer.sync().catch(console.error);