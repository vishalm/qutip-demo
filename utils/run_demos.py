#!/usr/bin/env python3
"""
QuTiP Demo Runner

This script provides an easy way to run all the QuTiP demonstrations.
Choose which demo to run from a simple menu.

Author: QuTiP Demo Project  
License: MIT
"""

import sys
import os

def print_banner():
    """Print welcome banner."""
    print("🌟" * 30)
    print("    QuTiP Demo Project")
    print("  Quantum Toolbox in Python")
    print("🌟" * 30)
    print()
    print("Welcome to the QuTiP demonstration project!")
    print("This showcases the powerful capabilities of QuTiP")
    print("for quantum physics simulation and visualization.")
    print()

def print_menu():
    """Print the demo selection menu."""
    print("📋 Available Demonstrations:")
    print()
    print("1. 🎯 Bloch Sphere & Rabi Oscillations")
    print("   - Interactive Bloch sphere visualization")
    print("   - Quantum gate demonstrations")
    print("   - Animated state evolution")
    print()
    print("2. 🌀 Quantum Decoherence Effects")
    print("   - T1 energy relaxation")
    print("   - T2 dephasing processes")
    print("   - Open vs closed system comparison")
    print()
    print("3. 🔬 Cavity QED & Quantum Optics")
    print("   - Jaynes-Cummings model")
    print("   - Vacuum Rabi oscillations")
    print("   - Photon statistics analysis")
    print()
    print("4. 🎮 Interactive Demo (Real-time Controls)")
    print("   - Parameter sliders and controls")
    print("   - Multiple demonstrations in one interface")
    print("   - Real-time visualization updates")
    print()
    print("5. 📊 Run All Demos (Sequential)")
    print("   - Execute all demonstrations one by one")
    print("   - Complete showcase of QuTiP capabilities")
    print()
    print("0. ❌ Exit")
    print()

def run_demo(choice):
    """Run the selected demonstration."""
    try:
        if choice == '1':
            print("🎯 Starting Bloch Sphere & Rabi Oscillations Demo...")
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'demos'))
            import bloch_rabi_demo
            bloch_rabi_demo.main()
            
        elif choice == '2':
            print("🌀 Starting Quantum Decoherence Demo...")
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'demos'))
            import decoherence_demo
            decoherence_demo.main()
            
        elif choice == '3':
            print("🔬 Starting Cavity QED Demo...")
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'demos'))
            import cavity_qed_demo
            cavity_qed_demo.main()
            
        elif choice == '4':
            print("🎮 Starting Interactive Demo...")
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'demos'))
            import interactive_demo
            interactive_demo.main()
            
        elif choice == '5':
            print("📊 Running All Demos...")
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'demos'))
            
            print("\n" + "="*60)
            print("Demo 1/3: Bloch Sphere & Rabi Oscillations")
            print("="*60)
            import bloch_rabi_demo
            bloch_rabi_demo.main()
            
            print("\n" + "="*60)
            print("Demo 2/3: Quantum Decoherence")
            print("="*60)
            import decoherence_demo
            decoherence_demo.main()
            
            print("\n" + "="*60)
            print("Demo 3/3: Cavity QED")
            print("="*60)
            import cavity_qed_demo
            cavity_qed_demo.main()
            
            print("\n🎉 All demos completed!")
            
        else:
            print("❌ Invalid choice. Please select 1-5 or 0 to exit.")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ Error importing demo module: {e}")
        print("Make sure all demo files are in the current directory.")
        return False
        
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        print("Please check that all dependencies are installed correctly.")
        return False

def check_dependencies():
    """Check if required dependencies are available."""
    missing_deps = []
    
    try:
        import qutip
        print(f"✅ QuTiP version {qutip.__version__} found")
    except ImportError:
        missing_deps.append("qutip")
    
    try:
        import numpy
        print(f"✅ NumPy version {numpy.__version__} found")
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        import matplotlib
        print(f"✅ Matplotlib version {matplotlib.__version__} found")
    except ImportError:
        missing_deps.append("matplotlib")
    
    try:
        import scipy
        print(f"✅ SciPy version {scipy.__version__} found")
    except ImportError:
        missing_deps.append("scipy")
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies found!")
    return True

def main():
    """Main demo runner function."""
    print_banner()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        sys.exit(1)
    
    print("\n🚀 Ready to run demonstrations!")
    
    while True:
        print("\n" + "-"*50)
        print_menu()
        
        try:
            choice = input("👉 Enter your choice (0-5): ").strip()
            
            if choice == '0':
                print("\n👋 Thank you for exploring QuTiP!")
                print("🌟 Learn more at: https://qutip.org/")
                break
            
            if run_demo(choice):
                input("\n⏸️  Press Enter to continue to menu...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
