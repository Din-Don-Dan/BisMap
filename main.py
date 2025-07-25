import networkx as nx
import bispy as bp #https://github.com/fandreuz/BisPy
#import matplotlib.pyplot as plt

coupling_edges = [[0,1],[0,2],[1,2],[3,2],[3,4],[4,2]]
Coupling = nx.DiGraph()
Coupling.add_edges_from(coupling_edges)

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
print(roots)

BG = nx.union(Coupling, Circuit)
rt = max(BG.nodes)+1
for x in roots:
    BG.add_edge(rt, x)

subax3 = plt.subplot(111)
nx.draw(BG, with_labels=True, font_weight='bold')


print(bp.dovier_piazza_policriti(BG, is_integer_graph=True))

# 5 a0, 6 a1, 7 b0, 8 b1

# mapping esatto da https://hal.science/hal-01655951/file/Siraichi_QubitAllocation_CGO18.pdf:
# 0 -> 6, 1 -> x, 2 -> 7, 3 -> 5, 4 -> 8

# coupling:
# [0,1],[0,2],[1,2],[3,2],[3,4],[4,2]

# mapped circuit interactions after Bis [(2, 8), (1, 4, 7), (6,), (0, 3, 5), (9,)]:
# 5 -> 3, 6 -> 0, 7 -> 4, 8 -> 2. (9 artificiale rimosso) 
# [5,7],[5,8],[6,7],[7,8] in
# [3,2],[3,4],[0,2],[2,4]

# effettivamente si introduce solo il reversal in 2,4