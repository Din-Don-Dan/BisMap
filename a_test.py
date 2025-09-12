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

    for a,b in circuit_map:
        if a < n_entries and b < n_entries:
            Circuit.add_edge(a, b)
    qcircuit, qr = construct_circuit(Circuit)

    coupling_edges = a_utils.filter_list(coupling_map)
    
    Coupling.add_edges_from(coupling_edges)
    coupling_map_nodes = Coupling.number_of_nodes()

    if coupling_map_nodes < qcircuit.num_qubits: raise ValueError
    ancilla = QuantumRegister(coupling_map_nodes-qcircuit.num_qubits, 'ancilla')
    qcircuit.add_register(ancilla)
    backend = GenericBackendV2(qcircuit.num_qubits)
    backend = GenericBackendV2(num_qubits=qcircuit.num_qubits, 
                                coupling_map = coupling_edges)
    
    transpiled_circuit = transpile(qcircuit, backend=backend, optimization_level=0, layout_method = 'sabre', routing_method='sabre')
    #print(transpiled_circuit.count_ops())


def bismap_circuit(circuit_map, n_entries, coupling_map):
    Circuit = nx.DiGraph()
    Coupling = nx.DiGraph()

    for a,b in circuit_map:
        if a < n_entries and b < n_entries:
            Circuit.add_edge(a, b)
    circuit_edges = Circuit.edges()
    qcircuit, qr = construct_circuit(Circuit)

    coupling_edges = a_utils.filter_list(coupling_map)
    
    Coupling.add_edges_from(coupling_edges)
    coupling_map_nodes = Coupling.number_of_nodes()

    if coupling_map_nodes < qcircuit.num_qubits: raise ValueError
    ancilla = QuantumRegister(coupling_map_nodes-qcircuit.num_qubits, 'ancilla')
    qcircuit.add_register(ancilla)
    backend = GenericBackendV2(qcircuit.num_qubits)
    backend = GenericBackendV2(num_qubits=qcircuit.num_qubits, 
                                coupling_map = coupling_edges)
    
    circuit_edges = list(map(lambda a : a_utils.add_c(a, coupling_map_nodes), circuit_edges))

    mapping_bis = a_utils.bismap(Coupling, circuit_edges)

    initial_layout = Layout()
    mapped = {}

    for node in range(Circuit.number_of_nodes()):
        mapped.update({mapping_bis[node+coupling_map_nodes]: qr[node]})

    initial_layout.from_dict(mapped)

    transpiled_bis = transpile(qcircuit, backend=backend, optimization_level=0, initial_layout = initial_layout, routing_method='sabre')
            
    #print(transpiled_bis.count_ops())


if __name__ == "__main__":
    circuit_edges = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,8],[8,7],[8,9],[9,10],[10,11],[11,12],[12,13],[1,13],[2,12],[3,11],[4,10],[5,9],[6,8],[0,14],[13,14],[1,0],[2,1],[3,2],[4,3],[5,4],[6,5],[8,6],[7,8],[9,8],[10,9],[11,10],[12,11],[13,12],[13,1],[12,2],[11,3],[10,4],[9,5],[8,6],[14,0],[14,13]]
    
    # add weights to all the edges of all Couplings 
    a_utils.add_weights(a_utils.devices_coupling_maps_dict)
    a_utils.add_weights_list(circuit_edges)

    bismap_circuit(circuit_edges, 2, a_utils.devices_coupling_maps_dict["IBM Athens"])
