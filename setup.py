#!/usr/bin/env python3
"""
Setup script for Code Tokenizer Flask Application
Run this script to set up the application locally
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"➤ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is 3.11 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"✗ Python 3.11+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor} detected")
    return True

def check_git():
    """Check if Git is installed"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        print("✓ Git is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ Git not found. GitHub repository cloning will not work.")
        return False

def create_directories():
    """Create necessary directories"""
    dirs = ['uploads', 'temp', 'static/css', 'static/js', 'templates']
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    print("✓ Created necessary directories")

def install_dependencies():
    """Install Python dependencies"""
    # Core dependencies (no database required)
    dependencies = [
        "Flask==3.0.0",
        "Werkzeug==3.0.1",
        "GitPython==3.1.40",
        "requests==2.31.0"
    ]
    
    # Install core dependencies
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"Installing {dep.split('==')[0]}"):
            return False
    
    return True

def setup_environment():
    """Create .env file with basic configuration"""
    env_content = """# Code Tokenizer Environment Configuration
SESSION_SECRET=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///tokenizer.db
FLASK_ENV=development
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✓ Created .env file with default configuration")
    else:
        print("✓ .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up Code Tokenizer Flask Application")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    check_git()  # Not critical, just warn
    
    # Setup steps
    create_directories()
    
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        print("✗ Dependency installation failed")
        sys.exit(1)
    
    setup_environment()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\nTo run the application:")
    print("1. Activate your virtual environment (if using one)")
    print("2. Run: python main.py")
    print("3. Open http://localhost:5000 in your browser")
    print("\n📖 See README.md for detailed instructions")

if __name__ == "__main__":
    main()