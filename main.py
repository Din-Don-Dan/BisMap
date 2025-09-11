import random
import a_utils
import a_test
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

def benchmark(input1, input2, input3, func, resolution, maxError = 0.001):
    tmin = resolution * (1 + (1 / maxError))
    count = 0
    start = time.monotonic()

    while time.monotonic() - start < tmin:
        random.seed(2**count)
        func(input1, input2, input3)
        count += 1
    duration = time.monotonic() - start
    return  duration / count

if __name__ == "__main__":
    resolution = resolution()

    # List of number of entries. For each entry, a different QRAM circuit is constructed.
    n_entries_list = [2, 4, 8, 16, 32, 64]

    # test-tailored data

    circuit_edges = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,8],[8,7],[8,9],[9,10],[10,11],[11,12],[12,13],[1,13],[2,12],[3,11],[4,10],[5,9],[6,8],[0,14],[13,14],[1,0],[2,1],[3,2],[4,3],[5,4],[6,5],[8,6],[7,8],[9,8],[10,9],[11,10],[12,11],[13,12],[13,1],[12,2],[11,3],[10,4],[9,5],[8,6],[14,0],[14,13]]
    
    # add weights to all the edges of all Couplings 
    a_utils.add_weights(a_utils.devices_coupling_maps_dict)
    a_utils.add_weights_list(circuit_edges)
    
    # plot average time to compute mapping for all device couplings with the same circuit. 
    i = 0
    points = [(None,None)] * len(a_utils.devices_coupling_maps_dict.keys())
    points_2 = [(None,None)] * len(a_utils.devices_coupling_maps_dict.keys())
    for n in n_entries_list:
        for device, coupling_map in a_utils.devices_coupling_maps_dict.items():
            print(device)
    
            points[i] = (device,
                        benchmark(circuit_edges, n, coupling_map, a_test.sabre_circuit, resolution))
        
            points_2[i] = (device,
                        benchmark(circuit_edges, n, coupling_map, a_test.bismap_circuit, resolution))
            i += 1

    xs1, ys1= zip(*points)
    plt.figure()
    plt.scatter(xs1, ys1)

    plt.title('Average mapping time')
    plt.xlabel('Coupling architecture')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.savefig('grafico_sabre.png')
    plt.show()

    xs2, ys2= zip(*points_2)
    plt.figure()
    plt.scatter(xs2, ys2)

    plt.title('Average mapping time')
    plt.xlabel('Coupling architecture')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.savefig('grafico_bis.png')
    plt.show()