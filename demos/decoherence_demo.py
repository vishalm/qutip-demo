#!/usr/bin/env python3
"""
QuTiP Demo: Quantum Decoherence and Open System Dynamics

This script demonstrates:
1. Quantum decoherence effects (T1 and T2 processes)
2. Lindblad master equation simulation
3. Comparison between closed and open quantum systems
4. Environmental effects on quantum coherence

Author: QuTiP Demo Project
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
from tqdm import tqdm
import warnings

# Suppress numerical warnings for cleaner output
np.seterr(divide='ignore', invalid='ignore', over='ignore')
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Set up matplotlib for better plots
try:
    plt.style.use('seaborn-v0_8')
except OSError:
    try:
        plt.style.use('seaborn')
    except OSError:
        plt.style.use('default')
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 12

def create_superposition_state(theta=np.pi/4, phi=0):
    """
    Create a superposition state on the Bloch sphere.
    
    Parameters:
    theta: polar angle (0 = |0⟩, π = |1⟩)
    phi: azimuthal angle
    """
    return np.cos(theta/2) * qt.basis(2, 0) + np.exp(1j*phi) * np.sin(theta/2) * qt.basis(2, 1)

def simulate_t1_relaxation():
    """Simulate T1 (energy relaxation) process."""
    print("⚡ Simulating T1 Energy Relaxation...")
    
    # Parameters
    omega_0 = 1.0  # qubit frequency
    gamma = 0.1    # relaxation rate (1/T1)
    
    # Time evolution
    t_max = 30
    t_points = np.linspace(0, t_max, 200)
    
    # Initial state: excited state |1⟩
    psi0 = qt.basis(2, 1)
    
    # Hamiltonian (free evolution)
    H = omega_0/2 * qt.sigmaz()
    
    # Collapse operators for T1 relaxation
    c_ops = [np.sqrt(gamma) * qt.sigmam()]  # |1⟩ → |0⟩ transition
    
    # Solve master equation
    print("Solving master equation for T1 relaxation...")
    result = qt.mesolve(H, psi0, t_points, c_ops, [])
    
    # Calculate populations and coherences
    P_ground = []
    P_excited = []
    coherence = []
    
    for state in tqdm(result.states, desc="Calculating observables"):
        # Populations
        P_ground.append(qt.expect(qt.projection(2, 0, 0), state))
        P_excited.append(qt.expect(qt.projection(2, 1, 1), state))
        
        # Coherence (off-diagonal elements)
        rho = state
        if rho.type == 'ket':
            rho = qt.ket2dm(rho)
        coherence.append(abs(rho[0, 1]))
    
    return t_points, P_ground, P_excited, coherence, result

def simulate_t2_dephasing():
    """Simulate T2 (dephasing) process."""
    print("🌀 Simulating T2 Dephasing...")
    
    # Parameters
    omega_0 = 1.0  # qubit frequency
    gamma_phi = 0.2  # pure dephasing rate
    
    # Time evolution
    t_max = 20
    t_points = np.linspace(0, t_max, 200)
    
    # Initial state: superposition |+⟩ = (|0⟩ + |1⟩)/√2
    psi0 = create_superposition_state(np.pi/2, 0)
    
    # Hamiltonian
    H = omega_0/2 * qt.sigmaz()
    
    # Collapse operators for pure dephasing
    c_ops = [np.sqrt(gamma_phi) * qt.sigmaz()]
    
    # Solve master equation
    print("Solving master equation for T2 dephasing...")
    result = qt.mesolve(H, psi0, t_points, c_ops, [])
    
    # Calculate observables
    P_ground = []
    P_excited = []
    coherence = []
    bloch_x = []
    bloch_y = []
    bloch_z = []
    
    for state in tqdm(result.states, desc="Calculating observables"):
        # Populations
        P_ground.append(qt.expect(qt.projection(2, 0, 0), state))
        P_excited.append(qt.expect(qt.projection(2, 1, 1), state))
        
        # Bloch vector components
        bloch_x.append(qt.expect(qt.sigmax(), state))
        bloch_y.append(qt.expect(qt.sigmay(), state))
        bloch_z.append(qt.expect(qt.sigmaz(), state))
        
        # Coherence
        rho = state
        if rho.type == 'ket':
            rho = qt.ket2dm(rho)
        coherence.append(abs(rho[0, 1]))
    
    return t_points, P_ground, P_excited, coherence, bloch_x, bloch_y, bloch_z, result

def simulate_t1_and_t2():
    """Simulate combined T1 and T2 effects."""
    print("🔄 Simulating Combined T1 and T2 Effects...")
    
    # Parameters
    omega_0 = 1.0
    gamma = 0.05    # T1 rate
    gamma_phi = 0.1  # pure dephasing rate
    
    # Total T2 rate: 1/T2 = 1/(2*T1) + 1/T2_phi
    # where T2_phi is pure dephasing time
    
    # Time evolution
    t_max = 40
    t_points = np.linspace(0, t_max, 300)
    
    # Initial state: superposition
    psi0 = create_superposition_state(np.pi/3, np.pi/4)
    
    # Hamiltonian
    H = omega_0/2 * qt.sigmaz()
    
    # Collapse operators
    c_ops = [
        np.sqrt(gamma) * qt.sigmam(),      # T1 relaxation
        np.sqrt(gamma_phi) * qt.sigmaz()   # Pure dephasing
    ]
    
    # Solve master equation
    print("Solving master equation for combined effects...")
    result = qt.mesolve(H, psi0, t_points, c_ops, [])
    
    # Calculate observables
    observables = {
        'P_ground': [],
        'P_excited': [],
        'coherence': [],
        'bloch_x': [],
        'bloch_y': [],
        'bloch_z': []
    }
    
    for state in tqdm(result.states, desc="Calculating observables"):
        # Populations
        observables['P_ground'].append(qt.expect(qt.projection(2, 0, 0), state))
        observables['P_excited'].append(qt.expect(qt.projection(2, 1, 1), state))
        
        # Bloch vector
        observables['bloch_x'].append(qt.expect(qt.sigmax(), state))
        observables['bloch_y'].append(qt.expect(qt.sigmay(), state))
        observables['bloch_z'].append(qt.expect(qt.sigmaz(), state))
        
        # Coherence
        rho = state
        if rho.type == 'ket':
            rho = qt.ket2dm(rho)
        observables['coherence'].append(abs(rho[0, 1]))
    
    return t_points, observables, result

def compare_closed_vs_open():
    """Compare closed system vs open system evolution."""
    print("⚖️  Comparing Closed vs Open System Evolution...")
    
    # Parameters
    omega_0 = 1.0
    omega_rabi = 0.2
    gamma = 0.1
    
    # Time evolution
    t_max = 25
    t_points = np.linspace(0, t_max, 200)
    
    # Initial state
    psi0 = qt.basis(2, 0)  # Ground state
    
    # Hamiltonian (Rabi oscillations)
    H = omega_0/2 * qt.sigmaz() + omega_rabi/2 * qt.sigmax()
    
    # Closed system evolution
    print("Solving closed system...")
    result_closed = qt.mesolve(H, psi0, t_points, [], [])
    
    # Open system evolution
    print("Solving open system...")
    c_ops = [np.sqrt(gamma) * qt.sigmam()]
    result_open = qt.mesolve(H, psi0, t_points, c_ops, [])
    
    # Calculate populations for both systems
    P_excited_closed = []
    P_excited_open = []
    
    for state_c, state_o in zip(result_closed.states, result_open.states):
        P_excited_closed.append(qt.expect(qt.projection(2, 1, 1), state_c))
        P_excited_open.append(qt.expect(qt.projection(2, 1, 1), state_o))
    
    return t_points, P_excited_closed, P_excited_open

def plot_decoherence_results():
    """Create comprehensive plots of all decoherence effects."""
    
    # Get all simulation results
    t1_results = simulate_t1_relaxation()
    t2_results = simulate_t2_dephasing()
    combined_results = simulate_t1_and_t2()
    comparison_results = compare_closed_vs_open()
    
    # Create the mega-plot
    fig = plt.figure(figsize=(16, 12))
    
    # Plot 1: T1 relaxation
    ax1 = plt.subplot(2, 3, 1)
    t_points, P_ground, P_excited, coherence, _ = t1_results
    plt.plot(t_points, P_excited, 'r-', linewidth=2, label='Excited |1⟩')
    plt.plot(t_points, P_ground, 'b-', linewidth=2, label='Ground |0⟩')
    
    # Theoretical T1 decay
    gamma = 0.1
    theory = np.exp(-gamma * t_points)
    plt.plot(t_points, theory, 'k--', alpha=0.7, label='Theory: e^(-γt)')
    
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.title('T1 Energy Relaxation')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: T2 dephasing - populations
    ax2 = plt.subplot(2, 3, 2)
    t_points, P_ground, P_excited, coherence, bloch_x, bloch_y, bloch_z, _ = t2_results
    plt.plot(t_points, P_excited, 'r-', linewidth=2, label='Excited |1⟩')
    plt.plot(t_points, P_ground, 'b-', linewidth=2, label='Ground |0⟩')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.title('T2 Dephasing - Populations')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: T2 dephasing - coherence
    ax3 = plt.subplot(2, 3, 3)
    plt.plot(t_points, coherence, 'g-', linewidth=2, label='|ρ₀₁|')
    
    # Theoretical T2 decay
    gamma_phi = 0.2
    coherence_theory = 0.5 * np.exp(-gamma_phi * t_points)
    plt.plot(t_points, coherence_theory, 'k--', alpha=0.7, label='Theory')
    
    plt.xlabel('Time')
    plt.ylabel('Coherence |rho_01|')
    plt.title('T2 Dephasing - Coherence Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 4: Combined T1 and T2 - Bloch vector
    ax4 = plt.subplot(2, 3, 4)
    t_points, observables, _ = combined_results
    plt.plot(t_points, observables['bloch_x'], 'r-', linewidth=2, label='<sigma_x>')
    plt.plot(t_points, observables['bloch_y'], 'g-', linewidth=2, label='<sigma_y>')
    plt.plot(t_points, observables['bloch_z'], 'b-', linewidth=2, label='<sigma_z>')
    plt.xlabel('Time')
    plt.ylabel('Expectation Value')
    plt.title('Combined T1 & T2 - Bloch Vector')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 5: Closed vs Open system
    ax5 = plt.subplot(2, 3, 5)
    t_points, P_excited_closed, P_excited_open = comparison_results
    plt.plot(t_points, P_excited_closed, 'b-', linewidth=2, label='Closed System')
    plt.plot(t_points, P_excited_open, 'r-', linewidth=2, label='Open System')
    plt.xlabel('Time')
    plt.ylabel('Excited State Population')
    plt.title('Closed vs Open System Evolution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 6: Bloch sphere trajectory for combined effects
    ax6 = plt.subplot(2, 3, 6, projection='3d')
    
    # Create Bloch sphere
    b = qt.Bloch()
    b.fig = fig
    b.axes = ax6
    
    # Add trajectory
    bloch_trajectory = np.array([
        observables['bloch_x'],
        observables['bloch_y'], 
        observables['bloch_z']
    ])
    
    b.add_points(bloch_trajectory)
    b.add_vectors(bloch_trajectory[:, 0], 'g')  # Initial state
    b.add_vectors(bloch_trajectory[:, -1], 'r')  # Final state
    b.render()
    ax6.set_title('Decoherence Trajectory\n(Green: Initial, Red: Final)')
    
    plt.tight_layout()
    plt.suptitle('QuTiP Demo: Quantum Decoherence and Open System Dynamics', 
                 fontsize=16, y=0.98)
    plt.show()

def demonstrate_different_environments():
    """Show how different environments affect quantum systems differently."""
    print("🌍 Demonstrating Different Environmental Effects...")
    
    # Parameters
    omega_0 = 1.0
    t_max = 20
    t_points = np.linspace(0, t_max, 150)
    
    # Initial state: superposition
    psi0 = create_superposition_state(np.pi/2, 0)
    
    # Hamiltonian
    H = omega_0/2 * qt.sigmaz()
    
    # Different environments
    environments = {
        'No Environment': [],
        'Amplitude Damping': [np.sqrt(0.1) * qt.sigmam()],
        'Phase Damping': [np.sqrt(0.1) * qt.sigmaz()],
        'Depolarizing': [np.sqrt(0.05) * qt.sigmax(), 
                        np.sqrt(0.05) * qt.sigmay(), 
                        np.sqrt(0.05) * qt.sigmaz()],
        'Hot Environment': [np.sqrt(0.1) * qt.sigmam(), 
                           np.sqrt(0.02) * qt.sigmap()]  # Thermal excitation
    }
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for i, (env_name, c_ops) in enumerate(environments.items()):
        if i >= len(axes):
            break
            
        print(f"Simulating {env_name}...")
        result = qt.mesolve(H, psi0, t_points, c_ops, [])
        
        # Calculate Bloch vector components
        bloch_x = [qt.expect(qt.sigmax(), state) for state in result.states]
        bloch_y = [qt.expect(qt.sigmay(), state) for state in result.states]
        bloch_z = [qt.expect(qt.sigmaz(), state) for state in result.states]
        
        # Plot trajectory
        axes[i].plot(t_points, bloch_x, 'r-', label='<sigma_x>')
        axes[i].plot(t_points, bloch_y, 'g-', label='<sigma_y>')
        axes[i].plot(t_points, bloch_z, 'b-', label='<sigma_z>')
        axes[i].set_title(env_name)
        axes[i].set_xlabel('Time')
        axes[i].set_ylabel('Expectation Value')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    # Remove unused subplot
    if len(environments) < len(axes):
        axes[-1].remove()
    
    plt.tight_layout()
    plt.suptitle('QuTiP Demo: Different Environmental Effects on Quantum Systems', 
                 fontsize=14, y=0.98)
    plt.show()

def main():
    """Main demo function."""
    print("🌊 Welcome to the QuTiP Quantum Decoherence Demo!")
    print("=" * 60)
    print("This demo explores how quantum systems lose coherence when")
    print("interacting with their environment - a fundamental aspect")
    print("of realistic quantum systems.")
    print("=" * 60)
    
    try:
        # Main decoherence plots
        plot_decoherence_results()
        print("✅ Main decoherence analysis completed!")
        
        # Different environments
        demonstrate_different_environments()
        print("✅ Environmental effects demonstration completed!")
        
    except Exception as e:
        print(f"❌ Error in decoherence demo: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎓 Key Learning Points:")
    print("• T1 (energy relaxation): quantum systems lose energy to environment")
    print("• T2 (dephasing): quantum superpositions lose phase coherence")
    print("• Open systems behave very differently from closed systems")
    print("• Different environments cause different types of decoherence")
    print("• QuTiP's master equation solver handles realistic quantum dynamics")
    
    print("\n🔬 Real-world relevance:")
    print("• Quantum computing: understanding qubit decoherence")
    print("• Quantum sensing: optimizing coherence times")
    print("• Quantum optics: cavity decay and atomic relaxation")
    print("• Quantum communication: channel noise characterization")
    
    print(f"\n📚 Learn more about open quantum systems at: https://qutip.org/")

if __name__ == "__main__":
    main()
