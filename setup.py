#!/usr/bin/env python3
"""
Setup script for AI Restaurant app
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def setup_virtual_environment():
    """Create and activate virtual environment"""
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    
    # Check if we're already in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment already activated")
        return True
    
    print("ℹ️  Please activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    return True

def install_dependencies():
    """Install required packages"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def setup_environment_file():
    """Create .env file from template"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            run_command("cp .env.example .env", "Creating environment file")
            print("⚠️  Please edit .env file and add your OpenAI API key")
        else:
            # Create basic .env file
            with open(".env", "w") as f:
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
                f.write("FLASK_ENV=development\n")
                f.write("FLASK_DEBUG=True\n")
            print("✅ Created .env file - please add your OpenAI API key")
    else:
        print("✅ .env file already exists")

def verify_structure():
    """Verify all necessary files and directories exist"""
    required_files = [
        "app.py",
        "requirements.txt",
        "templates/index.html",
        "static/css/style.css",
        "static/js/app.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files present")
    return True

def main():
    """Main setup function"""
    print("🤖 AI Restaurant Setup Script")
    print("=" * 50)
    
    # Check prerequisites
    check_python_version()
    
    if not verify_structure():
        print("❌ Setup failed - missing files")
        sys.exit(1)
    
    # Setup virtual environment
    setup_virtual_environment()
    
    # Install dependencies (only if in virtual environment or user confirms)
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        install_dependencies()
    else:
        response = input("Install dependencies globally? (not recommended) [y/N]: ")
        if response.lower() == 'y':
            install_dependencies()
        else:
            print("ℹ️  Please activate virtual environment and run: pip install -r requirements.txt")
    
    # Setup environment file
    setup_environment_file()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: python app.py")
    print("3. Open: http://localhost:5000")
    print("\n💡 For troubleshooting, check the README.md file")

if __name__ == "__main__":
    main()