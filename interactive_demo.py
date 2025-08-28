#!/usr/bin/env python3
"""
QuTiP Interactive Demo: Quantum Dynamics Visualizer

This script provides an interactive demonstration of QuTiP's capabilities
using matplotlib widgets for real-time parameter control.

Features:
- Interactive Bloch sphere visualization
- Real-time parameter sliders
- Multiple quantum phenomena demonstrations
- Educational tooltips and explanations

Author: QuTiP Demo Project
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import qutip as qt
import warnings
warnings.filterwarnings('ignore')

# Set up matplotlib for interactive plots
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11

class InteractiveQuTiPDemo:
    """Interactive QuTiP demonstration with matplotlib widgets."""
    
    def __init__(self):
        """Initialize the interactive demo."""
        self.fig = None
        self.current_demo = 'rabi'
        self.setup_interface()
        
    def setup_interface(self):
        """Set up the main interface with controls and plots."""
        self.fig = plt.figure(figsize=(16, 12))
        self.fig.suptitle('🌟 Interactive QuTiP Demo: Quantum Dynamics Visualizer', 
                         fontsize=16, fontweight='bold')
        
        # Create subplot layout
        # Controls on the left, main plots on the right
        self.ax_controls = plt.subplot2grid((4, 4), (0, 0), rowspan=4, colspan=1)
        self.ax_main1 = plt.subplot2grid((4, 4), (0, 1), rowspan=2, colspan=2)
        self.ax_main2 = plt.subplot2grid((4, 4), (2, 1), rowspan=2, colspan=2, projection='3d')
        self.ax_info = plt.subplot2grid((4, 4), (0, 3), rowspan=4, colspan=1)
        
        # Remove axes for control and info panels
        self.ax_controls.set_xticks([])
        self.ax_controls.set_yticks([])
        self.ax_info.set_xticks([])
        self.ax_info.set_yticks([])
        
        self.setup_controls()
        self.setup_info_panel()
        self.update_plots()
        
    def setup_controls(self):
        """Set up control widgets."""
        self.ax_controls.clear()
        self.ax_controls.set_title('🎛️ Controls', fontweight='bold', pad=20)
        
        # Demo selection radio buttons
        self.ax_controls.text(0.1, 0.95, 'Demo Type:', fontweight='bold', transform=self.ax_controls.transAxes)
        
        # Create slider axes
        slider_height = 0.03
        slider_spacing = 0.06
        start_y = 0.8
        
        # Parameter sliders (will be updated based on demo type)
        self.slider_axes = {}
        self.sliders = {}
        
        # Rabi oscillation parameters
        self.create_slider('omega_rabi', 'Rabi Freq (Ω)', 0.0, 1.0, 0.2, start_y)
        self.create_slider('detuning', 'Detuning (Δ)', -0.5, 0.5, 0.0, start_y - slider_spacing)
        self.create_slider('time_max', 'Time Max', 5, 50, 20, start_y - 2*slider_spacing)
        
        # Decoherence parameters
        self.create_slider('gamma', 'T1 Rate (γ)', 0.0, 0.2, 0.05, start_y - 3*slider_spacing)
        self.create_slider('gamma_phi', 'T2 Rate (γφ)', 0.0, 0.3, 0.1, start_y - 4*slider_spacing)
        
        # Cavity QED parameters
        self.create_slider('coupling', 'Coupling (g)', 0.02, 0.3, 0.1, start_y - 5*slider_spacing)
        self.create_slider('cavity_decay', 'Cavity Decay (κ)', 0.0, 0.1, 0.0, start_y - 6*slider_spacing)
        
        # Demo type buttons
        button_y = 0.2
        button_height = 0.04
        button_spacing = 0.05
        
        self.demo_buttons = {}
        demos = [('Rabi Oscillations', 'rabi'), ('Decoherence', 'decoherence'), ('Cavity QED', 'cavity')]
        
        for i, (name, key) in enumerate(demos):
            ax_button = plt.axes([0.02, button_y - i*button_spacing, 0.15, button_height])
            button = Button(ax_button, name)
            button.on_clicked(lambda x, demo=key: self.switch_demo(demo))
            self.demo_buttons[key] = button
        
        # Update button
        ax_update = plt.axes([0.02, 0.02, 0.15, button_height])
        self.update_button = Button(ax_update, '🔄 Update', color='lightgreen')
        self.update_button.on_clicked(lambda x: self.update_plots())
        
        # Hide control axes
        self.ax_controls.set_xlim(0, 1)
        self.ax_controls.set_ylim(0, 1)
        for spine in self.ax_controls.spines.values():
            spine.set_visible(False)
    
    def create_slider(self, name, label, vmin, vmax, vinit, y_pos):
        """Create a parameter slider."""
        ax_slider = plt.axes([0.02, y_pos, 0.15, 0.02])
        slider = Slider(ax_slider, label, vmin, vmax, valinit=vinit, valfmt='%.3f')
        slider.on_changed(lambda val: self.on_slider_change())
        
        self.slider_axes[name] = ax_slider
        self.sliders[name] = slider
    
    def on_slider_change(self):
        """Handle slider value changes."""
        # Update plots when sliders change
        self.update_plots()
    
    def switch_demo(self, demo_type):
        """Switch between different demo types."""
        self.current_demo = demo_type
        self.update_info_panel()
        self.update_plots()
    
    def setup_info_panel(self):
        """Set up information panel."""
        self.update_info_panel()
    
    def update_info_panel(self):
        """Update the information panel with current demo info."""
        self.ax_info.clear()
        self.ax_info.set_title('📚 Information', fontweight='bold', pad=20)
        
        info_text = {
            'rabi': """
🎯 Rabi Oscillations

Description:
Two-level quantum system driven by 
an external field. Shows coherent 
oscillations between ground and 
excited states.

Parameters:
• Ω (Rabi frequency): Coupling strength
• Δ (Detuning): Drive-qubit frequency difference
• Time: Evolution duration

Physics:
- Resonant driving (Δ=0) gives pure oscillations
- Off-resonant driving reduces amplitude
- Demonstrates quantum coherence

Applications:
- Quantum gate operations
- Qubit control in quantum computing
- Atomic physics experiments
            """,
            
            'decoherence': """
🌀 Quantum Decoherence

Description:
Shows how quantum systems lose 
coherence when interacting with 
their environment.

Parameters:
• γ (T1 rate): Energy relaxation rate
• γφ (T2 rate): Pure dephasing rate
• Time: Evolution duration

Physics:
- T1: Population decay |1⟩ → |0⟩
- T2: Phase coherence loss
- Open vs closed system comparison

Applications:
- Quantum error correction
- Qubit design optimization
- Understanding quantum-to-classical transition
            """,
            
            'cavity': """
🔬 Cavity QED

Description:
Atom-cavity interactions showing 
vacuum Rabi oscillations and 
photon exchange dynamics.

Parameters:
• g (Coupling): Atom-cavity coupling strength
• κ (Decay): Cavity photon loss rate
• Detuning: Atom-cavity frequency difference

Physics:
- Jaynes-Cummings model
- Strong vs weak coupling regimes
- Quantum light-matter interaction

Applications:
- Quantum computing with cavity qubits
- Single photon sources
- Quantum sensing
            """
        }
        
        text = info_text.get(self.current_demo, "Select a demo to see information")
        self.ax_info.text(0.05, 0.95, text, transform=self.ax_info.transAxes, 
                         fontsize=9, verticalalignment='top', wrap=True)
        
        # Hide info axes
        self.ax_info.set_xlim(0, 1)
        self.ax_info.set_ylim(0, 1)
        for spine in self.ax_info.spines.values():
            spine.set_visible(False)
    
    def get_current_parameters(self):
        """Get current parameter values from sliders."""
        params = {}
        for name, slider in self.sliders.items():
            params[name] = slider.val
        return params
    
    def update_plots(self):
        """Update the main plots based on current demo and parameters."""
        params = self.get_current_parameters()
        
        if self.current_demo == 'rabi':
            self.plot_rabi_oscillations(params)
        elif self.current_demo == 'decoherence':
            self.plot_decoherence(params)
        elif self.current_demo == 'cavity':
            self.plot_cavity_qed(params)
        
        self.fig.canvas.draw()
    
    def plot_rabi_oscillations(self, params):
        """Plot Rabi oscillations demonstration."""
        # Clear axes
        self.ax_main1.clear()
        self.ax_main2.clear()
        
        # Parameters
        omega_rabi = params['omega_rabi']
        detuning = params['detuning']
        t_max = params['time_max']
        
        # Time evolution
        t_points = np.linspace(0, t_max, 200)
        
        # Initial state: ground state
        psi0 = qt.basis(2, 0)
        
        # Hamiltonian
        omega_0 = 1.0
        H = (omega_0 + detuning)/2 * qt.sigmaz() + omega_rabi/2 * qt.sigmax()
        
        # Solve evolution
        result = qt.mesolve(H, psi0, t_points, [], [])
        
        # Calculate observables
        P_excited = [qt.expect(qt.num(2), state) for state in result.states]
        bloch_x = [qt.expect(qt.sigmax(), state) for state in result.states]
        bloch_y = [qt.expect(qt.sigmay(), state) for state in result.states]
        bloch_z = [qt.expect(qt.sigmaz(), state) for state in result.states]
        
        # Plot 1: Population dynamics
        self.ax_main1.plot(t_points, P_excited, 'r-', linewidth=2, label='Excited |1⟩')
        self.ax_main1.plot(t_points, 1-np.array(P_excited), 'b-', linewidth=2, label='Ground |0⟩')
        
        # Add theoretical curve for resonant case
        if abs(detuning) < 0.01:
            theory = 0.5 * (1 - np.cos(omega_rabi * t_points))
            self.ax_main1.plot(t_points, theory, 'k--', alpha=0.7, label='Theory')
        
        self.ax_main1.set_xlabel('Time')
        self.ax_main1.set_ylabel('Population')
        self.ax_main1.set_title(f'Rabi Oscillations: Ω={omega_rabi:.3f}, Δ={detuning:.3f}')
        self.ax_main1.legend()
        self.ax_main1.grid(True, alpha=0.3)
        
        # Plot 2: Bloch sphere
        b = qt.Bloch()
        b.fig = self.fig
        b.axes = self.ax_main2
        
        # Add trajectory
        bloch_vectors = np.array([bloch_x, bloch_y, bloch_z])
        b.add_points(bloch_vectors)
        
        # Mark start and end points
        b.add_vectors([bloch_x[0], bloch_y[0], bloch_z[0]], 'g')  # Start
        b.add_vectors([bloch_x[-1], bloch_y[-1], bloch_z[-1]], 'r')  # End
        
        b.render()
        self.ax_main2.set_title('Bloch Sphere Trajectory')
    
    def plot_decoherence(self, params):
        """Plot quantum decoherence demonstration."""
        # Clear axes
        self.ax_main1.clear()
        self.ax_main2.clear()
        
        # Parameters
        gamma = params['gamma']
        gamma_phi = params['gamma_phi']
        t_max = params['time_max']
        
        # Time evolution
        t_points = np.linspace(0, t_max, 200)
        
        # Initial state: superposition
        psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
        
        # Hamiltonian
        H = 0.5 * qt.sigmaz()
        
        # Collapse operators
        c_ops = []
        if gamma > 0:
            c_ops.append(np.sqrt(gamma) * qt.sigmam())
        if gamma_phi > 0:
            c_ops.append(np.sqrt(gamma_phi) * qt.sigmaz())
        
        # Solve evolution (closed and open systems)
        result_closed = qt.mesolve(H, psi0, t_points, [], [])
        result_open = qt.mesolve(H, psi0, t_points, c_ops, [])
        
        # Calculate coherence
        def get_coherence(states):
            coherence = []
            for state in states:
                if state.type == 'ket':
                    rho = qt.ket2dm(state)
                else:
                    rho = state
                coherence.append(abs(rho[0, 1]))
            return coherence
        
        coherence_closed = get_coherence(result_closed.states)
        coherence_open = get_coherence(result_open.states)
        
        # Plot 1: Coherence comparison
        self.ax_main1.plot(t_points, coherence_closed, 'b-', linewidth=2, label='Closed System')
        self.ax_main1.plot(t_points, coherence_open, 'r-', linewidth=2, label='Open System')
        
        # Add theoretical T2 decay
        if gamma_phi > 0 or gamma > 0:
            total_decay = gamma/2 + gamma_phi
            theory = 0.5 * np.exp(-total_decay * t_points)
            self.ax_main1.plot(t_points, theory, 'k--', alpha=0.7, label='Theory')
        
        self.ax_main1.set_xlabel('Time')
        self.ax_main1.set_ylabel('Coherence |ρ₀₁|')
        self.ax_main1.set_title(f'Decoherence: γ={gamma:.3f}, γφ={gamma_phi:.3f}')
        self.ax_main1.legend()
        self.ax_main1.grid(True, alpha=0.3)
        
        # Plot 2: Bloch sphere trajectory for open system
        bloch_vectors = []
        for state in result_open.states[::10]:  # Subsample for performance
            bloch_vectors.append([
                qt.expect(qt.sigmax(), state),
                qt.expect(qt.sigmay(), state),
                qt.expect(qt.sigmaz(), state)
            ])
        
        b = qt.Bloch()
        b.fig = self.fig
        b.axes = self.ax_main2
        
        if bloch_vectors:
            trajectory = np.array(bloch_vectors).T
            b.add_points(trajectory)
            b.add_vectors(bloch_vectors[0], 'g')   # Start
            b.add_vectors(bloch_vectors[-1], 'r')  # End
        
        b.render()
        self.ax_main2.set_title('Open System Trajectory')
    
    def plot_cavity_qed(self, params):
        """Plot cavity QED demonstration."""
        # Clear axes
        self.ax_main1.clear()
        self.ax_main2.clear()
        
        # Parameters
        g = params['coupling']
        kappa = params['cavity_decay']
        t_max = params['time_max']
        
        # System parameters
        omega_c = 1.0
        omega_a = 1.0
        N_cavity = 8
        
        # Time evolution
        t_points = np.linspace(0, t_max, 200)
        
        # Create Hamiltonian
        a = qt.tensor(qt.destroy(N_cavity), qt.qeye(2))
        a_dag = a.dag()
        sigma_plus = qt.tensor(qt.qeye(N_cavity), qt.sigmap())
        sigma_minus = qt.tensor(qt.qeye(N_cavity), qt.sigmam())
        
        H = omega_c * a_dag * a + omega_a/2 * qt.tensor(qt.qeye(N_cavity), qt.sigmaz()) + \
            g * (a_dag * sigma_minus + a * sigma_plus)
        
        # Initial state: vacuum cavity + excited atom
        psi0 = qt.tensor(qt.basis(N_cavity, 0), qt.basis(2, 1))
        
        # Collapse operators
        c_ops = []
        if kappa > 0:
            c_ops.append(np.sqrt(kappa) * a)
        
        # Solve evolution
        result = qt.mesolve(H, psi0, t_points, c_ops, [])
        
        # Calculate observables
        P_excited = [qt.expect(sigma_plus * sigma_minus, state) for state in result.states]
        n_photons = [qt.expect(a_dag * a, state) for state in result.states]
        
        # Plot 1: Energy exchange
        self.ax_main1.plot(t_points, P_excited, 'r-', linewidth=2, label='Atomic Energy')
        self.ax_main1.plot(t_points, n_photons, 'g-', linewidth=2, label='Cavity Energy')
        
        # Add theoretical vacuum Rabi oscillations
        if kappa == 0:
            rabi_freq = 2 * g
            theory_atom = 0.5 * (1 + np.cos(rabi_freq * t_points))
            theory_cavity = 0.5 * (1 - np.cos(rabi_freq * t_points))
            self.ax_main1.plot(t_points, theory_atom, 'k--', alpha=0.7, label='Theory')
        
        self.ax_main1.set_xlabel('Time')
        self.ax_main1.set_ylabel('Energy (ℏω units)')
        self.ax_main1.set_title(f'Cavity QED: g={g:.3f}, κ={kappa:.3f}')
        self.ax_main1.legend()
        self.ax_main1.grid(True, alpha=0.3)
        
        # Plot 2: 3D visualization of photon number distribution evolution
        # Show photon number probability at a few time points
        times_to_show = [0, len(result.states)//3, 2*len(result.states)//3, -1]
        time_labels = [t_points[i] for i in times_to_show]
        
        # Calculate photon distributions
        photon_probs = []
        max_n = min(6, N_cavity)
        
        for idx in times_to_show:
            state = result.states[idx]
            probs = []
            for n in range(max_n):
                proj_n = qt.tensor(qt.basis(N_cavity, n) * qt.basis(N_cavity, n).dag(), 
                                 qt.qeye(2))
                probs.append(qt.expect(proj_n, state))
            photon_probs.append(probs)
        
        # Create 3D bar plot
        self.ax_main2.clear()
        
        # Set up 3D bar chart
        x_pos = np.arange(max_n)
        y_pos = np.arange(len(times_to_show))
        
        for i, (probs, time_label) in enumerate(zip(photon_probs, time_labels)):
            self.ax_main2.bar(x_pos, probs, zs=i, zdir='y', alpha=0.7, 
                             label=f't={time_label:.1f}')
        
        self.ax_main2.set_xlabel('Photon Number n')
        self.ax_main2.set_ylabel('Time')
        self.ax_main2.set_zlabel('Probability')
        self.ax_main2.set_title('Photon Statistics Evolution')
    
    def show(self):
        """Display the interactive demo."""
        plt.tight_layout()
        plt.show()

def main():
    """Main function to run the interactive demo."""
    print("🌟 Starting Interactive QuTiP Demo...")
    print("=" * 50)
    print("This interactive demonstration showcases QuTiP's powerful")
    print("quantum simulation capabilities with real-time parameter control.")
    print("=" * 50)
    
    # Create and show the demo
    demo = InteractiveQuTiPDemo()
    
    print("✅ Demo interface created successfully!")
    print("\n🎮 How to use:")
    print("• Use the sliders to adjust parameters in real-time")
    print("• Click the demo buttons to switch between demonstrations")
    print("• Click 'Update' to refresh the plots")
    print("• Observe how quantum systems respond to parameter changes")
    
    print(f"\n📚 Learn more about QuTiP at: https://qutip.org/")
    
    demo.show()

if __name__ == "__main__":
    main()
