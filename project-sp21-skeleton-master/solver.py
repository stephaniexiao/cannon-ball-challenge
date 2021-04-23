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
    m = 100

    t = len(G.nodes) - 1

    c, k, m = helper(G, m, t)
    print("END")
    return c, k 

def helper(G, m, t):

    c = []
    k = []

    if m <= 0:
        return c, k, m
    m = m - 1

    edges = list(G.edges) # [(1, 5)]
    nodes = list(G.nodes) # [5]
    print("Nodes:", nodes)

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
    shortest_path_vertices = nx.dijkstra_path(G, 0, t)

    # shortest_path_edges = []
    # for i in range(len(shortest_path_vertices) - 1): # [0, 1, 2, 5, 3, 4]
    #     edge_weight = G[shortest_path_vertices[i]][shortest_path_vertices[i+1]]['weight']
    #     shortest_path_edges.append((shortest_path_vertices[i], shortest_path_vertices[i+1], edge_weight))


    shortest_path_edges_and_vertices = []


    for i in range(len(shortest_path_vertices)): # [0, 1, 2, 5, 3, 4]
    
        # Safety check for i+1 case for edges
        if i + 1 < len(shortest_path_vertices):
            edge_weight = G[shortest_path_vertices[i]][shortest_path_vertices[i+1]]['weight']
            shortest_path_edges_and_vertices.append((shortest_path_vertices[i], shortest_path_vertices[i+1], edge_weight))

        # Looping through edges in Dijkstras to get edge weights + calculate heuristic
        v = shortest_path_vertices[i]
        vertex_weight = 0
        count = 0
        for edge in edges: 
            if edge[0] == v or edge[1] == v:
                vertex_weight +=  G[edge[0]][edge[1]]['weight']
                count += 1
        if count > 0:
            vertex_weight = (vertex_weight / count) - (0.1 * vertex_weight)
        shortest_path_edges_and_vertices.append((v, None, vertex_weight))

    # Sorting all weights in ascending order
    shortest_path_edges_and_vertices.sort(key = lambda x: x[2], reverse = False)
    print(shortest_path_edges_and_vertices)

    # print(shortest_path_edges_and_vertices)
    # min_edge_weight = min(shortest_path_edges, key = lambda x: x[2]) #(A, B, weight)

    # best_path = shortest_path_edges
    # best_weights = sum(shortest_path_edges, key = lambda x: x[2])
    # i = 5
    for A, B, weight in shortest_path_edges_and_vertices:
        # i = i - 1
        # print("c =", c)
        # print("k =", k)
        # print("max_c =", max_c)
        # print("max_k =", max_k)
        if i<= 0 or (max_k <= 0 and max_c <= 0):
            # print ("END")
            return c, k, m
        G_copy = G.copy()

        if B == None: 
            if max_c <= 0:
                # print("case 1")
                continue
            if A == 0 or A == t:
                # print("case 2")
                continue
            if nx.is_isolate(G, A):
                # print("case 3")
                continue
            G_copy.remove_node(A)
            # print("removed_node:", A)
            c.append(A)
            max_c = max_c - 1
        
        else:
            if max_k <= 0:
                continue
            G_copy.remove_edge(A, B) #args: u, v
            # print("removed edge:", (A, B))

            k.append((A, B))
            max_k = max_k - 1

        # Checks if removing disconnects the graph
        if is_valid_solution(G, c, k, t): #note this returns true when a node is disconnected
            new_c, new_k, m = helper(G_copy, m, t)
            c_copy = c + new_c
            k_copy = k + new_k
            if is_valid_solution(G, c_copy, k_copy, t):
                if calculate_score(G, c_copy, k_copy, t) > calculate_score(G, c, k, t): 
                    c += new_c
                    k += new_k
        else:
            if B == None:
                print("added back node:", A)
                c.remove(A)
                max_c += 1
            else:
                print("added back edge: ", (A, B))
                k.remove((A, B))
                max_k += 1   
    return c, k, m



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
# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     t = len(G.nodes) - 1
#     assert is_valid_solution(G, c, k, t)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k, t)))
#     write_output_file(G, c, k, 'outputs/large/large-1.out')

# RUN if you want to run ALL inputs:
# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/small/*')
    for input_path in inputs:
        output_path = 'outputs/small/' + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        c, k = solve(G)
        t = len(G.nodes) - 1
        assert is_valid_solution(G, c, k, t)
        distance = calculate_score(G, c, k, t)
        write_output_file(G, c, k, output_path)
