from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library import *
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.compiler import transpile
from qiskit.transpiler import CouplingMap, Layout
from qiskit.transpiler.passes import BasisTranslator
from qiskit.circuit import EquivalenceLibrary
from qiskit.converters import circuit_to_dag, dag_to_circuit
from collections import deque
import networkx as nx
import random
import a_utils

random.seed(69420)

def construct_circuit(nxDiGraph) -> QuantumCircuit:

    # number of internal nodes of the binary tree representing the QRAM Bucket Brigade
    n_nodes = nxDiGraph.number_of_nodes()
    edges = list(nxDiGraph.edges())

    qrouters = QuantumRegister(n_nodes, 'qrouter')

    qc = QuantumCircuit(qrouters)
    
    for val in edges:
        qc.cx(val[0], val[1])

    return qc, qrouters

def sabre_circuit(circuit_map, n_entries, coupling_map):
    Circuit = nx.DiGraph()
    Coupling = nx.DiGraph()
    Coupling.add_weighted_edges_from(coupling_map)
    Coupling.remove_edges_from(a_utils.filter(Coupling))
    coupling_map_nodes = Coupling.number_of_nodes()

    for a,b,w in circuit_map:
        if a < n_entries and b < n_entries:
            Circuit.add_weighted_edges_from((a, b, w))
    Circuit.remove_edges_from(a_utils.filter(Circuit))
    qcircuit, qr = construct_circuit(Circuit)

    if coupling_map_nodes < qcircuit.num_qubits: raise ValueError
    ancilla = QuantumRegister(coupling_map_nodes-qcircuit.num_qubits, 'ancilla')
    qcircuit.add_register(ancilla)
    backend = GenericBackendV2(qcircuit.num_qubits)
    backend = GenericBackendV2(num_qubits=qcircuit.num_qubits, 
                                coupling_map = coupling_map)
    
    transpiled_circuit = transpile(qcircuit, backend=backend, optimization_level=0, layout_method = 'sabre', routing_method='sabre')
    print(transpiled_circuit.count_ops())


def bismap_circuit(circuit_map, n_entries, coupling_map):
    Circuit = nx.DiGraph()
    Coupling = nx.DiGraph()
    Coupling.add_weighted_edges_from(coupling_map)
    Coupling.remove_edges_from(a_utils.filter(Coupling))
    coupling_map_nodes = Coupling.number_of_nodes()

    for a,b,w in circuit_map:
        if a < n_entries and b < n_entries:
            Circuit.add_weighted_edges_from((a, b, w))
    Circuit.remove_edges_from(a_utils.filter(Circuit))
    qcircuit, qr = construct_circuit(Circuit)

    if coupling_map_nodes < qcircuit.num_qubits: raise ValueError
    ancilla = QuantumRegister(coupling_map_nodes-qcircuit.num_qubits, 'ancilla')
    qcircuit.add_register(ancilla)
    backend = GenericBackendV2(qcircuit.num_qubits)
    backend = GenericBackendV2(num_qubits=qcircuit.num_qubits, 
                                coupling_map = coupling_map)
    
    mapping_bis = a_utils.bismap(Coupling, circuit_map)
    initial_layout = Layout()
    mapped = {}

    for node in range(Circuit.number_of_nodes()):
        mapped.update({mapping_bis[node+coupling_map_nodes]: qr[node]})

    initial_layout.from_dict(mapped)

    transpiled_bis = transpile(qcircuit, backend=backend, optimization_level=0, initial_layout = initial_layout, routing_method='sabre')
            
    print(transpiled_bis.count_ops())


if __name__ == "__main__":

    print("test functions file")
