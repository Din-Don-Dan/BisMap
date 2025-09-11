import random
import a_utils
import networkx as nx
import time
import matplotlib.pyplot as plt

#system clock estimate
def resolution():
    start = time.monotonic()
    while time.monotonic() == start:
        pass
    stop = time.monotonic()
    return stop - start

def benchmark(input1, input2, func, resolution, maxError = 0.001):
    tmin = resolution * (1 + (1 / maxError))
    count = 0
    start = time.monotonic()

    while time.monotonic() - start < tmin:
        random.seed(2**count)
        func(input1, input2)
        count += 1
    duration = time.monotonic() - start
    return  duration / count

if __name__ == "__main__":
    resolution = resolution()

    # add weights to all the edges of all Couplings 
    a_utils.add_weights(a_utils.devices_coupling_maps_dict)

    # plot average time to compute mapping for all device couplings with the same circuit. 
    i = 0
    points = [(None,None)] * len(a_utils.devices_coupling_maps_dict.keys())
    for x, y in a_utils.devices_coupling_maps_dict.items():
        print(x)
        Coupling = nx.DiGraph()
        Coupling.add_weighted_edges_from(y)
        Coupling.remove_edges_from(a_utils.filter(Coupling))

        n = max(Coupling.nodes)
        circuit_edges = [[n+1,n+3],[n+1,n+4],[n+2,n+3],[n+3,n+4]] #[[1,3],[1,4],[2,3],[3,4]]
    
        points[i] = (x,
                     benchmark(Coupling, circuit_edges, a_utils.bismap, resolution))
        i += 1

    xs, ys1= zip(*points)
    plt.figure()
    plt.scatter(xs, ys1)

    plt.title('Average mapping time')
    plt.xlabel('Coupling architecture')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.savefig('grafico.png')
    plt.show()