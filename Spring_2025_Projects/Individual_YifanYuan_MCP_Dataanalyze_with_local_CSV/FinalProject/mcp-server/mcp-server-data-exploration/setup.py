#!/usr/bin/env python3
"""Setup script for MCP server data science environment."""

import subprocess
import sys
from pathlib import Path
import re
import os

def run_command(cmd, check=True):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        return None


def check_dependencies():
    """Check and install required dependencies."""
    required_packages = [
        "mcp",
        "pandas", 
        "numpy", 
        "scipy", 
        "scikit-learn", 
        "statsmodels",
        "matplotlib",
        "plotly"
    ]
    
    print("Checking required packages...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"[OK] {package} is already installed")
        except ImportError:
            print(f"[MISSING] {package} is not installed. Installing automatically...")
        try:
            subprocess.check_call(["uv", "pip", "install", package])

            print(f"[INSTALLED] {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"[FAILED] Failed to install {package}. Please install it manually.")


def install_local_package():
    """Install the package in development mode."""
    print("Installing package in development mode...")
    
    # 创建 pyproject.toml 文件
    pyproject_path = Path("pyproject.toml")
    print("Creating pyproject.toml file...")
    
    pyproject_content = """[build-system]
requires = ["setuptools>=42", "wheel", "mcp"]
build-backend = "setuptools.build_meta"

[project]
name = "mcp_server_ds"
version = "0.1.0"
description = "MCP Server for Data Science Tasks"
requires-python = ">=3.7"
dependencies = ["mcp", "pandas", "numpy"]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
"""
    pyproject_path.write_text(pyproject_content)
    print("Created pyproject.toml file")
    

    cmd = ["uv", "pip", "install", "-e", "."]
    try:
        subprocess.check_call(cmd)
        print("Package installed successfully in development mode")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Failed to install package: {str(e)}")

def create_server_script():
    """Create a script to run the MCP server directly."""
    script_content = """#!/usr/bin/env python3
import mcp_server_ds

if __name__ == "__main__":
    mcp_server_ds.run()
"""
    
    script_path = Path("run_server.py")
    script_path.write_text(script_content)
    
    # Make the script executable on Unix-like systems
    if os.name != 'nt':  # not Windows
        script_path.chmod(script_path.stat().st_mode | 0o111)
    
    print(f"Created server script at {script_path}")
    print(f"  Run the server with: python {script_path}")

def main():
    """Main setup function without Claude Desktop dependency."""
    print("Starting setup...")
    check_dependencies()
    install_local_package()
    create_server_script()
    print("\nSetup completed successfully!")
    print("\nTo use the MCP server with the Streamlit client:")
    print("1. Run the script: python run_server.py")
    print("   (or use the path to server.py in the client config)")
    print("2. Connect to it via the MCP client")

if __name__ == "__main__":
    main()
