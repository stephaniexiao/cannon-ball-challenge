import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import random


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    iterations = 0
    best_c = []
    best_k = []

    if len(list(G.nodes)) <= 30:
        iterations = 500
    elif len(list(G.nodes)) <= 50:
        iterations = 200
    elif len(list(G.nodes)) <= 100: 
        iterations = 15
    first_time = True
    for i in range(iterations):
        m = 0
        t = len(list(G.nodes)) - 1
        if len(list(G.nodes)) <= 30:
            max_k, max_c, m = 15, 1, 100
        elif len(list(G.nodes)) <= 50:
            max_k, max_c, m = 50, 3, 100
        elif len(list(G.nodes)) <= 100: 
            max_k, max_c, m = 100, 5, 500
        else:
            max_k, max_c = 0, 0
        c, k, m, max_c, max_k, first_time = helper(G, m, t, max_c, max_k, first_time)
        first_time = False
        if calculate_score(G, c, k, t) > calculate_score(G, best_c, best_k, t):
            best_c, best_k = c, k
    print("END")
    return best_c, best_k

def helper(G, m, t, max_c, max_k, first_time):
    c, k = [], []
    if m <= 0:
        return c, k, m, max_c, max_k, first_time
    m = m - 1
    edges = list(G.edges) # [(1, 5)]
    nodes = list(G.nodes) # [5]
    shortest_path_vertices = nx.dijkstra_path(G, 0, t)
    shortest_path_edges_and_vertices = []
    for i in range(len(shortest_path_vertices)): # [0, 1, 2, 5, 3, 4]
        # Safety check for i+1 case for edges
        if i + 1 < len(shortest_path_vertices):
            edge_weight = G[shortest_path_vertices[i]][shortest_path_vertices[i+1]]['weight']
            shortest_path_edges_and_vertices.append((shortest_path_vertices[i], shortest_path_vertices[i+1], edge_weight))
        # Looping through edges in Dijkstras to get edge weights + calculate heuristic
        v = shortest_path_vertices[i]
        vertex_weight, count = 0, 0
        for edge in edges: 
            if edge[0] == v or edge[1] == v:
                vertex_weight +=  G[edge[0]][edge[1]]['weight']
                count += 1
        if count > 0:
            vertex_weight = (vertex_weight / count) - (0.1 * vertex_weight)
        shortest_path_edges_and_vertices.append((v, None, vertex_weight))

    # 60% we sort array in ascending, 20% we sort in descending, 20% we don't sort
    rand_prob = random.random()
    if rand_prob <= 0.6 or first_time:
        shortest_path_edges_and_vertices.sort(key = lambda x: x[2], reverse = False)
    elif rand_prob <= 0.8:
        shortest_path_edges_and_vertices.sort(key = lambda x: x[2], reverse = True)
    else:
        random.shuffle(shortest_path_edges_and_vertices)
    for A, B, weight in shortest_path_edges_and_vertices:
        if i<= 0 or (max_k <= 0 and max_c <= 0):
            return c, k, m, max_c, max_k, first_time
        G_copy = G.copy()
        #20% of the time, you just continue
        rand_prob_2 = random.random()
        if rand_prob_2 <= 0.2 and not first_time:
            continue 
        if B == None: 
            if max_c <= 0:
                continue
            if A == 0 or A == t:
                continue
            if nx.is_isolate(G, A):
                continue
            if A in c: 
                continue
            G_copy.remove_node(A)
            c.append(A)
            max_c = max_c - 1
        elif B != None:
            if max_k <= 0:
                continue
            if (A, B) in k or (B, A) in k:
                continue
            G_copy.remove_edge(A, B) #args: u, v
            k.append((A, B))
            max_k = max_k - 1
        # Checks if removing disconnects the graph
        if is_valid_solution(G, c, k, t): #note this returns true when a node is disconnected
            new_c, new_k, m, max_c, max_k, first_time  = helper(G_copy, m, t, max_c, max_k, first_time)
            c_copy = c + new_c
            k_copy = k + new_k
            if is_valid_solution(G, c_copy, k_copy, t):
                if calculate_score(G, c_copy, k_copy, t) > calculate_score(G, c, k, t): 
                    c += new_c
                    k += new_k
        else:
            if B == None:
                c.remove(A)
                max_c += 1
            else:
                k.remove((A, B))
                max_k += 1   
    return c, k, m, max_c, max_k, first_time
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
#     currScore = read_output_file(G, 'outputs/medium/medium-1.out', t)
#     print("currScore", currScore)
#     if currScore < calculate_score(G, c, k, t):
#         write_output_file(G, c, k, 'outputs/medium/medium-1.out')

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
        # print("distance", distance)
        currScore = read_output_file(G, output_path, t)
        # print("currScore", currScore)
        if currScore < distance:
                        write_output_file(G, c, k, output_path)
