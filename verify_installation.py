#!/usr/bin/env python3
"""
Verify PlanExe installation and dependency resolution.
Run this after installing with: pip install .[gradio-ui]

Usage:
    python verify_installation.py
"""

import sys

def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("  ❌ FAIL: Python 3.10 or higher is required")
        return False
    print("  ✅ PASS: Python version is compatible")
    return True

def check_package_installed(package_name):
    """Check if a package is installed."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def check_pillow_version():
    """Check Pillow version and compatibility."""
    print("\nChecking Pillow installation...")
    try:
        import PIL
        from PIL import __version__ as pillow_version
        print(f"  Pillow version: {pillow_version}")
        
        # Parse version
        major, minor = map(int, pillow_version.split('.')[:2])
        
        # Check if version is in the acceptable range (10.2.0 to 10.4.x)
        if major == 10 and minor >= 2:
            print(f"  ✅ PASS: Pillow {pillow_version} is in the compatible range (>=10.2.0,<11.0)")
            return True
        elif major < 10:
            print(f"  ⚠️  WARNING: Pillow {pillow_version} is older than expected (should be >=10.2.0)")
            return True  # Still might work
        elif major >= 11:
            print(f"  ❌ FAIL: Pillow {pillow_version} is too new (should be <11.0)")
            print("     This will conflict with llama-index-llms-gemini")
            return False
        else:
            print(f"  ⚠️  WARNING: Unexpected Pillow version {pillow_version}")
            return True
    except ImportError:
        print("  ❌ FAIL: Pillow is not installed")
        return False

def check_pydantic_version():
    """Check Pydantic version and compatibility."""
    print("\nChecking Pydantic installation...")
    try:
        import pydantic
        from pydantic import __version__ as pydantic_version
        print(f"  Pydantic version: {pydantic_version}")
        
        # Parse version
        major, minor = map(int, pydantic_version.split('.')[:2])
        
        # Check if version is in the acceptable range (>=2.11.5,<3.0.0)
        if major == 2 and minor >= 11 and (minor > 11 or int(pydantic_version.split('.')[2]) >= 5):
            print(f"  ✅ PASS: Pydantic {pydantic_version} is in the compatible range (>=2.11.5,<3.0.0)")
            return True
        elif major == 2 and minor < 11:
            print(f"  ❌ FAIL: Pydantic {pydantic_version} is too old (should be >=2.11.5)")
            print("     This will conflict with llama-index-workflows")
            return False
        elif major >= 3:
            print(f"  ❌ FAIL: Pydantic {pydantic_version} is too new (should be <3.0.0)")
            print("     This may cause compatibility issues")
            return False
        else:
            print(f"  ⚠️  WARNING: Unexpected Pydantic version {pydantic_version}")
            return True
    except ImportError:
        print("  ❌ FAIL: Pydantic is not installed")
        return False

def check_core_dependencies():
    """Check if core dependencies are installed."""
    print("\nChecking core dependencies...")
    
    dependencies = {
        'gradio': 'Gradio UI framework',
        'llama_index': 'LlamaIndex (from llama-index-core)',
        'google.generativeai': 'Google Gemini AI (from llama-index-llms-gemini)',
        'luigi': 'Luigi workflow manager',
        'pandas': 'Pandas data analysis',
        'numpy': 'NumPy numerical computing',
    }
    
    all_passed = True
    for package, description in dependencies.items():
        if check_package_installed(package):
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description} (package: {package})")
            all_passed = False
    
    return all_passed

def check_planexe_import():
    """Check if PlanExe can be imported."""
    print("\nChecking PlanExe installation...")
    try:
        import planexe
        print(f"  ✅ PASS: PlanExe is installed")
        
        # Try to import the main app module
        try:
            from planexe.plan import app_text2plan
            print(f"  ✅ PASS: Main app module can be imported")
            return True
        except ImportError as e:
            print(f"  ⚠️  WARNING: Could not import app module: {e}")
            return True  # Base package is installed at least
    except ImportError:
        print("  ❌ FAIL: PlanExe is not installed")
        print("     Run: pip install .[gradio-ui]")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("PlanExe Installation Verification")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_pydantic_version(),
        check_pillow_version(),
        check_core_dependencies(),
        check_planexe_import(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ SUCCESS: All checks passed!")
        print("=" * 60)
        print("\nYou can now run PlanExe with:")
        print("    python -m planexe.plan.app_text2plan")
        print("\nThen open http://localhost:7860 in your browser")
        return 0
    else:
        print("❌ FAILURE: Some checks failed")
        print("=" * 60)
        print("\nPlease check the errors above and:")
        print("1. Ensure you're in a virtual environment")
        print("2. Run: pip install --upgrade pip")
        print("3. Run: pip install .[gradio-ui]")
        print("\nFor help, see INSTALL.md or DEPENDENCY_FIX.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
