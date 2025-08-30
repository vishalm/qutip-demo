#!/usr/bin/env python3
"""
Screenshot Generation Helper for QuTiP Demo

This script helps generate screenshots for the README documentation.
It runs each demo and pauses at key moments for screenshot capture.

Usage: python generate_screenshots.py [demo_name]
"""

import sys
import time
import subprocess

def print_instructions(demo_name, description, key_moments):
    """Print screenshot instructions for a demo."""
    print(f"\n🎬 {demo_name} Screenshot Guide")
    print("=" * 50)
    print(f"Description: {description}")
    print("\n📸 Key moments to capture:")
    for i, moment in enumerate(key_moments, 1):
        print(f"  {i}. {moment}")
    print("\n⏸️  The demo will pause after launching. Take screenshots then press Enter to continue.")
    print("💾 Save screenshots in: resources/screenshots/")
    print("-" * 50)

def run_demo_with_pause(script_name):
    """Run a demo script and pause for screenshots."""
    try:
        print(f"\n🚀 Launching {script_name}...")
        print("⏳ Starting demo in 3 seconds...")
        time.sleep(3)
        
        # Start the demo
        process = subprocess.Popen([sys.executable, script_name])
        
        print("\n📸 Demo is running! Take your screenshots now.")
        input("Press Enter when you've captured all needed screenshots...")
        
        # Terminate the demo
        process.terminate()
        process.wait()
        print("✅ Demo closed.")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user.")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ Error running demo: {e}")

def main():
    """Main screenshot generation function."""
    demos = {
        'bloch': {
            'script': 'demos/bloch_rabi_demo.py',
            'description': 'Bloch sphere visualization and Rabi oscillations',
            'moments': [
                'Bloch sphere with trajectory (save as: bloch_sphere_rabi.png)',
                'Quantum gates grid plot (save as: quantum_gates_bloch.png)',
                'Animated evolution frames (optional additional shots)'
            ]
        },
        'decoherence': {
            'script': 'demos/decoherence_demo.py', 
            'description': 'Quantum decoherence and open system dynamics',
            'moments': [
                'Main decoherence comparison plots (save as: decoherence_comparison.png)',
                'Coherence loss over time (save as: coherence_loss.png)',
                'Different environmental effects (optional additional shots)'
            ]
        },
        'cavity': {
            'script': 'demos/cavity_qed_demo.py',
            'description': 'Cavity QED and quantum optics demonstrations', 
            'moments': [
                'Vacuum Rabi oscillations (save as: cavity_qed_rabi.png)',
                'Photon statistics distributions (save as: photon_statistics.png)',
                'Strong coupling regime comparisons (optional additional shots)'
            ]
        },
        'interactive': {
            'script': 'demos/interactive_demo.py',
            'description': 'Interactive demo with real-time controls',
            'moments': [
                'Full interface with sliders and plots (save as: interactive_demo.png)',
                'Different demo modes if possible (optional additional shots)'
            ]
        },
        'launcher': {
            'script': 'utils/run_demos.py',
            'description': 'Demo launcher menu',
            'moments': [
                'Terminal with main menu displayed (save as: demo_launcher.png)'
            ]
        }
    }
    
    if len(sys.argv) > 1:
        demo_choice = sys.argv[1].lower()
        if demo_choice in demos:
            demo = demos[demo_choice]
            print_instructions(demo_choice.capitalize(), demo['description'], demo['moments'])
            run_demo_with_pause(demo['script'])
        else:
            print(f"❌ Unknown demo: {demo_choice}")
            print(f"Available demos: {', '.join(demos.keys())}")
    else:
        print("📸 QuTiP Demo Screenshot Generator")
        print("=" * 40)
        print("This tool helps you generate screenshots for the README.")
        print("\nAvailable demos:")
        for name, demo in demos.items():
            print(f"  • {name}: {demo['description']}")
        print(f"\nUsage: python {sys.argv[0]} [demo_name]")
        print("Example: python generate_screenshots.py bloch")
        print("\nOr run all demos manually and take screenshots as needed.")

if __name__ == "__main__":
    main()
