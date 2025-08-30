#!/usr/bin/env python3
"""
QuTiP Demo: Bloch Sphere Visualization and Rabi Oscillations

This script demonstrates:
1. Bloch sphere visualization of qubit states
2. Rabi oscillations under resonant driving
3. Different quantum gates and their effects
4. Time evolution of quantum states

Author: QuTiP Demo Project
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

def create_initial_states():
    """Create various interesting initial quantum states."""
    states = {
        'ground': qt.basis(2, 0),                    # |0⟩
        'excited': qt.basis(2, 1),                   # |1⟩
        'plus': (qt.basis(2, 0) + qt.basis(2, 1)).unit(),      # |+⟩ = (|0⟩ + |1⟩)/√2
        'minus': (qt.basis(2, 0) - qt.basis(2, 1)).unit(),     # |-⟩ = (|0⟩ - |1⟩)/√2
        'right': (qt.basis(2, 0) + 1j*qt.basis(2, 1)).unit(), # |R⟩ = (|0⟩ + i|1⟩)/√2
        'left': (qt.basis(2, 0) - 1j*qt.basis(2, 1)).unit(),  # |L⟩ = (|0⟩ - i|1⟩)/√2
    }
    return states

def rabi_hamiltonian(omega_0, omega_rabi):
    """
    Create the Rabi Hamiltonian for a two-level system.
    
    Parameters:
    omega_0: qubit frequency
    omega_rabi: Rabi frequency (coupling strength)
    """
    # Pauli matrices
    sigma_z = qt.sigmaz()
    sigma_x = qt.sigmax()
    
    # Hamiltonian: H = ω₀/2 σz + ΩR/2 σx
    H = omega_0/2 * sigma_z + omega_rabi/2 * sigma_x
    return H

def simulate_rabi_oscillations():
    """Simulate and visualize Rabi oscillations."""
    print("🎯 Simulating Rabi Oscillations...")
    
    # Parameters
    omega_0 = 1.0  # qubit frequency
    omega_rabi = 0.3  # Rabi frequency
    
    # Time evolution
    t_max = 20
    t_points = np.linspace(0, t_max, 200)
    
    # Initial state: ground state
    psi0 = qt.basis(2, 0)
    
    # Hamiltonian
    H = rabi_hamiltonian(omega_0, omega_rabi)
    
    # Solve the Schrödinger equation
    print("Solving Schrödinger equation...")
    result = qt.mesolve(H, psi0, t_points, [], [])
    
    # Calculate populations
    P_ground = []
    P_excited = []
    
    for state in tqdm(result.states, desc="Calculating populations"):
        P_ground.append(qt.expect(qt.num(2), state))  # Population of excited state
        P_excited.append(1 - P_ground[-1])  # Population of ground state
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Population dynamics
    ax1.plot(t_points, P_excited, 'b-', linewidth=2, label='Ground |0⟩')
    ax1.plot(t_points, P_ground, 'r-', linewidth=2, label='Excited |1⟩')
    ax1.set_xlabel('Time (1/ω₀)')
    ax1.set_ylabel('Population')
    ax1.set_title('Rabi Oscillations: Population Dynamics')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add theoretical prediction
    rabi_freq = omega_rabi
    P_excited_theory = np.sin(rabi_freq * t_points / 2)**2
    ax1.plot(t_points, P_excited_theory, 'k--', alpha=0.7, 
             label=f'Theory: Ω = {omega_rabi}')
    ax1.legend()
    
    # Plot 2: Bloch sphere trajectory
    b = qt.Bloch()
    b.fig = fig
    b.axes = ax2
    
    # Calculate Bloch vectors
    print("Calculating Bloch vectors...")
    bloch_vectors = []
    for state in tqdm(result.states, desc="Bloch vectors"):
        bloch_vectors.append([
            qt.expect(qt.sigmax(), state),
            qt.expect(qt.sigmay(), state),
            qt.expect(qt.sigmaz(), state)
        ])
    
    bloch_vectors = np.array(bloch_vectors)
    
    # Add trajectory to Bloch sphere
    b.add_points(bloch_vectors.T)
    b.add_vectors(bloch_vectors[-1])  # Final state
    b.add_vectors(bloch_vectors[0], 'g')  # Initial state
    b.point_color = ['b']
    b.point_size = [2]
    b.render()
    
    plt.tight_layout()
    plt.suptitle('QuTiP Demo: Rabi Oscillations Visualization', fontsize=16, y=1.02)
    plt.show()
    
    return result, t_points

def demonstrate_quantum_gates():
    """Demonstrate various quantum gates and their effects on the Bloch sphere."""
    print("\n🚪 Demonstrating Quantum Gates...")
    
    # Create initial state: |+⟩ = (|0⟩ + |1⟩)/√2
    initial_state = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    
    # Define quantum gates
    gates = {
        'I (Identity)': qt.qeye(2),
        'X (Pauli-X)': qt.sigmax(),
        'Y (Pauli-Y)': qt.sigmay(),
        'Z (Pauli-Z)': qt.sigmaz(),
        'H (Hadamard)': (qt.sigmax() + qt.sigmaz()).unit(),
        'S (Phase)': qt.qdiags([1, 1j], 0),
        'T (π/8)': qt.qdiags([1, np.exp(1j*np.pi/4)], 0),
    }
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    for i, (gate_name, gate) in enumerate(gates.items()):
        # Apply gate
        final_state = gate * initial_state
        
        # Calculate Bloch vector
        bloch_vector = [
            qt.expect(qt.sigmax(), final_state),
            qt.expect(qt.sigmay(), final_state),
            qt.expect(qt.sigmaz(), final_state)
        ]
        
        # Create subplot
        ax = fig.add_subplot(2, 4, i+1, projection='3d')
        
        # Create Bloch sphere
        b = qt.Bloch()
        b.fig = fig
        b.axes = ax
        
        # Add initial state (green) and final state (red)
        initial_bloch = [
            qt.expect(qt.sigmax(), initial_state),
            qt.expect(qt.sigmay(), initial_state),
            qt.expect(qt.sigmaz(), initial_state)
        ]
        
        b.add_vectors(initial_bloch, 'g')
        b.add_vectors(bloch_vector, 'r')
        b.render()
        ax.set_title(f'{gate_name}', fontsize=10)
    
    plt.tight_layout()
    plt.suptitle('QuTiP Demo: Quantum Gates on Bloch Sphere\n(Green: Initial |+>, Red: After Gate)', 
                 fontsize=14, y=0.98)
    plt.show()

def animated_bloch_evolution():
    """Create an animated Bloch sphere showing time evolution."""
    print("\n🎬 Creating Animated Bloch Sphere Evolution...")
    
    # Parameters for a more interesting evolution
    omega_0 = 1.0
    omega_x = 0.3
    omega_y = 0.2
    
    # Time-dependent Hamiltonian for interesting dynamics
    H = omega_0/2 * qt.sigmaz() + omega_x/2 * qt.sigmax() + omega_y/2 * qt.sigmay()
    
    # Initial state: superposition
    psi0 = (qt.basis(2, 0) + 0.7*qt.basis(2, 1)).unit()
    
    # Time points
    t_max = 10
    t_points = np.linspace(0, t_max, 100)
    
    # Solve evolution
    print("Solving for animated evolution...")
    result = qt.mesolve(H, psi0, t_points, [], [])
    
    # Calculate Bloch vectors
    bloch_vectors = []
    for state in result.states:
        bloch_vectors.append([
            qt.expect(qt.sigmax(), state),
            qt.expect(qt.sigmay(), state),
            qt.expect(qt.sigmaz(), state)
        ])
    
    # Create animation
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    b = qt.Bloch()
    b.fig = fig
    b.axes = ax
    
    def animate(frame):
        b.clear()
        # Add trajectory up to current frame
        if frame > 0:
            trajectory = np.array(bloch_vectors[:frame+1]).T
            b.add_points(trajectory)
        
        # Add current state vector
        b.add_vectors(bloch_vectors[frame], 'r')
        b.render()
        ax.set_title(f'Quantum State Evolution (t = {t_points[frame]:.2f})')
        # Ensure 3D axis properties are set correctly
        if hasattr(ax, 'set_xlim3d'):
            ax.set_xlim3d([-1, 1])
            ax.set_ylim3d([-1, 1])
            ax.set_zlim3d([-1, 1])
        return ax,
    
    # Create animation
    anim = FuncAnimation(fig, animate, frames=len(t_points), 
                        interval=100, blit=False, repeat=True)
    
    plt.show()
    
    # Save animation if desired
    # anim.save('bloch_evolution.gif', writer='pillow', fps=10)
    
    return anim

def main():
    """Main demo function."""
    print("🌟 Welcome to the QuTiP Bloch Sphere and Rabi Oscillations Demo!")
    print("=" * 60)
    print("This demo showcases QuTiP's capabilities for quantum state visualization")
    print("and dynamics simulation using the famous Bloch sphere representation.")
    print("=" * 60)
    
    # Demo 1: Rabi oscillations
    try:
        result, t_points = simulate_rabi_oscillations()
        print("✅ Rabi oscillations demo completed!")
    except Exception as e:
        print(f"❌ Error in Rabi oscillations demo: {e}")
    
    # Demo 2: Quantum gates
    try:
        demonstrate_quantum_gates()
        print("✅ Quantum gates demo completed!")
    except Exception as e:
        print(f"❌ Error in quantum gates demo: {e}")
    
    # Demo 3: Animated evolution
    try:
        anim = animated_bloch_evolution()
        print("✅ Animated Bloch sphere demo completed!")
    except Exception as e:
        print(f"❌ Error in animated demo: {e}")
    
    print("\n🎉 Demo completed! QuTiP makes quantum physics visualization easy and beautiful.")
    print("\nKey takeaways:")
    print("• QuTiP provides intuitive tools for quantum state manipulation")
    print("• Bloch sphere visualization makes quantum mechanics tangible")
    print("• Complex quantum dynamics can be simulated with just a few lines of code")
    print("• Perfect for education, research, and quantum technology development")
    
    print(f"\n📚 Learn more at: https://qutip.org/")

if __name__ == "__main__":
    main()
