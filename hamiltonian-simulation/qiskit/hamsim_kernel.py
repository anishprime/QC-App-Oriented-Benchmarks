'''
Hamiltonian Simulation Benchmark Program - Qiskit Kernel
(C) Quantum Economic Development Consortium (QED-C) 2024.
'''

'''
There are multiple Hamiltonians and three methods defined for this kernel.
Hamiltonians are applied via a base class HamiltonianKernel and derived classes for specific hamiltonians.
The Hamiltonian name is specified in the "hamiltonian" argument.
The "method" argument indicates the type of fidelity comparison that will be done. 
In this case, method 3 is used to create a mirror circuit for scalability.
'''
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np
import math

pi = math.pi

# Gates to be saved for printing purpose.
# DEVNOTE: these are global for now, for convenience; improve later
XX_ = None
YY_ = None
ZZ_ = None
XXYYZZ_ = None
XX_mirror_ = None
YY_mirror_ = None
ZZ_mirror_ = None
XXYYZZ_mirror_ = None
XXYYZZ_quasi_mirror_ = None


# For validating the implementation of XXYYZZ operation (saved for possible use in drawing)
_use_XX_YY_ZZ_gates = False


#apply initial state to the quantum circuit
def initial_state(n_spins, init_state):
    #Initialize the quantum state.
    qr = QuantumRegister(n_spins)
    qc = QuantumCircuit(qr, name = "InitialState")
    if init_state == "checkerboard" or init_state == "neele":
        # Checkerboard state, or "Neele" state
        for k in range(0, n_spins, 2):
            qc.x([k])
    elif init_state == "ghz":
        # GHZ state: 1/sqrt(2) (|00...> + |11...>)
        qc.h(0)
        for k in range(1, n_spins):
            qc.cx(k-1, k)

    return qc


def HamiltonianSimulation(n_spins, K, t, hamiltonian, w, h_x, h_z, use_XX_YY_ZZ_gates, method, random_pauli_flag):

    qr = QuantumRegister(n_spins)
    cr = ClassicalRegister(n_spins)
    qc = QuantumCircuit(qr, cr, name = hamiltonian)

    qc_initial = initial_state(n_spins, init_state)
    qc.append()




