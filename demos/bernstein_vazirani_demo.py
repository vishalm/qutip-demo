#!/usr/bin/env python3
"""
Qiskit Demo: Bernstein-Vazirani Algorithm

This demo showcases the power of quantum computing using IBM's Qiskit framework
to implement the Bernstein-Vazirani algorithm. This algorithm demonstrates 
quantum advantage by finding a hidden binary string in just one query, 
whereas classical algorithms require up to n queries.

The Bernstein-Vazirani algorithm is perfect for demonstrating:
- Quantum superposition and interference
- Oracle-based quantum algorithms
- Quantum advantage over classical computation
- Qiskit circuit construction and simulation

Author: QuTiP/Qiskit Demo Project
License: MIT
Reference: https://www.ibm.com/quantum/qiskit
"""

import random
import time
from typing import Tuple, Dict
import numpy as np

try:
    from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
    from qiskit_aer import AerSimulator
    from qiskit import transpile
    from qiskit.visualization import plot_histogram
    import matplotlib.pyplot as plt
    QISKIT_AVAILABLE = True
except ImportError as e:
    print(f"❌ Qiskit not installed: {e}")
    print("Install with: pip install qiskit qiskit-aer")
    QISKIT_AVAILABLE = False

def bernstein_vazirani_circuit(secret_bits: str) -> Tuple[QuantumCircuit, int]:
    """
    Build the Bernstein-Vazirani circuit for a given secret bitstring s.
    
    The BV algorithm uses quantum superposition and interference to determine
    a hidden bitstring s in a single oracle query, compared to n classical queries.
    
    Args:
        secret_bits: Hidden binary string to recover
        
    Returns:
        Tuple of (quantum_circuit, number_of_bits)
    """
    n = len(secret_bits)
    
    # Create quantum registers: n input qubits + 1 ancilla
    x = QuantumRegister(n, 'x')      # Input qubits
    anc = QuantumRegister(1, 'anc')  # Ancilla qubit for oracle
    c = ClassicalRegister(n, 'c')    # Classical bits for measurement
    qc = QuantumCircuit(x, anc, c)
    
    # Step 1: Initialize ancilla in |-> = (|0>-|1>)/sqrt(2)
    # This creates the phase kickback effect
    qc.x(anc)
    qc.h(anc)
    
    # Step 2: Put input qubits into uniform superposition
    # Creates superposition of all possible n-bit strings
    qc.h(x)
    
    # Step 3: Oracle U_f implementation
    # For each bit s_i=1, apply CNOT from x_i to ancilla
    # This encodes f_s(x) = s·x (mod 2) as a phase
    for i, bit in enumerate(secret_bits):
        if bit == '1':
            qc.cx(x[i], anc[0])
    
    # Step 4: Undo the input Hadamards to create interference
    # Converts phase differences back to computational basis
    qc.h(x)
    
    # Step 5: Measure input qubits (ancilla not needed)
    qc.measure(x, c)
    
    return qc, n

def classical_baseline(secret_bits: str, oracle_func) -> Tuple[str, int]:
    """
    Classical algorithm to find the hidden bitstring.
    Requires up to n queries to determine each bit.
    
    Args:
        secret_bits: The hidden string (for comparison)
        oracle_func: Function that computes s·x (mod 2)
        
    Returns:
        Tuple of (recovered_string, number_of_queries)
    """
    n = len(secret_bits)
    recovered = ['0'] * n
    queries = 0
    
    # Query each bit position individually
    for i in range(n):
        # Create query string with 1 in position i, 0s elsewhere
        query = ['0'] * n
        query[i] = '1'
        query_string = ''.join(query)
        
        # Query the oracle
        result = oracle_func(query_string)
        queries += 1
        
        # If oracle returns 1, then s_i = 1
        recovered[i] = str(result)
    
    return ''.join(recovered), queries

def oracle_function(secret: str, x: str) -> int:
    """
    Classical oracle function: f_s(x) = s·x (mod 2)
    
    Args:
        secret: Hidden bitstring
        x: Query bitstring
        
    Returns:
        Dot product modulo 2
    """
    return sum(int(s) * int(xi) for s, xi in zip(secret, x)) % 2

def run_bernstein_vazirani_demo():
    """Main demonstration of the Bernstein-Vazirani algorithm."""
    print("🔬 Qiskit Bernstein-Vazirani Algorithm Demo")
    print("=" * 60)
    print("This demo shows quantum advantage in finding hidden information!")
    print("Based on IBM Qiskit: https://www.ibm.com/quantum/qiskit")
    print("=" * 60)
    
    if not QISKIT_AVAILABLE:
        return
    
    # Generate random secret bitstring
    n_qubits = 6
    secret = ''.join(random.choice('01') for _ in range(n_qubits))
    
    print(f"\n🎯 Challenge: Find the hidden {n_qubits}-bit string!")
    print(f"Secret bitstring (hidden from algorithm): {secret}")
    print(f"Classical approach needs up to {n_qubits} queries")
    print("Quantum approach needs only 1 query!")
    
    # === QUANTUM APPROACH ===
    print(f"\n🌟 Quantum Approach (Bernstein-Vazirani):")
    print("-" * 40)
    
    # Build quantum circuit
    start_time = time.time()
    qc, n = bernstein_vazirani_circuit(secret)
    
    # Simulate on quantum computer
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    
    print("Running quantum simulation...")
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    quantum_time = time.time() - start_time
    
    # Find most frequent measurement
    recovered_quantum = max(counts, key=counts.get)
    success_rate = counts.get(recovered_quantum, 0) / 1024 * 100
    
    print(f"✅ Quantum result: {recovered_quantum}")
    print(f"✅ Success rate: {success_rate:.1f}%")
    print(f"✅ Time: {quantum_time:.4f} seconds")
    print(f"✅ Oracle queries: 1")
    
    # === CLASSICAL APPROACH ===
    print(f"\n💻 Classical Approach (Bit-by-bit):")
    print("-" * 40)
    
    start_time = time.time()
    recovered_classical, num_queries = classical_baseline(
        secret, lambda x: oracle_function(secret, x)
    )
    classical_time = time.time() - start_time
    
    print(f"✅ Classical result: {recovered_classical}")
    print(f"✅ Oracle queries: {num_queries}")
    print(f"✅ Time: {classical_time:.4f} seconds")
    
    # === COMPARISON ===
    print(f"\n📊 Comparison:")
    print("-" * 40)
    print(f"Secret string:     {secret}")
    print(f"Quantum recovery:  {recovered_quantum} ({'✅ Correct' if recovered_quantum == secret else '❌ Wrong'})")
    print(f"Classical recovery: {recovered_classical} ({'✅ Correct' if recovered_classical == secret else '❌ Wrong'})")
    print(f"\nQuantum advantage: {num_queries}x fewer oracle queries!")
    
    return qc, counts, secret, recovered_quantum

def visualize_results(qc, counts, secret, recovered):
    """Create visualizations of the quantum circuit and results."""
    if not QISKIT_AVAILABLE:
        return
        
    print(f"\n📈 Creating Visualizations...")
    
    # Set up matplotlib for better rendering
    try:
        plt.style.use('default')
    except:
        pass
    
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 10))
    
    # 1. Quantum Circuit Diagram
    ax1 = plt.subplot(2, 2, 1)
    try:
        qc_draw = qc.draw('mpl', ax=ax1)
        ax1.set_title('Bernstein-Vazirani Quantum Circuit', fontsize=12, pad=20)
    except Exception as e:
        ax1.text(0.5, 0.5, f'Circuit diagram\n(install matplotlib for visualization)\n{qc}', 
                ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title('Bernstein-Vazirani Quantum Circuit')
    
    # 2. Measurement Results Histogram
    ax2 = plt.subplot(2, 2, 2)
    if counts:
        try:
            # Sort results for better visualization
            sorted_counts = dict(sorted(counts.items()))
            bars = ax2.bar(range(len(sorted_counts)), list(sorted_counts.values()), 
                          color=['red' if k == secret else 'lightblue' for k in sorted_counts.keys()])
            ax2.set_xticks(range(len(sorted_counts)))
            ax2.set_xticklabels(list(sorted_counts.keys()), rotation=45)
            ax2.set_xlabel('Measured Bitstrings')
            ax2.set_ylabel('Counts (out of 1024 shots)')
            ax2.set_title('Quantum Measurement Results')
            
            # Highlight the correct answer
            for i, (key, bar) in enumerate(zip(sorted_counts.keys(), bars)):
                if key == secret:
                    bar.set_color('red')
                    ax2.annotate('Secret!', xy=(i, sorted_counts[key]), 
                               xytext=(i, sorted_counts[key] + 50),
                               arrowprops=dict(arrowstyle='->', color='red'),
                               ha='center', color='red', fontweight='bold')
        except Exception as e:
            ax2.text(0.5, 0.5, f'Measurement results:\n{counts}', 
                    ha='center', va='center', transform=ax2.transAxes)
    
    # 3. Algorithm Comparison
    ax3 = plt.subplot(2, 2, 3)
    algorithms = ['Quantum\n(BV)', 'Classical\n(Bit-by-bit)']
    queries = [1, len(secret)]
    colors = ['green', 'orange']
    
    bars = ax3.bar(algorithms, queries, color=colors, alpha=0.7)
    ax3.set_ylabel('Number of Oracle Queries')
    ax3.set_title('Quantum vs Classical Efficiency')
    ax3.set_ylim(0, max(queries) * 1.2)
    
    # Add value labels on bars
    for bar, query in zip(bars, queries):
        height = bar.get_height()
        ax3.annotate(f'{query}', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold')
    
    # 4. Quantum Advantage Explanation
    ax4 = plt.subplot(2, 2, 4)
    ax4.axis('off')
    
    explanation = f"""
🎯 Bernstein-Vazirani Algorithm

📖 Problem: Find hidden bitstring s = "{secret}"

🔬 Quantum Solution:
• Create superposition of all inputs
• Apply oracle once to encode s as phases  
• Use interference to extract s directly
• Result: s recovered in 1 oracle query

💻 Classical Solution:
• Query each bit position individually
• Need up to n = {len(secret)} oracle queries
• No interference or superposition

⚡ Quantum Advantage: {len(secret)}x fewer queries!

🌐 This demonstrates fundamental quantum
   computing advantages using IBM Qiskit.
"""
    
    ax4.text(0.05, 0.95, explanation, transform=ax4.transAxes, fontsize=9,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.5))
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Visualizations displayed!")

def extended_demonstrations():
    """Run extended demonstrations with different parameters."""
    if not QISKIT_AVAILABLE:
        return
        
    print(f"\n🚀 Extended Demonstrations:")
    print("=" * 60)
    
    # 1. Scale Test
    print("\n1️⃣ Scalability Test:")
    for n in [4, 6, 8, 10]:
        secret = ''.join(random.choice('01') for _ in range(n))
        qc, _ = bernstein_vazirani_circuit(secret)
        
        simulator = AerSimulator()
        compiled = transpile(qc, simulator)
        result = simulator.run(compiled, shots=100).result()
        counts = result.get_counts()
        
        recovered = max(counts, key=counts.get)
        success = "✅" if recovered == secret else "❌"
        print(f"   n={n}: {success} Secret: {secret}, Recovered: {recovered}")
    
    # 2. Multiple Secret Test
    print("\n2️⃣ Success Rate Test (n=6, 10 trials):")
    successes = 0
    trials = 10
    
    for i in range(trials):
        secret = ''.join(random.choice('01') for _ in range(6))
        qc, _ = bernstein_vazirani_circuit(secret)
        
        simulator = AerSimulator()
        compiled = transpile(qc, simulator)
        result = simulator.run(compiled, shots=100).result()
        counts = result.get_counts()
        
        recovered = max(counts, key=counts.get)
        if recovered == secret:
            successes += 1
    
    print(f"   Success rate: {successes}/{trials} = {successes/trials*100:.0f}%")
    
    # 3. Circuit Depth Analysis
    print("\n3️⃣ Circuit Analysis:")
    n = 8
    secret = '1' * n  # Worst case: all 1s
    qc, _ = bernstein_vazirani_circuit(secret)
    
    print(f"   Circuit depth: {qc.depth()}")
    print(f"   Gate count: {qc.size()}")
    print(f"   Qubits used: {qc.num_qubits}")

def main():
    """Main function to run the Bernstein-Vazirani demonstration."""
    print("\n🌟 Welcome to the Qiskit Bernstein-Vazirani Demo!")
    print("=" * 60)
    print("This demo showcases quantum computing using IBM's Qiskit framework.")
    print("We'll demonstrate the Bernstein-Vazirani algorithm - a perfect example")
    print("of quantum advantage in a simple, easy-to-understand problem.")
    print("=" * 60)
    
    if not QISKIT_AVAILABLE:
        print("\n❌ Qiskit is not available. Please install it:")
        print("   pip install qiskit qiskit-aer matplotlib")
        return
    
    try:
        # Run main demonstration
        qc, counts, secret, recovered = run_bernstein_vazirani_demo()
        
        # Create visualizations
        print(f"\n📊 Would you like to see visualizations? (Close plots to continue)")
        visualize_results(qc, counts, secret, recovered)
        
        # Extended demonstrations
        extended_demonstrations()
        
        print(f"\n🎓 Key Learning Points:")
        print("• Quantum algorithms can solve some problems exponentially faster")
        print("• Superposition allows parallel exploration of solution space")
        print("• Quantum interference enables extracting hidden information")
        print("• Qiskit provides powerful tools for quantum algorithm development")
        
        print(f"\n🌐 Learn More:")
        print("• IBM Qiskit: https://www.ibm.com/quantum/qiskit")
        print("• Qiskit Textbook: https://qiskit.org/textbook/")
        print("• Quantum algorithms: https://qiskit.org/ecosystem/algorithms/")
        
    except Exception as e:
        print(f"❌ Error in Bernstein-Vazirani demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
