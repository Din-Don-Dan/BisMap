import networkx as nx
import bispy as bp #https://github.com/fandreuz/BisPy
import queue
#import matplotlib.pyplot as plt

# Ipotesi che Coupling e Circuit siano aciclici a priori (nessun problema di dimensioni di scc)
# nodi Coupling da 0 a n
# nodi Circuit da n+1 a m

coupling_edges = [[0,1],[0,2],[1,2],[3,2],[3,4],[4,2]]
Coupling = nx.DiGraph()
Coupling.add_edges_from(coupling_edges)
n = max(Coupling.nodes)
#Coupling_scc = nx.condensation(Coupling)
#print(Coupling_scc.number_of_nodes())

circuit_edges = [[5,7],[5,8],[6,7],[7,8]]
Circuit = nx.DiGraph()
Circuit.add_edges_from(circuit_edges)

#Circuitscc = nx.condensation(Circuit)
#print(Circuit_scc.number_of_nodes())

roots = []
for x in Circuit.nodes:
    if not Circuit.in_degree(x):
        roots.append(x)

for x in Coupling.nodes:
    if not Coupling.in_degree(x):
        roots.append(x)
#print(roots)

BG = nx.union(Coupling, Circuit)
rt = max(BG.nodes)+1
for x in roots:
    BG.add_edge(rt, x)

bis = bp.dovier_piazza_policriti(BG, is_integer_graph=True)

# mapping esatto da https://hal.science/hal-01655951/file/Siraichi_QubitAllocation_CGO18.pdf:
# 0 -> 6, 1 -> x, 2 -> 7, 3 -> 5, 4 -> 8

#come decidere il mapping:
coupling_stack = queue.LifoQueue(maxsize=n+1)
circuit_stack = queue.LifoQueue(maxsize=rt-n)
mapping = []

bis.reverse()

for bisset in bis:
    for node in bisset: #scorre m+1 nodi, lineare non quadratico
        if node == rt:
            continue
        if node <= n:
            if not circuit_stack.empty():
                candidate = circuit_stack.get()
                mapping.append([candidate, node])
            else:
                coupling_stack.put(node)
        if node > n:
            if not coupling_stack.empty():
                candidate = coupling_stack.get()
                mapping.append([node, candidate])
            else:
                circuit_stack.put(node)

mdict = dict(mapping)
print("Mapping qubit {logico : fisico} :", mdict)

mapped = []
for x in circuit_edges:
    mapped.append(list(map(mdict.get, x)))
print("Circuito mappato:", mapped)

# debug:
l = []
while not coupling_stack.empty():
    l.append(coupling_stack.get())
    print("qubit fisici non utilizzati:" ,l)
if not circuit_stack.empty():
    print("Errore - Circuit stack non vuota")
