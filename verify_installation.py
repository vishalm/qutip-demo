#!/usr/bin/env python3
"""
QuTiP Demo Installation Verification

This script verifies that all dependencies are properly installed
and the demo code will run correctly.

Run this script after installing requirements.txt to ensure everything works.
"""

import sys
import importlib

def check_dependency(module_name, package_name=None):
    """Check if a module can be imported."""
    if package_name is None:
        package_name = module_name
    
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package_name} v{version}")
        return True
    except ImportError:
        print(f"❌ {package_name} - NOT FOUND")
        return False

def check_qutip_functionality():
    """Test basic QuTiP functionality."""
    try:
        import qutip as qt
        import numpy as np
        
        # Test basic operations
        psi = qt.basis(2, 0)
        sx = qt.sigmax()
        exp_val = qt.expect(sx, psi)
        
        # Test Bloch sphere
        b = qt.Bloch()
        
        print("✅ QuTiP basic functionality works")
        return True
        
    except Exception as e:
        print(f"❌ QuTiP functionality test failed: {e}")
        return False

def main():
    """Main verification function."""
    print("🔍 QuTiP Demo Installation Verification")
    print("=" * 50)
    
    # Required dependencies
    dependencies = [
        ('qutip', 'QuTiP'),
        ('numpy', 'NumPy'),
        ('scipy', 'SciPy'),
        ('matplotlib', 'Matplotlib'),
        ('tqdm', 'tqdm'),
    ]
    
    print("📦 Checking Dependencies:")
    all_deps_ok = True
    
    for module, name in dependencies:
        if not check_dependency(module, name):
            all_deps_ok = False
    
    print(f"\n🧪 Testing QuTiP Functionality:")
    qutip_ok = check_qutip_functionality()
    
    print(f"\n📄 Checking Demo Files:")
    demo_files = [
        'bloch_rabi_demo.py',
        'decoherence_demo.py', 
        'cavity_qed_demo.py',
        'interactive_demo.py',
        'run_demos.py'
    ]
    
    files_ok = True
    for filename in demo_files:
        try:
            with open(filename, 'r') as f:
                compile(f.read(), filename, 'exec')
            print(f"✅ {filename}")
        except FileNotFoundError:
            print(f"❌ {filename} - NOT FOUND")
            files_ok = False
        except SyntaxError as e:
            print(f"❌ {filename} - SYNTAX ERROR: {e}")
            files_ok = False
    
    print("\n" + "=" * 50)
    
    if all_deps_ok and qutip_ok and files_ok:
        print("🎉 SUCCESS! Everything is properly installed and ready to use.")
        print("\n🚀 You can now run the demos:")
        print("   python run_demos.py")
        print("\n📚 Or run individual demos:")
        for demo in demo_files[:-1]:  # Exclude run_demos.py
            print(f"   python {demo}")
        return True
    else:
        print("❌ ISSUES DETECTED. Please fix the problems above.")
        if not all_deps_ok:
            print("\n💡 To install missing dependencies:")
            print("   pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
