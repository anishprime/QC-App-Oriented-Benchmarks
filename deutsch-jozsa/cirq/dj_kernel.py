"""
Deutsch-Jozsa Benchmark Program - Cirq
"""

from collections import defaultdict
import sys
import time

import cirq
import numpy as np

# sys.path[1:1] = ["_common", "_common/cirq"]
# sys.path[1:1] = ["../../_common", "../../_common/cirq"]
# import cirq_utils as cirq_utils
# import execute as ex
# import metrics as metrics

np.random.seed(0)

verbose = False

# saved circuits for display
QC_ = None
Uf_ = None

############### Circuit Definition

# Create a constant oracle, appending gates to given circuit
def constant_oracle(input_size, num_qubits):

    #Initialize Quantum Circuit
    qr = [cirq.GridQubit(i, 0) for i in range(num_qubits)]
    qc = cirq.Circuit()

    #Added identities because cirq requires gates on each qubit
    for qubit in range(input_size):
        qc.append(cirq.I(qr[qubit]))

    #Add X Gate or Identity at random on last qubit for constant oracle
    output = np.random.randint(2)
    if output == 1:
        qc.append(cirq.X(qr[input_size]))
    else:
        qc.append(cirq.I(qr[input_size]))

    return cirq_utils.to_gate(num_qubits=num_qubits, circ=qc, name="Uf")

# Create a balanced oracle.
# Perform CNOTs with each input qubit as a control and the output bit as the target.
# Vary the input states that give 0 or 1 by wrapping some of the controls in X-gates.
def balanced_oracle(input_size, num_qubits):

    #Initialize Quantum Circuit
    qr = [cirq.GridQubit(i, 0) for i in range(num_qubits)]
    qc = cirq.Circuit()

    b_str = "10101010101010101010"  # permit input_string up to 20 chars
    for qubit in range(input_size):
        if b_str[qubit] == '1':
            qc.append(cirq.X(qr[qubit]))
            
    for qubit in range(input_size):
        qc.append(cirq.CX(qr[qubit], qr[input_size]))

    for qubit in range(input_size):
        if b_str[qubit] == '1':
            qc.append(cirq.X(qr[qubit]))

    return cirq_utils.to_gate(num_qubits=num_qubits, circ=qc, name="Uf")

# Create benchmark circuit
def DeutschJozsa(num_qubits, type):
    # size of input is one less than available qubits
    input_size = num_qubits - 1

    # allocate qubits
    qr = [cirq.GridQubit(i, 0) for i in range(num_qubits)]
    qc = cirq.Circuit()

    # start with flipping the ancilla to 1
    qc.append(cirq.X(qr[input_size]))

    # Add Hadamard on all qubits, including ancilla
    for i_qubit in range(num_qubits):
        qc.append(cirq.H(qr[i_qubit]))

    # Add a constant or balanced oracle function
    if type == 0:
        Uf = constant_oracle(input_size, num_qubits)
    else:
        Uf = balanced_oracle(input_size, num_qubits)

    qc.append(Uf.on(*qr))
  
    # end with Hadamard on all qubits, excluding ancilla
    for i_qubit in range(input_size):
        qc.append(cirq.H(qr[i_qubit]))

    # uncompute ancilla qubit, not necessary for algorithm
    qc.append(cirq.X(qr[input_size]))
    
    # measure all qubits, excluding ancilla
    qc.append(cirq.measure(*[qr[i_qubit] for i_qubit in range(input_size)], key='result'))

    # save smaller circuit example for display
    global QC_, Uf_
    if QC_ == None or num_qubits <= 6:
        if num_qubits < 9: QC_ = qc
    if Uf_ == None or num_qubits <= 6:
        if num_qubits < 9: Uf_ = Uf

    # return a handle on the circuit
    return qc

def kernel_draw():
    # print a sample circuit
    print("Sample Circuit:"); print(QC_ if QC_ != None else "  ... too large!")
    qr_state = [cirq.GridQubit(i, 0) for i in range(Uf_.num_qubits)] # we need to create registers to print circuits in cirq
    print("\nQuantum Oracle 'Uf' ="); print(cirq.Circuit(cirq.decompose(Uf_.on(*qr_state))) if Uf_ != None else " ... too large!")
