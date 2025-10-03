"""
Claude Development Framework CLI Tool

A command-line interface for the Claude Development Framework that simplifies
project initialization, specification generation, testing, planning, and quality checks.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="claude-dev",
    version="1.0.0",
    author="Claude Development Framework Team",
    author_email="noreply@example.com",
    description="CLI tool for Claude Development Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/claude-development-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
        "jinja2>=3.0",
        "rich>=13.0",
        "pytest>=7.0",
        "coverage>=7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "pylint>=2.17",
            "mypy>=1.0",
        ],
        "agents": [
            "anthropic>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "claude-dev=claude_dev.cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "claude_dev": [
            "templates/*.j2",
        ],
    },
)
