import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import itertools


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """

    edges = list(G.edges) # [(1, 5)]
    nodes = list(G.nodes) # [5]
    
    if len(nodes) <= 30:
        max_k = 15
        max_c = 1
    
    elif len(nodes) <= 50:
        max_k = 50
        max_c = 3
    
    elif len(nodes) <= 100: 
        max_k = 100
        max_c = 5

    else:
        max_k = 0
        max_c = 0
    
    
    shortest_path_vertices = nx.dijkstra_path(G, 0, len(G.nodes) - 1)

    shortest_path_edges = []
    for i in range(len(shortest_path_vertices) - 1): # [0, 1, 2, 5, 3, 4]
        edge_weight = G[shortest_path_vertices[i]][shortest_path_vertices[i+1]]['weight']
        shortest_path_edges.append((shortest_path_vertices[i], shortest_path_vertices[i+1], edge_weight))

    shortest_path_edges.sort(key = lambda x: x[2], reverse = False)
    # min_edge_weight = min(shortest_path_edges, key = lambda x: x[2]) #(A, B, weight)

    # best_path = shortest_path_edges
    # best_weights = sum(shortest_path_edges, key = lambda x: x[2])


    c = []
    k = []
    for A, B, weight in shortest_path_edges:
        G_copy = G.copy()
        G_copy.remove_edge(A, B) #args: u, v
        
        k.append((A, B))
        #checks if removing disconnects the graph
        if is_valid_solution(G, c, k): 
            new_c, new_k = solve(G_copy)
            c_copy = c + new_c
            k_copy = k + new_k
            if is_valid_solution(G, c_copy, k_copy):
                if calculate_score(G, c_copy, k_copy) > calculate_score(G, c, k): 
                    c += new_c
                    k += new_k
        else:
            k.remove((A, B))
            
    return c, k

# def is_better(G_copy, new_c, new_k, best_curr_weight):
#     for e1, e2 in new_k:
#         G_copy.remove_edge(e1, e2)
#     for v1, v2 in new_c:
#         G_copy.remove_edge(v1, v2)

#     short_path_v = nx.dijkstra_path(G, 0, len(G.nodes) - 1)

#     short_path_e = []
#     for i in range(len(short_path_v) - 1): # [0, 1, 2, 5, 3, 4]
#         edge_weight = G[short_path_v[i]][short_path_v[i+1]]['weight']
#         short_path_e.append((short_path_v[i], short_path_v[i+1], edge_weight))

#     new_weights = sum(short_path_e, key = lambda x: x[2])
#     return best_curr_weight >= new_weights

    # G_copy remove all new_c and new_k
            # take edge weights and sum them
                # if better, replace best path and best weights


    # for v in shortest_path_vertices:
    #     shortest_path_edges.append((v, v+1))
    
    # while: checks to make sure we didn't remove over c cities
    # for v in shortest_path_vertices:
    #     G_copy = G.copy()


    # while: checks to make sure we haven't removed over k edges


    
    # shortest_path_vertices = nx.dijkstra_path(G, 0, len(G.nodes) - 1)
    # remove one edge (at random or starting from source)
    # run dijkstras from S to T, if disconnected = abort, else = we check if the path is longer / remove one edge and do same thing




# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# RUN if you want to run ONE input:
if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    c, k = solve(G)
    assert is_valid_solution(G, c, k)
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    write_output_file(G, c, k, 'outputs/100.out')

# RUN if you want to run ALL inputs:
#For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
