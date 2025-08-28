#!/usr/bin/env python3
"""
QuTiP Demo: Cavity QED and Quantum Optics

This script demonstrates:
1. Jaynes-Cummings model (atom-cavity interactions)
2. Vacuum Rabi oscillations
3. Photon statistics and quantum light
4. Strong coupling regime effects
5. Cavity decay and atomic relaxation

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

def jaynes_cummings_hamiltonian(omega_c, omega_a, g, N_cavity=10):
    """
    Create the Jaynes-Cummings Hamiltonian for atom-cavity interaction.
    
    Parameters:
    omega_c: cavity frequency
    omega_a: atomic transition frequency  
    g: atom-cavity coupling strength
    N_cavity: maximum number of cavity photons to consider
    
    Returns Hamiltonian in the basis |n,ground⟩, |n,excited⟩
    """
    # Create operators
    # Cavity operators
    a = qt.tensor(qt.destroy(N_cavity), qt.qeye(2))  # cavity annihilation
    a_dag = a.dag()                                   # cavity creation
    n_c = a_dag * a                                   # cavity number operator
    
    # Atomic operators  
    sigma_z = qt.tensor(qt.qeye(N_cavity), qt.sigmaz())    # atomic inversion
    sigma_plus = qt.tensor(qt.qeye(N_cavity), qt.sigmap()) # atomic raising
    sigma_minus = qt.tensor(qt.qeye(N_cavity), qt.sigmam()) # atomic lowering
    
    # Jaynes-Cummings Hamiltonian
    # H = ωc a†a + ωa/2 σz + g(a†σ- + aσ+)
    H = omega_c * n_c + omega_a/2 * sigma_z + g * (a_dag * sigma_minus + a * sigma_plus)
    
    return H, a, a_dag, sigma_plus, sigma_minus, sigma_z

def vacuum_rabi_oscillations():
    """Demonstrate vacuum Rabi oscillations in the Jaynes-Cummings model."""
    print("🔄 Simulating Vacuum Rabi Oscillations...")
    
    # Parameters
    omega_c = 1.0    # cavity frequency
    omega_a = 1.0    # atomic frequency (resonant)
    g = 0.1          # coupling strength
    N_cavity = 10    # cavity Hilbert space size
    
    # Time evolution
    t_max = 40
    t_points = np.linspace(0, t_max, 300)
    
    # Create Hamiltonian and operators
    H, a, a_dag, sigma_plus, sigma_minus, sigma_z = jaynes_cummings_hamiltonian(
        omega_c, omega_a, g, N_cavity)
    
    # Initial state: atom excited, cavity vacuum |0,e⟩
    psi0 = qt.tensor(qt.basis(N_cavity, 0), qt.basis(2, 1))
    
    # Solve the Schrödinger equation
    print("Solving Jaynes-Cummings dynamics...")
    result = qt.mesolve(H, psi0, t_points, [], [])
    
    # Calculate observables
    print("Calculating observables...")
    P_excited = []  # Atomic excited state population
    P_ground = []   # Atomic ground state population
    n_photons = []  # Average photon number
    photon_dist = []  # Photon number distribution
    
    for state in tqdm(result.states, desc="Processing states"):
        # Atomic populations
        P_excited.append(qt.expect(sigma_plus * sigma_minus, state))
        P_ground.append(1 - P_excited[-1])
        
        # Cavity photon number
        n_photons.append(qt.expect(a_dag * a, state))
        
        # Photon number distribution for selected times
        if len(photon_dist) < 4 and len(P_excited) % (len(t_points)//4) == 0:
            # Calculate probability of each photon number
            probs = []
            for n in range(min(5, N_cavity)):  # Show first 5 Fock states
                proj_n = qt.tensor(qt.basis(N_cavity, n) * qt.basis(N_cavity, n).dag(), 
                                 qt.qeye(2))
                probs.append(qt.expect(proj_n, state))
            photon_dist.append(probs)
    
    return t_points, P_excited, P_ground, n_photons, photon_dist, result

def plot_vacuum_rabi():
    """Create plots for vacuum Rabi oscillations."""
    t_points, P_excited, P_ground, n_photons, photon_dist, result = vacuum_rabi_oscillations()
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 10))
    
    # Plot 1: Atomic populations
    ax1 = plt.subplot(2, 3, 1)
    plt.plot(t_points, P_excited, 'r-', linewidth=2, label='Excited |e>')
    plt.plot(t_points, P_ground, 'b-', linewidth=2, label='Ground |g>')
    
    # Add theoretical vacuum Rabi frequency
    g = 0.1
    theory = 0.5 * (1 + np.cos(2*g*t_points))
    plt.plot(t_points, theory, 'k--', alpha=0.7, label='Theory')
    
    plt.xlabel('Time (1/ωc)')
    plt.ylabel('Population')
    plt.title('Vacuum Rabi Oscillations')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Cavity photon number
    ax2 = plt.subplot(2, 3, 2)
    plt.plot(t_points, n_photons, 'g-', linewidth=2, label='<n>')
    
    # Theoretical photon number
    n_theory = 0.5 * (1 - np.cos(2*g*t_points))
    plt.plot(t_points, n_theory, 'k--', alpha=0.7, label='Theory')
    
    plt.xlabel('Time (1/ωc)')
    plt.ylabel('Average Photon Number')
    plt.title('Cavity Photon Dynamics')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Energy exchange
    ax3 = plt.subplot(2, 3, 3)
    plt.plot(t_points, P_excited, 'r-', linewidth=2, label='Atomic Energy')
    plt.plot(t_points, n_photons, 'g-', linewidth=2, label='Cavity Energy')
    total_energy = np.array(P_excited) + np.array(n_photons)
    plt.plot(t_points, total_energy, 'k-', linewidth=2, label='Total Energy')
    plt.xlabel('Time (1/ωc)')
    plt.ylabel('Energy (hbar*w units)')
    plt.title('Energy Exchange')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 4-6: Photon number distributions at different times
    for i, (probs, time_idx) in enumerate(zip(photon_dist, [0, len(t_points)//4, len(t_points)//2, 3*len(t_points)//4])):
        if i >= 3:
            break
        ax = plt.subplot(2, 3, 4+i)
        n_values = list(range(len(probs)))
        plt.bar(n_values, probs, alpha=0.7, color=f'C{i}')
        plt.xlabel('Photon Number n')
        plt.ylabel('Probability')
        plt.title(f'Photon Distribution (t={t_points[time_idx]:.1f})')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.suptitle('QuTiP Demo: Jaynes-Cummings Model - Vacuum Rabi Oscillations', 
                 fontsize=16, y=0.98)
    plt.show()

def thermal_state_evolution():
    """Demonstrate evolution starting from thermal cavity state."""
    print("🌡️  Simulating Thermal State Evolution...")
    
    # Parameters
    omega_c = 1.0
    omega_a = 1.0
    g = 0.15
    N_cavity = 15
    n_thermal = 2.0  # Average thermal photon number
    
    # Time evolution
    t_max = 30
    t_points = np.linspace(0, t_max, 200)
    
    # Create Hamiltonian
    H, a, a_dag, sigma_plus, sigma_minus, sigma_z = jaynes_cummings_hamiltonian(
        omega_c, omega_a, g, N_cavity)
    
    # Create thermal state for cavity
    cavity_thermal = qt.thermal_dm(N_cavity, n_thermal)
    atom_ground = qt.basis(2, 0) * qt.basis(2, 0).dag()
    
    # Initial state: thermal cavity + ground atom
    rho0 = qt.tensor(cavity_thermal, atom_ground)
    
    # Solve master equation
    print("Solving thermal state evolution...")
    result = qt.mesolve(H, rho0, t_points, [], [])
    
    # Calculate observables
    P_excited = []
    n_photons = []
    photon_variance = []
    
    for state in tqdm(result.states, desc="Calculating observables"):
        P_excited.append(qt.expect(sigma_plus * sigma_minus, state))
        n_avg = qt.expect(a_dag * a, state)
        n_photons.append(n_avg)
        n_squared = qt.expect(a_dag * a_dag * a * a, state)
        photon_variance.append(n_squared - n_avg**2)
    
    return t_points, P_excited, n_photons, photon_variance

def strong_coupling_regime():
    """Demonstrate strong coupling effects with varying coupling strength."""
    print("💪 Exploring Strong Coupling Regime...")
    
    # Parameters
    omega_c = 1.0
    omega_a = 1.0
    N_cavity = 8
    
    # Different coupling strengths
    g_values = [0.05, 0.1, 0.2, 0.3]  # From weak to strong coupling
    
    # Time evolution
    t_max = 25
    t_points = np.linspace(0, t_max, 200)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()
    
    for i, g in enumerate(g_values):
        print(f"Simulating g = {g}...")
        
        # Create Hamiltonian
        H, a, a_dag, sigma_plus, sigma_minus, sigma_z = jaynes_cummings_hamiltonian(
            omega_c, omega_a, g, N_cavity)
        
        # Initial state: atom excited, cavity vacuum
        psi0 = qt.tensor(qt.basis(N_cavity, 0), qt.basis(2, 1))
        
        # Solve
        result = qt.mesolve(H, psi0, t_points, [], [])
        
        # Calculate atomic excited state population
        P_excited = [qt.expect(sigma_plus * sigma_minus, state) for state in result.states]
        
        # Plot
        axes[i].plot(t_points, P_excited, 'r-', linewidth=2, label=f'g = {g}')
        
        # Add theoretical Rabi frequency
        rabi_freq = 2*g  # Vacuum Rabi frequency
        theory = 0.5 * (1 + np.cos(rabi_freq * t_points))
        axes[i].plot(t_points, theory, 'k--', alpha=0.7, label='Theory')
        
        axes[i].set_xlabel('Time (1/ωc)')
        axes[i].set_ylabel('Excited State Population')
        axes[i].set_title(f'Coupling g = {g} (Omega_R = {rabi_freq:.2f})')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.suptitle('QuTiP Demo: Strong Coupling Regime in Cavity QED', 
                 fontsize=14, y=0.98)
    plt.show()

def cavity_decay_effects():
    """Demonstrate effects of cavity decay on dynamics."""
    print("📉 Simulating Cavity Decay Effects...")
    
    # Parameters
    omega_c = 1.0
    omega_a = 1.0
    g = 0.1
    kappa_values = [0.0, 0.02, 0.05, 0.1]  # Cavity decay rates
    N_cavity = 10
    
    # Time evolution
    t_max = 40
    t_points = np.linspace(0, t_max, 200)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()
    
    for i, kappa in enumerate(kappa_values):
        print(f"Simulating κ = {kappa}...")
        
        # Create Hamiltonian
        H, a, a_dag, sigma_plus, sigma_minus, sigma_z = jaynes_cummings_hamiltonian(
            omega_c, omega_a, g, N_cavity)
        
        # Initial state: atom excited, cavity vacuum
        psi0 = qt.tensor(qt.basis(N_cavity, 0), qt.basis(2, 1))
        
        # Collapse operators for cavity decay
        c_ops = []
        if kappa > 0:
            c_ops.append(np.sqrt(kappa) * a)  # Cavity photon loss
        
        # Solve master equation
        result = qt.mesolve(H, psi0, t_points, c_ops, [])
        
        # Calculate observables
        P_excited = [qt.expect(sigma_plus * sigma_minus, state) for state in result.states]
        n_photons = [qt.expect(a_dag * a, state) for state in result.states]
        
        # Plot atomic population
        axes[i].plot(t_points, P_excited, 'r-', linewidth=2, label='Excited |e>')
        axes[i].plot(t_points, n_photons, 'g-', linewidth=2, label='<n>')
        
        axes[i].set_xlabel('Time (1/ωc)')
        axes[i].set_ylabel('Population / Photon Number')
        
        if kappa == 0:
            axes[i].set_title('No Decay (kappa = 0)')
        else:
            axes[i].set_title(f'Cavity Decay kappa = {kappa}')
        
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.suptitle('QuTiP Demo: Effects of Cavity Decay on Atom-Cavity Dynamics', 
                 fontsize=14, y=0.98)
    plt.show()

def photon_statistics():
    """Analyze photon statistics for different quantum states."""
    print("📊 Analyzing Photon Statistics...")
    
    N_cavity = 15  # Reduced size to avoid numerical issues
    
    # Different quantum states
    states = {
        'Vacuum': qt.basis(N_cavity, 0),
        'Fock n=3': qt.basis(N_cavity, 3),
        'Coherent α=1.5': qt.coherent(N_cavity, 1.5),  # Reduced alpha
        'Thermal n̄=2': qt.thermal_dm(N_cavity, 2),  # Reduced thermal photons
        # Skip squeezed state as it can cause numerical issues
    }
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for i, (state_name, state) in enumerate(states.items()):
        if i >= len(axes):
            break
        
        # Calculate photon number distribution
        try:
            if state.type == 'ket':
                probs = [float(abs(state[n])**2) for n in range(min(10, N_cavity))]
            else:  # density matrix
                probs = [float(state[n,n].real) for n in range(min(10, N_cavity))]
            
            # Normalize probabilities to avoid numerical errors
            prob_sum = sum(probs)
            if prob_sum > 0:
                probs = [p/prob_sum for p in probs]
            
            # Calculate statistics
            n_avg = sum(n * p for n, p in enumerate(probs))
            n_squared = sum(n**2 * p for n, p in enumerate(probs))
            variance = max(0, n_squared - n_avg**2)  # Ensure non-negative
            
            # Mandel Q parameter
            if n_avg > 1e-10:
                mandel_q = (variance - n_avg) / n_avg
            else:
                mandel_q = 0
            
            # Plot distribution
            n_values = list(range(len(probs)))
            axes[i].bar(n_values, probs, alpha=0.7, color=f'C{i}')
            
        except Exception as e:
            print(f"Warning: Could not analyze {state_name}: {e}")
            # Create empty plot
            axes[i].text(0.5, 0.5, f'Error analyzing\n{state_name}', 
                        ha='center', va='center', transform=axes[i].transAxes)
            n_avg = 0
            mandel_q = 0
        axes[i].set_xlabel('Photon Number n')
        axes[i].set_ylabel('Probability')
        axes[i].set_title(f'{state_name}\\n<n>={n_avg:.2f}, Q={mandel_q:.2f}')
        axes[i].grid(True, alpha=0.3)
    
    # Remove unused subplot
    if len(states) < len(axes):
        axes[-1].remove()
    
    plt.tight_layout()
    plt.suptitle('QuTiP Demo: Photon Statistics for Different Quantum States\n(Q<0: sub-Poisson, Q=0: Poisson, Q>0: super-Poisson)', 
                 fontsize=14, y=0.98)
    plt.show()

def main():
    """Main demo function."""
    print("🔬 Welcome to the QuTiP Cavity QED and Quantum Optics Demo!")
    print("=" * 65)
    print("This demo explores the fascinating world of quantum optics,")
    print("where atoms and light interact in ways that have no classical analog.")
    print("=" * 65)
    
    try:
        # Demo 1: Vacuum Rabi oscillations
        plot_vacuum_rabi()
        print("✅ Vacuum Rabi oscillations demo completed!")
        
        # Demo 2: Thermal state evolution
        t_points, P_excited, n_photons, photon_var = thermal_state_evolution()
        
        plt.figure(figsize=(12, 4))
        plt.subplot(1, 3, 1)
        plt.plot(t_points, P_excited, 'r-', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('Excited Population')
        plt.title('Thermal State: Atomic Evolution')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 3, 2)
        plt.plot(t_points, n_photons, 'g-', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('⟨n⟩')
        plt.title('Thermal State: Photon Number')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 3, 3)
        plt.plot(t_points, photon_var, 'b-', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('Var(n)')
        plt.title('Thermal State: Photon Variance')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.suptitle('QuTiP Demo: Thermal Cavity State Evolution', fontsize=14)
        plt.show()
        print("✅ Thermal state evolution demo completed!")
        
        # Demo 3: Strong coupling regime
        strong_coupling_regime()
        print("✅ Strong coupling regime demo completed!")
        
        # Demo 4: Cavity decay effects
        cavity_decay_effects()
        print("✅ Cavity decay effects demo completed!")
        
        # Demo 5: Photon statistics
        photon_statistics()
        print("✅ Photon statistics demo completed!")
        
    except Exception as e:
        print(f"❌ Error in cavity QED demo: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎓 Key Learning Points:")
    print("• Jaynes-Cummings model describes fundamental atom-light interactions")
    print("• Vacuum Rabi oscillations show energy exchange between atom and cavity")
    print("• Strong coupling enables coherent quantum dynamics")
    print("• Cavity decay introduces realistic decoherence effects")
    print("• Different quantum states have distinct photon statistics")
    print("• QuTiP handles complex quantum optics systems with ease")
    
    print("\n🔬 Real-world Applications:")
    print("• Quantum computing: cavity-based qubits and gates")
    print("• Quantum communication: single-photon sources")
    print("• Quantum sensing: enhanced measurement precision")
    print("• Fundamental physics: testing quantum mechanics")
    print("• Quantum technology: lasers, masers, and quantum devices")
    
    print(f"\n📚 Explore more quantum optics with QuTiP at: https://qutip.org/")

if __name__ == "__main__":
    main()
