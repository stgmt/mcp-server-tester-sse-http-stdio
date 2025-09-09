#!/usr/bin/env python3

"""
Setup script for mcp-server-tester Python wrapper.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mcp-server-tester",
    version="1.0.0",
    author="MCP Server Tester Team",
    author_email="noreply@anthropic.com",
    description="Python wrapper for mcp-server-tester-sse-http-stdio NPM package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stgmt/mcp-server-tester-sse-http-stdio",
    project_urls={
        "Bug Tracker": "https://github.com/stgmt/mcp-server-tester-sse-http-stdio/issues",
        "NPM Package": "https://www.npmjs.com/package/mcp-server-tester-sse-http-stdio",
        "Docker Hub": "https://hub.docker.com/r/stgmt/mcp-server-tester"
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp-server-tester=mcp_server_tester.cli:main",
            "mcp-tester=mcp_server_tester.cli:main",
        ],
    },
    include_package_data=True,
    keywords="mcp, server, testing, model-context-protocol, llm, ai",
)